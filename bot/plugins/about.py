import re

from telepot.namedtuple import ReplyKeyboardMarkup

from bot.about_string import about_text

patterns = [
    "درباره ما📖",
]

defualt_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بیخیال"}]], resize_keyboard=True)


def run(msg, user, matches, bot, ):
    print(msg["from"]["id"], "   ", msg["from"]["first_name"] if "first_name" in msg["from"] else "no_first_name",
          "   ", msg["from"]["username"] if "username" in msg["from"] else "no_username", "   ", msg["text"])

    if re.match("درباره ما📖", msg["text"]):
        bot.sendMessage(msg["from"]["id"], about_text["about"], reply_markup=defualt_keyboard)
