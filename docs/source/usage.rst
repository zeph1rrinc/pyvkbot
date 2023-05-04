Usage
=====

.. _installation:

Creating bots
----------------

First of all you should get the api_key for you bot using the `oficial docs`: https://dev.vk.com/api/bots/getting-started

To create the bot, you can use the ``pyvkbot.Bot()`` class:

.. autoclass:: pyvkbot.Bot

The ``token`` and ``group_id`` parameter should be defined.
Otherwise, :py:class:`Bot` will raise an exception

Getting started
----------------

Create the bot

    .. code-block:: Python

        import os

        from pyvkbot import Bot

        token = os.getenv("TOKEN")
        group_id = os.getenv("GROUP_ID")

        bot = Bot(token=token, group_id=group_id)

Bind the commands

      .. code-block:: Python

          @bot.message("Start")
           def hello(bot: Bot, message: dict[str, str]):
               bot.send_message(peer_id=message["peer_id"], text="Hello there!")


          @bot.message()
          def default(bot: Bot, message: dict[str, str]):
              bot.send_message(peer_id=message["peer_id"], text="Sorry, i don't understand you")

Start the bot

      .. code-block:: Python

          bot.start_polling(lambda: print("Bot started"))

Enjoy your bot!

Bot examples you can see on https://github.com/zeph1rrinc/pyvkbot/tree/master/examples
