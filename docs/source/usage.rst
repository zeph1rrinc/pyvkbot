Usage
=====

.. _installation:

Installation
------------

To use pyvkbot, first install it using pip:

.. code-block:: console

   (.venv) $ pip install pyvkbot

Creating bots
----------------

First of all you should get the api_key for you bot using the `oficial docs`: https://dev.vk.com/api/bots/getting-started

To create the bot, you can use the ``pyvkbot.Bot()`` class:

.. autoclass:: pyvkbot.Bot

The ``token`` and ``group_id`` parameter should be defined.
Otherwise, :py:class:`Bot` will raise an exception

.. autoexception:: TypeError
