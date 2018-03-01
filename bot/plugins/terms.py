import re

from telepot.namedtuple import ReplyKeyboardMarkup

from bot.terms_string import terms_text

patterns = [
    "شرایط و قوانین🚫",
]

defualt_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بیخیال"}]], resize_keyboard=True)


def run(msg, user, matches, bot, ):
    print(msg["from"]["id"], "   ", msg["from"]["first_name"] if "first_name" in msg["from"] else "no_first_name",
          "   ", msg["from"]["username"] if "username" in msg["from"] else "no_username", "   ", msg["text"])

    if re.match("شرایط و قوانین🚫", msg["text"]):
        bot.sendMessage(msg["from"]["id"], terms_text["terms"], reply_markup=defualt_keyboard)
