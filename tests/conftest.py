import pytest
from vk_api.bot_longpoll import VkBotEventType


@pytest.fixture()
def prepare_events(monkeypatch):
    event = type("test_event", (), dict())
    test_event = event()
    test_event.type = VkBotEventType.MESSAGE_NEW
    test_event.message = {
        "peer_id": 13,
        "attachments": [],
        "text": 'go'
    }
    test_event2 = event()
    test_event2.type = VkBotEventType.MESSAGE_NEW
    test_event2.message = {
        "peer_id": 13,
        "action": {'type': '123'},
        "text": ''
    }
    monkeypatch.setattr('vk_api.bot_longpoll.VkBotLongPoll.listen', lambda *_: [test_event, test_event2])
