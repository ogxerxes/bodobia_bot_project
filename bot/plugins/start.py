import re
from bot.st import strings

from telepot.namedtuple import ReplyKeyboardMarkup

patterns = [
    r"^[#/!]([Ss][Tt][Aa][Rr][Tt])$",

]
from telegram_users.models import TelegramUser

defualt = [
    [{"text": "جست و جو🔎"},],[{"text": "اضافه کردن ملک➕🏠"}, ],

    [{"text": "شرایط و قوانین🚫"},{"text": "درباره ما📖"}, {"text": "ثبت نظر"}],

]
admin = [
    [{"text": "جست و جو🔎"}, {"text": "اضافه کردن ملک➕🏠"}],
    [{"text": "آگهی های اجاره اختصاصی بدوبیا⏳"}, {"text": "آگهی های فروش اختصاصی بدوبیا💰"}],
    [{"text": "راهنمای ادمین📕"}, {"text": "شرایط و قوانین🚫"}],
    [{"text": "حذف املاک ثبت شده❌"}, {"text": "تایید املاک جدید✅"}, ],
    [{"text": "درباره ما📖"}, {"text": "دریافت نظر"}],

]
d_keyboard = ReplyKeyboardMarkup(keyboard=defualt, resize_keyboard=True)
admin_keyboard = ReplyKeyboardMarkup(keyboard=admin, resize_keyboard=True)


def run(msg, user, matches, bot, ):
    print(msg["from"]["id"], "   ", msg["from"]["first_name"] if "first_name" in msg["from"] else "no_first_name",
          "   ", msg["from"]["username"] if "username" in msg["from"] else "no_username", "   ", msg["text"])

    if re.match(r"^[#/!]([Ss][Tt][Aa][Rr][Tt])$", msg["text"]):
        if user.is_admin:
            bot.sendMessage(msg["from"]["id"], strings["welcome"], reply_markup=admin_keyboard)
            return bot.sendMessage(msg["from"]["id"],
                                   "خوش آمدید. شما ادمین هستید.\n لطفا یکی از گزینه ها را انتخاب کنید.",
                                   reply_markup=admin_keyboard)
        else:

            return bot.sendMessage(msg["from"]["id"], strings["welcome"], reply_markup=d_keyboard)
