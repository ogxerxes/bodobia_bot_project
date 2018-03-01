import importlib
import re
from pprint import pprint

from django.core.exceptions import ObjectDoesNotExist
from telepot import Bot

from bodobia import settings
from telegram_users.models import TelegramUser

plugins = []


def load_plugs():
    for x in settings.BOT_PLUGINS:
        module_name = 'bot.plugins' + '.' + x
        # try:
        plugins.append(importlib.import_module(module_name))
        print("Plugin " + x + " loaded")
        # except:
        #     print("Loading plugin " + x + " failed")


def check_user(user):
    #  TODO: name
    try:
        user = TelegramUser.objects.get(telegram_id=user["id"])
        user.messages += 1
        user.save()
    except ObjectDoesNotExist:
        user = TelegramUser.objects.create(telegram_id=user["id"], name=user["first_name"] if "first_name" in user else None,
                                           username=user["username"] if "username" in user else None, )
    return user


load_plugs()


def handle(msg):
    if "text" not in msg and not "photo" in msg:
        return False
    if "photo" in msg:
        msg["photo_file_id"] = msg["photo"][-1]["file_id"]
        msg["text"] = "<img>"
    user = check_user(msg["from"])
    bot = user.bot
    if msg["text"] == "بیخیال":
        user.step = None
        user.save()
        msg["text"] = "/start"
    if user.step:
        msg["text"] = "##{} {}".format(user.step, msg["text"])
        # if "callback" in msg:
        # msg["text"] = "&&{} {}".format(user.step, msg["data"])
    for plugin in plugins:
        for k in plugin.patterns:
            if re.match(k, msg["text"]):
                print("Trigerred")
                matches = list(re.match(k, msg["text"]).groups())

                plugin.run(msg, user, matches, bot)
                #  res = threading.Thread(target=plugin.run, args=(msg, matches))
                #  res.start()
