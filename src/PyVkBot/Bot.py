import json
from typing import Callable
import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from loguru import logger
from typing import Union

from .Types import ActionTypes, EventTypes, AttachmentTypes
from .Exceptions import NotAvailableEventError, UnexpectedTriggerError, DuplicateTriggerError
from .Keyboard import Keyboard


class Bot:
    def __init__(self, token: str, main_chat: int = None, group_id: int = None, logging: bool = True):
        self.main_chat = main_chat
        self.vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.vk_session, group_id=group_id)

        self.events = {
            EventTypes.MESSAGE: {},
            EventTypes.ACTION: {},
            EventTypes.ATTACHMENT: {}
        }

        self.start_command = None
        self.default_message = None

        if not logging:
            logger.remove(handler_id=0)

    def __bind(self, command: str, callback: Callable):
        cmd = command.lower()
        if cmd in self.events[EventTypes.MESSAGE]:
            raise DuplicateTriggerError(f"Command '{cmd}' already bound!")
        self.events[EventTypes.MESSAGE][cmd] = callback

    def __handle_events(self, event: str, trigger: str, message: dict):
        self.events[event][trigger](self, message)
        logger.debug(f"handle event '{event}' with trigger '{trigger}'")

    def __validate_event(self, event: str, trigger: str = None):
        if event in (EventTypes.ACTION, EventTypes.ATTACHMENT) and not trigger:
            raise UnexpectedTriggerError(f"Not enough arguments for event '{event}'. See doc for more information")
        if trigger:
            if any([
                all([event == EventTypes.ACTION, trigger.upper() not in ActionTypes.__dict__]),
                all([event == EventTypes.ATTACHMENT, trigger.upper() not in AttachmentTypes.__dict__])
            ]):
                raise UnexpectedTriggerError(f"Unexpected option '{trigger}' for event '{event}'")
        return True

    def delete_message(self, peer_id: int, cmids: list):
        self.send_api_method("messages.delete", {"peer_id": peer_id, "cmids": cmids, "delete_for_all": 1})

    def on(self, event: str, callback: Callable, trigger: str = None):
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
                raise NotAvailableEventError(f"Not available event named '{event}'. See doc for more information")
        logger.debug(f"Bound new event '{event}', with trigger '{trigger}'")

    def parse_message(self, message: dict):
        msg = message['text'].lower()
        cmd = msg.split('\n')[0].strip()
        id = message.get("peer_id")
        attachments = message.get("attachments")
        payload = None
        if message.get('payload'):
            payload = json.loads(message['payload'])
        action = message.get('action')
        if payload and payload.get('command') == 'start' and self.start_command:
            self.start_command(self, message)
            return
        if action:
            action_type = action['type']
            if action_type in self.events[EventTypes.ACTION]:
                self.__handle_events(EventTypes.ACTION, action['type'], message)
                return
        if attachments:
            attachment_type = attachments[0]['type']
            if attachment_type in self.events[EventTypes.ATTACHMENT]:
                self.__handle_events(EventTypes.ATTACHMENT, attachment_type, message)
                return
        if msg:
            logger.debug(f"Received new message from chat {id} - '{msg}'")
            for command in self.events[EventTypes.MESSAGE]:
                if command.find(cmd) != -1:
                    self.__handle_events(EventTypes.MESSAGE, cmd, message)
                    return
        if self.default_message:
            self.default_message(self, message)

    def start(self, callback: Callable):
        self.start_command = callback

    def send_api_method(self, method: str, payload: dict):
        response = self.vk_session.method(method, payload)
        logger.debug(
            f"Sent api method '{method}'. "
            f"With payload {json.dumps(payload, ensure_ascii=False).encode('utf-8').decode()}. "
            f"Response: {json.dumps(response, ensure_ascii=False).encode('utf-8').decode()}"
        )

    def send_message(self, peer_id: int, text: str, keyboard: Union[str, Keyboard] = None):
        data = {
            "peer_id": peer_id,
            "message": text,
            "random_id": 0
        }
        if keyboard:
            if type(keyboard) == str:
                data['keyboard'] = keyboard
            else:
                data['keyboard'] = keyboard.get_keyboard()
        self.send_api_method("messages.send", data)

    def start_polling(self, callback: Callable = None):
        try:
            if callback is not None:
                callback()
            for event in self.longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    self.parse_message(event.message)
        except requests.exceptions.ReadTimeout as _ex:
            logger.error(_ex)
            self.start_polling()
        except vk_api.exceptions.ApiError as _ex:
            logger.error(_ex)
            self.start_polling()
