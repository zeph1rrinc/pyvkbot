import os

from pyvkbot import Bot

token = os.getenv("TOKEN")
group_id = os.getenv("GROUP_ID")

bot = Bot(token=token, group_id=group_id)


def get_user(bot: Bot, user_id: int) -> str | dict[str, str]:
    return bot.send_api_method("users.get", {"user_id": user_id})


@bot.action("chat_invite_user")
def hello(bot: Bot, message: dict[str, str]):
    new_user = get_user(bot, message["action"]["member_id"])[0]
    bot.send_message(message["peer_id"], text=f"hello {new_user['first_name']}")


@bot.attachment("audio_message")
def delete_audio_message(bot: Bot, message: dict["str", "str"]):
    bot.delete_message(message["peer_id"], cmids=[message["conversation_message_id"]])
    bot.send_message(message["peer_id"], text="Audio message are not allowed")


bot.start_polling()
