# -*- coding: UTF-8 -*-
from erina import Bot
from modules import handlers

credentials = {
    "user": "",
    "passw": ""
}

bot = Bot(credentials)

for handler in handlers:
    bot.addHandler(handler)

bot.listen()
