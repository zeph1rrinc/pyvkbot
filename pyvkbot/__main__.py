import json
import os

from loguru import logger

from .Bot import Bot

bot = Bot(token=os.getenv("TEST_ACCESS_TOKEN"), group_id=os.getenv("TEST_GROUP_ID"))


def get_user(bot: Bot, user_id: int) -> str | dict[str, str]:
    return bot.send_api_method("users.get", {"user_id": user_id})


@bot.attachment("audio_message")
def audio_message(bot, message):
    user_data = json.loads(
        json.dumps(get_user(bot, message["from_id"]), ensure_ascii=False)
    )
    print(user_data)
    bot.send_message(
        peer_id=message["peer_id"],
        text=f'{user_data[0]["first_name"]} {user_data[0]["last_name"]} i can\'t listen',
    )


@bot.message("Привет")
def test_handler(bot, message):
    logger.debug(
        json.loads(json.dumps(get_user(bot, message["from_id"]), ensure_ascii=False))
    )
    bot.send_message(peer_id=message["peer_id"], text=message["text"])


if __name__ == "__main__":
    bot.start_polling()
