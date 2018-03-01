import re
from telegram_users.models import Comment
from telepot.namedtuple import ReplyKeyboardMarkup

from bot.about_string import about_text

patterns = [
    "دریافت نظر",
    r"##select_action (.*)",
]

defualt_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بیخیال"},{"text": "پاک کردن همه نظرات"}]], resize_keyboard=True)


def run(msg, user, matches, bot, ):
    print(msg["from"]["id"], "   ", msg["from"]["first_name"] if "first_name" in msg["from"] else "no_first_name",
          "   ", msg["from"]["username"] if "username" in msg["from"] else "no_username", "   ", msg["text"])

    if re.match("دریافت نظر", msg["text"]):
        user.step = "select_action"
        user.save()
        q = Comment.objects.all()
        if len(q) == 0:
            return bot.sendMessage(msg["from"]["id"], "نظر جدید موجود نیست", reply_markup=defualt_keyboard)

        for q in q:
            q.text += "\n\nثبت کننده نظر : {}\n\n".format(q.get_comment_owner())
            bot.sendMessage(msg["from"]["id"], q.text, reply_markup=defualt_keyboard)

    if re.match("##select_action (.*)", msg["text"]):
        if matches[0] == "پاک کردن همه نظرات":
            Comment.objects.all().delete()

            user.save()
            return bot.sendMessage(msg["from"]["id"], 'نظرات پاک شد', reply_markup=defualt_keyboard)



