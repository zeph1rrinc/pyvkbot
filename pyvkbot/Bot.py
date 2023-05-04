import json
from typing import Callable
from typing import Union

import requests
import vk_api
from loguru import logger
from vk_api.bot_longpoll import VkBotEventType
from vk_api.bot_longpoll import VkBotLongPoll

from .Exceptions import DuplicateTriggerError
from .Exceptions import NotAvailableEventError
from .Exceptions import UnexpectedTriggerError
from .Keyboard import Keyboard
from .Types import ActionTypes
from .Types import AttachmentTypes
from .Types import EventTypes


class Bot:
    """
    Main class for working with vk bot

    :param token: VK access token
    :type token: str

    :param group_id: id of your group
    :type group_id: int

    :param main_chat: id of main chat for bot
    :type main_chat: int

    :param logging: if True - logging in stdout by loguru.logger
    :type logging: bool
    """

    def __init__(
        self, token: str, group_id: int, main_chat: int = None, logging: bool = True
    ):
        self.main_chat = main_chat
        self.vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.vk_session, group_id=group_id)
        self.logging = logging

        self.events = {
            EventTypes.MESSAGE: {},
            EventTypes.ACTION: {},
            EventTypes.ATTACHMENT: {},
        }

        self.start_command = None
        self.default_message = None

    def __bind(self, command: str, callback: Callable):
        cmd = command.lower()
        if cmd in self.events[EventTypes.MESSAGE]:
            raise DuplicateTriggerError(f"Command '{cmd}' already bound!")
        self.events[EventTypes.MESSAGE][cmd] = callback

    def __handle_events(self, event: str, trigger: str, message: dict):
        self.events[event][trigger](self, message)
        self.__log(f"handle event '{event}' with trigger '{trigger}'")

    def __log(self, message: str, error: bool = False):
        if self.logging:
            if error:
                logger.error(message)
                return
            logger.debug(message)

    def __validate_event(self, event: str, trigger: str = None):
        if event in (EventTypes.ACTION, EventTypes.ATTACHMENT) and not trigger:
            raise UnexpectedTriggerError(
                f"Not enough arguments for event '{event}'. See doc for more information"
            )
        if trigger:
            if any(
                [
                    all(
                        [
                            event == EventTypes.ACTION,
                            trigger.upper() not in ActionTypes.__dict__,
                        ]
                    ),
                    all(
                        [
                            event == EventTypes.ATTACHMENT,
                            trigger.upper() not in AttachmentTypes.__dict__,
                        ]
                    ),
                ]
            ):
                raise UnexpectedTriggerError(
                    f"Unexpected option '{trigger}' for event '{event}'"
                )
        return True

    def delete_message(self, peer_id: int, cmids: list):
        """
        Deleting message from group chat, if author is not admin

        :param peer_id: id of chat where you want to delete messages
        :type peer_id: int
        :param cmids: list of conversations ids of message, which you want to delete
        :type cmids: list
        """
        self.send_api_method(
            "messages.delete", {"peer_id": peer_id, "cmids": cmids, "delete_for_all": 1}
        )

    def message(self, trigger: str = None):
        """
        Decorator for creating handlers for messages

        :param trigger: trigger message for command. None for default answer
        :param type: str
        """

        def _wrapper(func):
            self.on(event=EventTypes.MESSAGE, callback=func, trigger=trigger)
            return func

        return _wrapper

    def attachment(self, trigger: str):
        """
        Decorator for creating handlers for attachments

        :param trigger: type of trigger attachment
        :param type: str
        """

        def _wrapper(func):
            self.on(event=EventTypes.ATTACHMENT, callback=func, trigger=trigger)
            return func

        return _wrapper

    def action(self, trigger: str):
        """
        Decorator for creating handlers for actions

        :param trigger: type of trigger action
        :param type: str
        """

        def __wrapper(func):
            self.on(event=EventTypes.ACTION, callback=func, trigger=trigger)
            return func

        return __wrapper

    def on(self, event: str, callback: Callable, trigger: str = None):
        """
        Creating handler for events in longpoll listen

        :param event: Event type. You can take in from Types
        :type event: str

        :param callback: Function, which is executed, when event triggers
        :type callback: Callable

        :param trigger: Trigger for event. Command for message or type of event for other
        :type trigger: str
        """
        self.__validate_event(event, trigger)
        match event:
            case EventTypes.ACTION:
                self.events[EventTypes.ACTION][trigger] = callback
            case EventTypes.MESSAGE:
                if trigger:
                    self.__bind(trigger, callback)
                else:
                    self.default_message = callback
            case EventTypes.ATTACHMENT:
                self.events[EventTypes.ATTACHMENT][trigger] = callback
            case _:
                raise NotAvailableEventError(
                    f"Not available event named '{event}'. See doc for more information"
                )
        self.__log(f"Bound new event '{event}', with trigger '{trigger}'")

    def parse_message(self, message: dict):
        """
        Closed method for parsing message

        :param message: message dict from event object
        :type message: dict
        """
        msg = message["text"].lower()
        cmd = msg.split("\n")[0].strip()
        id = message.get("peer_id")
        attachments = message.get("attachments")
        payload = None
        if message.get("payload"):
            payload = json.loads(message["payload"])
        action = message.get("action")
        if payload and payload.get("command") == "start" and self.start_command:
            self.start_command(self, message)
            return
        if action:
            action_type = action["type"]
            if action_type in self.events[EventTypes.ACTION]:
                self.__handle_events(EventTypes.ACTION, action["type"], message)
                return
        if attachments:
            attachment_type = attachments[0]["type"]
            if attachment_type in self.events[EventTypes.ATTACHMENT]:
                self.__handle_events(EventTypes.ATTACHMENT, attachment_type, message)
                return
        if msg:
            self.__log(f"Received new message from chat {id} - '{msg}'")
            for command in self.events[EventTypes.MESSAGE]:
                if command.find(cmd) != -1:
                    self.__handle_events(EventTypes.MESSAGE, cmd, message)
                    return
        if self.default_message:
            self.default_message(self, message)

    def start(self, callback: Callable):
        """
        Creating handler for "start" button in private messages

        :param callback: Function, which is executed, when button is pushed
        :type callback: Callable
        """
        self.start_command = callback

    def send_api_method(self, method: str, payload: dict):
        """
        Sending some vk api method

        :param method: VK api method
        :type method: str

        :param payload: dict of data to send in method
        :type payload: dict
        """
        response = self.vk_session.method(method, payload)
        self.__log(
            f"Sent api method '{method}'. "
            f"With payload {json.dumps(payload, ensure_ascii=False).encode('utf-8').decode()}. "
            f"Response: {json.dumps(response, ensure_ascii=False).encode('utf-8').decode()}"
        )
        return response

    def send_message(
        self, peer_id: int, text: str, keyboard: Union[str, Keyboard] = None
    ):
        """
        Sending message in chat

        :param peer_id: id of chat, where you want to send message
        :type peer_id: int

        :param text: text of message you wanted to send
        :type text: str

        :param keyboard: [OPTIONAL] Keyboard for user, if needed. Takes Keyboard class or json string
        :type keyboard: str | Keyboard
        """
        data = {"peer_id": peer_id, "message": text, "random_id": 0}
        if keyboard:
            if type(keyboard) == str:
                data["keyboard"] = keyboard
            else:
                data["keyboard"] = keyboard.get_keyboard()
        self.send_api_method("messages.send", data)

    def start_polling(self, callback: Callable = None):
        """
        Starting polling messages from users

        :param callback: [OPTIONAL] Function, which would be executed, when bot is started
        :type callback: Callable
        """
        try:
            if callback is not None:
                callback()
            for event in self.longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    self.parse_message(event.message)
        except requests.exceptions.ReadTimeout as _ex:
            self.__log(_ex, error=True)
            self.start_polling()
        except vk_api.exceptions.ApiError as _ex:
            self.__log(_ex, error=True)
            self.start_polling()
