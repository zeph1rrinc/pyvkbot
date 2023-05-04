import os

from pyvkbot import Bot
from pyvkbot import Keyboard

token = os.getenv("TOKEN")
group_id = os.getenv("GROUP_ID")

bot = Bot(token=token, group_id=group_id)


@bot.message("get keyboard")
def get_keyboard(bot: Bot, message: dict[str, str]):
    keyboard = Keyboard(inline=False)
    keyboard.add_button(label="123")
    bot.send_message(
        peer_id=message["peer_id"], text="Your keyboard", keyboard=keyboard
    )


@bot.message("remove keyboard")
def remove_keyboard(bot: Bot, message: dict[str, str]):
    keyboard = Keyboard(inline=False).get_empty_keyboard()
    bot.send_message(
        peer_id=message["peer_id"], text="Keyboard removed", keyboard=keyboard
    )


bot.start_polling()
