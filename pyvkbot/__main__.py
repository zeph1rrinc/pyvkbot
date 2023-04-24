from .Bot import Bot
from . import Types

from loguru import logger
import os
import json

def get_user(bot: Bot, user_id: int) -> str | dict[str, str]:
    return bot.send_api_method("users.get", {"user_id": user_id})


def test_handler(bot, message):
    logger.debug(json.loads(json.dumps(get_user(bot, message['from_id']), ensure_ascii=False)))
    bot.send_message(peer_id=message['peer_id'], text=message['text'])



if __name__ == "__main__":
    bot = Bot(token=os.getenv('TEST_ACCESS_TOKEN'), group_id=os.getenv('TEST_GROUP_ID'))
    bot.on(Types.EventTypes.MESSAGE, test_handler)

    bot.start_polling()