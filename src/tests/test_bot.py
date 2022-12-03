import json
import os

import pytest
import requests
import vk_api

from .test_fixtures import prepare_events
from PyVkBot import Bot, Types, Exceptions, Keyboard


token = os.getenv('TEST_ACCESS_TOKEN')
group_id = int(os.getenv('TEST_GROUP_ID'))

bot = Bot(
    token=token,
    group_id=group_id,
    logging=False
)


def test_on_ok():
    bot.on(Types.EventTypes.MESSAGE, lambda _, message: 13)
    assert bot.default_message(None, None) == 13
    bot.on(Types.EventTypes.MESSAGE, lambda _, message: 14, "go")
    assert bot.events[Types.EventTypes.MESSAGE].get('go')(None, None) == 14
    bot.on(Types.EventTypes.ACTION, lambda _, message: 13, Types.ActionTypes.CHAT_KICK_USER)
    assert bot.events[Types.EventTypes.ACTION].get(Types.ActionTypes.CHAT_KICK_USER)(None, None) == 13
    bot.on(Types.EventTypes.ATTACHMENT, lambda _, message: 13, Types.AttachmentTypes.VIDEO)
    assert bot.events[Types.EventTypes.ATTACHMENT].get(Types.AttachmentTypes.VIDEO)(None, None) == 13


def test_on_duplicate_rises():
    with pytest.raises(Exceptions.DuplicateTriggerError):
        bot.on(Types.EventTypes.MESSAGE, lambda _, message: 15, "run")
        bot.on(Types.EventTypes.MESSAGE, lambda _, message: 14, "run")


def test_on_unexpected_raises():
    with pytest.raises(Exceptions.UnexpectedTriggerError):
        bot.on(Types.EventTypes.ACTION, lambda _, message: 123, "123")


def test_on_raises_not_available_action():
    with pytest.raises(Exceptions.NotAvailableEventError):
        bot.on("312312", lambda _, message: 13)


def test_on_validating_events():
    with pytest.raises(Exceptions.UnexpectedTriggerError):
        bot.on(Types.EventTypes.ACTION, lambda _, message: 13)


def test_start_ok():
    start_command = bot.start_command
    bot.start(lambda _, message: 13)
    assert bot.start_command is not start_command
    assert bot.start_command(None, None) == 13


def test_send_api_method_ok(monkeypatch):
    monkeypatch.setattr('vk_api.VkApi.method', lambda *_: 'mother')
    bot.send_api_method("messages.send", {"peer_id": 123, "message": '123', "random_id": 0})
    bot.send_message(123, '123')
    bot.delete_message(123, [123])


def test_parse_message_default_message_ok():
    message = {
        "peer_id": 13,
        "text": "hello",
    }
    bot.parse_message(message)


def test_parse_message_action_ok():
    message = {
        "peer_id": 13,
        "action": {'type': Types.ActionTypes.CHAT_KICK_USER},
        "text": ''
    }
    bot.parse_message(message)


def test_parse_message_payload_ok():
    message = {
        "peer_id": 13,
        "payload": json.dumps({'command': 'start'}),
        "text": ''
    }
    bot.parse_message(message)


def test_parse_message_attachments_ok():
    message = {
        "peer_id": 13,
        "attachments": [{'type': Types.AttachmentTypes.VIDEO}],
        "text": ''
    }
    bot.parse_message(message)


def test_parse_message_command_ok():
    message = {
        "peer_id": 13,
        "attachments": [],
        "text": 'go'
    }
    bot.parse_message(message)


def test_start_polling_ok(prepare_events):
    bot.start_polling(lambda *_: _)


def test_handling_requests_error(prepare_events):
    def raise_requests_error():
        raise requests.exceptions.ReadTimeout

    bot.start_polling(raise_requests_error)


def test_handling_vkapi_error(prepare_events):
    def raise_vkapi_error():
        raise vk_api.exceptions.ApiError(bot.vk_session, "messages.send", '123', '123',
                                         {"error_code": 123, "error_msg": "321"})

    bot.start_polling(raise_vkapi_error)


@pytest.mark.parametrize("keyboard",
                         [
                             Keyboard(inline=False),
                             Keyboard(inline=True)
                         ])
def test_send_message_with_keyboard(keyboard, monkeypatch):
    monkeypatch.setattr('vk_api.VkApi.method', lambda *_: 'mother')
    keyboard.add_button(label="123")
    bot.send_message(peer_id=123, text="hello", keyboard=keyboard)
    bot.send_message(peer_id=123, text="hello", keyboard=keyboard.get_keyboard())
    bot.send_message(peer_id=123, text='removed', keyboard=keyboard.get_empty_keyboard())

