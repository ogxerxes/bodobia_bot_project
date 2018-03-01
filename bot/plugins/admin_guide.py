import re
from telegram_users.models import TelegramUser
from bot.admin_help_string import admin_string
from telepot.namedtuple import ReplyKeyboardMarkup

patterns = [
    "راهنمای ادمین📕",
]

defualt_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بیخیال"}]], resize_keyboard=True)


def run(msg, user, matches, bot, ):
    print(msg["from"]["id"], "   ", msg["from"]["first_name"] if "first_name" in msg["from"] else "no_first_name",
          "   ", msg["from"]["username"] if "username" in msg["from"] else "no_username", "   ", msg["text"])

    if re.match("راهنمای ادمین📕", msg["text"]):
        if user.is_admin:
            bot.sendMessage(msg["from"]["id"], admin_string["admin_help"], reply_markup=defualt_keyboard)
