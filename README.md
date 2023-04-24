# PYVKBOT

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=black)

[![tests&build](https://img.shields.io/github/workflow/status/zeph1rrinc/pyvkbot/publish/master?label=release%26build&logo=github&logoColor=white)](https://github.com/zeph1rrinc/pyvkbot/actions)
[![LICENCE](https://img.shields.io/badge/License-MIT-yellow.svg?logo=ReadtheDocs&logoColor=white)](/LICENSE.md)
[![Version](https://img.shields.io/pypi/v/pyvkbot?logo=pypi&logoColor=white)](https://pypi.org/project/PyVkBot/)

## Installation

```
pip install pyvkbot
```

## Bot
### Methods
### init
Creating instance for future working

Params:
- token: str - access token of your group
- group_id: int - id of your group
- main_chat: int - [OPTIONAL] main chat for bot
- logging: bool - [OPTIONAL. DEFAULT: True] if True - logging in stdout by loguru.logger

Example:

```python
import os
from PyVkBot import Bot

token = os.getenv("TOKEN")

bot = Bot(token=token, main_chat=123, group_id=123123123, logging=False)
```

### delete_message
Deleting message from group chat, if author is not admin

Params:
- peer_id: int - id of chat where you want to delete messages
- cmidis: list - list of conversations ids of message, which you want to delete

Example:
```python
from PyVkBot import Bot

def delete_some_message(bot: Bot, message: dict):
    bot.delete_message(peer_id=message['peer_id'], cmids=[message['conversation_message_id']])
```

### on
Creating handler for events in longpoll listen

Params:
- event: str - Event type. You can take in from Types
- callback: Callable - function, which is executed, when event triggers
- trigger: str - trigger for event. Command for message or type of event for other (you can get it from Types)

Example:

```python
from PyVkBot import Types

def test_handler(bot, message):
  print(bot, message)

# triggers when user left or kicked from chat
bot.on(Types.EventTypes.ACTION, test_handler, Types.ActionTypes.CHAT_KICK_USER)
# triggers when user sent audio message
bot.on(Types.EventTypes.ATTACHMENT, test_handler, Types.AttachmentTypes.AUDIO_MESSAGE)
# triggers when user sent "hello"
bot.on(Types.EventTypes.MESSAGE, test_handler, "hello")
# triggers when user sent any test message
bot.on(Types.EventTypes.MESSAGE, test_handler)
```

### send_api_method
Sending some vk api method

Params:
- method: str - vk_api method. See [Docs](https://dev.vk.com/method?ref=tjournal.ru) for learn more
- payload: dict - dict of data to send in method

Example
```python
bot.send_api_method("messages.send", {"peer_id": 123, "text": "hi", "random_id":0})
```

### send_message
Sending message in chat

Params:
- peer_id: int - id of chat, where you want to send message
- text: str - text of message you wanted to send
- keyboard: Union[str, Keyboard] - [OPTIONAL] Keyboard for user, if needed. Takes Keyboard class or json string

Example:
```python
from PyVkBot.Keyboard import Keyboard

# Sends hi message to chat
bot.send_message(peer_id=123, text='hi')

# Send hello message to chat with keyboard
keyboard = Keyboard(inline=False)
keyboard.add_button(label="123")
bot.send_message(peer_id=123, text="hello", keyboard=keyboard)
# or
bot.send_message(peer_id=123, text="hello", keyboard=keyboard.get_keyboard())

# Send hello message to chat with removing keyboard
keyboard=Keyboard(inline=False).get_empty_keyboard()
bot.send_message(peer_id=123, text="hello", keyboard=keyboard)
```

### start
Creating handler for "start" button in private messages

Params:
- callback: Callable - function, which is executed, when button is pushed

Example:
```python
from PyVkBot import Bot

def start_command(bot: Bot, message: dict):
    bot.send_message(peer_id=message['peer_id'], text="Hello there!")

bot.start(start_command)
```

### start_polling
Starting polling messages from users

Params:
- callback: Callable - [OPTIONAL] Function, which would be executed, when bot is started

Example
```python
bot.start_polling()
bot.start_polling(lambda *_: print("BOT STARTED!"))
```

## Keyboard
Creating a vk keyboard

Params:
- one_time: bool - [OPTIONAL. DEFAULT: False] If true, keyboard closes when user pushes the buttons
- inline: bool - [OPTIONAL. DEFAULT: False] if ture, keyboard will be inline

Example:
```python
from PyVkBot.Keyboard import Keyboard

# Simple vk keyboard
simple_keyboard = Keyboard()

# Simple one time vk keyboard
one_time_keyboard = Keyboard(one_time=True)

# Inline vk keyboard
inline_keyboard = Keyboard(inline=True)
```

All keyboard methods you can see in [doc](https://vk-api.readthedocs.io/en/latest/keyboard.html). Callback methods are not implemented.
