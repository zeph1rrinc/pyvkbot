import os

from pyvkbot import Bot

token = os.getenv("TOKEN")
group_id = os.getenv("GROUP_ID")

bot = Bot(token=token, group_id=group_id)


def get_user(bot: Bot, user_id: int) -> str | dict[str, str]:
    return bot.send_api_method("users.get", {"user_id": user_id})


@bot.message("Hello")
def hello(bot: Bot, message: dict[str, str]):
    user_data = get_user(bot, message["peer_id"])[0]
    bot.send_message(
        message["peer_id"], f"Hello, {user_data['first_name']} {user_data['last_name']}"
    )


bot.start_polling()
