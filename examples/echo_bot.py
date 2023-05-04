import os

from pyvkbot import Bot

token = os.getenv("TOKEN")
group_id = os.getenv("GROUP_ID")

bot = Bot(token=token, group_id=group_id)


@bot.message()
def echo(bot: Bot, message: dict[str, str]):
    bot.send_message(peer_id=message["peer_id"], text=message["text"])


bot.start_polling(lambda: print("Bot started"))
