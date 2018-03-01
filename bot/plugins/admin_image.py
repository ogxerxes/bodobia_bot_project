import re

from telepot.namedtuple import ReplyKeyboardMarkup

patterns = [
    r"^<img>",
]

defualt_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بیخیال"}]], resize_keyboard=True)


def run(msg, user, matches, bot, ):
    print(msg, user, matches, bot)
    if re.match(r"^<img>", msg["text"]):
        if msg["text"] == "<img>":
            if user.is_admin:
                return_text = "\n\n Image File ID: {}".format(msg["photo_file_id"])
                user.step = None
                return bot.sendMessage(msg["from"]["id"], return_text, reply_markup=defualt_keyboard)

            else:
                user.step = None
                return bot.sendMessage(msg["from"]["id"], "شما ادمین نیستید", reply_markup=defualt_keyboard)
