import re
from telegram_users.models import Comment
from telepot.namedtuple import ReplyKeyboardMarkup

from bot.about_string import about_text

patterns = [
    "ثبت نظر",
    r"##entering_comment (.*)",
]

defualt_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بیخیال"}]], resize_keyboard=True)


def run(msg, user, matches, bot, ):
    print(msg["from"]["id"], "   ", msg["from"]["first_name"] if "first_name" in msg["from"] else "no_first_name",
          "   ", msg["from"]["username"] if "username" in msg["from"] else "no_username", "   ", msg["text"])

    if re.match("ثبت نظر", msg["text"]):
        bot.sendMessage(msg["from"]["id"],
                        "لطفا سوالات و پيشنهادات خود را براي ما ارسال نماييد تا در اولين فرصت به آن ترتيب اثر داده شود.",
                        reply_markup=defualt_keyboard)
        user.step = "entering_comment"
        user.save()

    if re.match("##entering_comment (.*)", msg["text"]):
        user.user_comment = matches[0]


        user.save()

        Comment.objects.create(owner=user, text=user.user_comment)

        return bot.sendMessage(msg["from"]["id"], 'از توجه شما سپاسگذاريم\n پيام شما توسط مديريت بررسي و در صورت نياز در اولين فرصت با شما تماس گرفته ميشود.', reply_markup=defualt_keyboard)


