import re

from bot.plugins.add import no_room_houses
from bot.st import strings
from houses.models import House
from telepot.namedtuple import ReplyKeyboardMarkup
from telegram_users.models import TelegramUser

patterns = [
    "جست و جو🔎",
    r"##search_house_type (.*)",
    r"##search_house_deal (.*)",
    r"##search_house_city (.*)",
    r"##searching (.*)",

]

defualt_keyboard = ReplyKeyboardMarkup(keyboard=[

    [{"text": "بیخیال"}]], resize_keyboard=True)

search_keyboard = ReplyKeyboardMarkup(keyboard=[

    [{"text": "نتیجه بعدی"}, {"text": "نتیجه قبلی"}],
    [{"text": "بیخیال"}],
])

house_type_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "ویلا"}, {"text": "آ‍‍پارتمان"}, ],
    [{"text": "خانه"}, {"text": "باغ"}],
    [{"text": "زمین"}, {"text": "مغازه"}],
    [{"text": "دفتر کار"}, {"text": "سایر املاک"}],
    [{"text": "بیخیال"}],
], resize_keyboard=True)

city_choice_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "#شهسوار"}, {"text": "#خرم #آباد"}],
    [{"text": "#عباس #آباد"}, {"text": "#نشتارود"}],
    [{"text": "#متل #قو"}, {"text": "#کلاردشت"}],
    [{"text": "#شیرود"}, {"text": "#نمک #آبرود"}],
    [{"text": "#سایر #شهر ها"}, {"text": "بیخیال"}],

], resize_keyboard=True)
deal_type_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "خرید"}, {"text": "رهن و اجاره"}, {"text": "بیخیال"}],
], resize_keyboard=True)

allowed_house_types = {"خانه", "زمین", "مغازه", "آ‍‍پارتمان", "ویلا", "دفتر کار", "باغ", "سایر املاک", }

allowed_house_deals = {"رهن و اجاره", "خرید", }

allowed_add_house_city = {"#شهسوار", "#نشتارود", "#عباس #آباد", "#متل #قو", "#شیرود", "#کلاردشت", "#نمک #آبرود",
                          "#خرم #آباد",
                          "#سایر #شهر ها"}




def run(msg, user, matches, bot):
    print(msg["from"]["id"], "   ", msg["from"]["first_name"] if "first_name" in msg["from"] else "no_first_name",
          "   ", msg["from"]["username"] if "username" in msg["from"] else "no_username", "   ", msg["text"])

    if re.match("جست و جو🔎", msg["text"]):
        user.step = "search_house_type"
        user.save()
        return bot.sendMessage(msg["from"]["id"], "بدو بيا از ليست پايين ملكت رو انتخاب كن!", reply_markup=house_type_keyboard)

    if re.match("##search_house_type (.*)", msg["text"]):
        if not matches[0] in allowed_house_types:
            user.step = "search_house_type"
            bot.sendMessage(msg["from"]["id"], "بدو بيا از ليست پايين ملكت رو انتخاب كن!", reply_markup=house_type_keyboard)
        else:
            user.step = "search_house_deal"
            user.search_house_type = matches[0]
            user.save()
            return bot.sendMessage(msg["from"]["id"], "دنبال اجاره ميگردي يا خريد؟", reply_markup=deal_type_keyboard)

    if re.match("##search_house_deal (.*)", msg["text"]):
        if not matches[0] in allowed_house_deals:
            user.step = "search_house_type"
            bot.sendMessage(msg["from"]["id"], "دنبال اجاره ميگردي يا خريد؟", reply_markup=deal_type_keyboard)
        else:
            if matches[0] == "خرید":
                user.step = "search_house_city"
                user.search_house_deal = "فروش"
                user.save()
                return bot.sendMessage(msg["from"]["id"], "شهرت رو انتخاب كن تا بگم چي دارم واست!",
                                       reply_markup=city_choice_keyboard)
            else:
                user.step = "search_house_city"
                user.search_house_deal = matches[0]
                user.save()
                return bot.sendMessage(msg["from"]["id"], "شهرت رو انتخاب كن تا بگم چي دارم واست!",
                                       reply_markup=city_choice_keyboard)



    if re.match("##search_house_city (.*)", msg["text"]):
        if not matches[0] in allowed_add_house_city:
            bot.sendMessage(msg["from"]["id"], "شهرت رو انتخاب كن تا بگم چي دارم واست!", reply_markup=city_choice_keyboard)
        else:
            user.search_house_city = matches[0]
            user.res_number = 0
            user.step = "searching"
            user.save()
            q = House.objects.filter(house_type=user.search_house_type, house_deal=user.search_house_deal,
                                     house_city=user.search_house_city, hidden=False).order_by('-date_time')
            if len(q) < 1:
                user.step = None
                # stepesho bokon none ke bere menu asli
                user.save()
                return bot.sendMessage(msg["from"]["id"], "نتیجه ای یافت نشد", reply_markup=defualt_keyboard)
            else:
                if len(q) == 1:
                    user.res_number = 0
                    h = q[user.res_number]
                    return_text = "کل نتایج : {} \n".format(len(q))
                    return_text += "نتیجه شماره : {} \n\n".format(user.res_number + 1)
                    return_text += "ثبت کننده آگهی: {}\n".format(h.get_house_owner())
                    return_text += "تاریخ ثبت: {}\n".format(h.date_created)
                    return_text += "\n اطلاعات تماس: {}".format(h.house_contact_info)
                    return_text += "\n شهر : #{}".format(h.house_city)
                    return_text += "\n نوع ملک : {}".format(h.house_type)
                    return_text += "\n آدرس ملک: {}".format(h.house_address)
                    return_text += "\n متراژ: {} متر مربع".format(h.house_surface)
                    return_text += "\n نوع معامله: {}".format(h.house_deal)

                    if h.house_deal == "رهن و اجاره":

                        return_text += "\n میزان ودیعه :{} میلیون تومان".format(h.house_pre_price)
                        return_text += "\n قیمت اجاره ماهیانه: {}تومان".format(h.house_price)
                        return_text += "\n مدت زمان تقريبي اجاره: {}".format(h.house_ejare_time)

                    else:
                        return_text += "\n قیمت کل ملک: {} میلیون تومان".format(h.house_price)
                        if h.house_swap == "بدم نمیاد":
                            return_text += "\nمالک تمایل خود را برای معاوضه ملک با خودرو یا ملک دیگری اعلام میکند.\n"

                    if h.house_type not in no_room_houses:
                        return_text += "\n تعداد اتاق: {}".format(h.house_rooms)
                        return_text += "\n امکانات ملک: {}".format(h.house_options)

                    return_text += "\n اطلاعات اضافی: {}\n\n".format(h.house_extra_info)
                    return_text += "\n لطفا لينك بدوبيا رو به دوستانتون در گروه هاي مختلف معرفي كنيد.به اميد خانه دار شدن همه!@bodobia_bot"
                    return_text += "\n Image File ID: {}".format(h.house_file_id)

                    ##TODO: tedade kole nataiejam ezafe kon mishe len(q) dige ia bala bezar natije folan az folan mesalan 1/10
                    bot.sendMessage(msg["from"]["id"], return_text, reply_markup=defualt_keyboard)
                    if not h.house_file_id == "null":
                        bot.sendPhoto(msg["from"]["id"], h.house_file_id, reply_markup=defualt_keyboard)

                if len(q) > 1:
                    user.step = "searching"

                    user.res_number = 0
                    user.save()
                    h = q[user.res_number]
                    return_text = "کل نتایج : {} \n".format(len(q))
                    return_text += "نتیجه شماره : {} \n\n".format(user.res_number + 1)
                    return_text += "ثبت کننده آگهی: {}\n".format(h.get_house_owner())
                    return_text += "تاریخ ثبت: {}\n".format(h.date_created)
                    return_text += "\n اطلاعات تماس: {}".format(h.house_contact_info)
                    return_text += "\n شهر : #{}".format(h.house_city)
                    return_text += "\n نوع ملک : {}".format(h.house_type)
                    return_text += "\n آدرس ملک: {}".format(h.house_address)
                    return_text += "\n متراژ: {} متر مربع".format(h.house_surface)
                    return_text += "\n نوع معامله: {}".format(h.house_deal)

                    if h.house_deal == "رهن و اجاره":

                        return_text += "\n میزان ودیعه :{} میلیون تومان".format(h.house_pre_price)
                        return_text += "\n قیمت اجاره ماهیانه: {}تومان".format(h.house_price)
                        return_text += "\n مدت زمان تقريبي اجاره: {}".format(h.house_ejare_time)

                    else:
                        return_text += "\n قیمت کل ملک: {} میلیون تومان".format(h.house_price)
                        if h.house_swap == "بدم نمیاد":
                            return_text += "\nمالک تمایل خود را برای معاوضه ملک با خودرو یا ملک دیگری اعلام میکند.\n"

                    if h.house_type not in no_room_houses:
                        return_text += "\n تعداد اتاق: {}".format(h.house_rooms)
                        return_text += "\n امکانات ملک: {}".format(h.house_options)

                    return_text += "\n اطلاعات اضافی: {}\n\n".format(h.house_extra_info)
                    return_text += "\n لطفا لينك بدوبيا رو به دوستانتون در گروه هاي مختلف معرفي كنيد.به اميد خانه دار شدن همه!@bodobia_bot"
                    return_text += "\n Image File ID: {}".format(h.house_file_id)
                    ##TODO: tedade kole nataiejam ezafe kon mishe len(q) dige ia bala bezar natije folan az folan mesalan 1/10
                    bot.sendMessage(msg["from"]["id"], return_text, reply_markup=search_keyboard)
                    if not h.house_file_id == "null":
                        bot.sendPhoto(msg["from"]["id"], h.house_file_id, reply_markup=search_keyboard)

    if re.match("##searching (.*)", msg["text"]):
        # TODO: handle unknown charachters like string in this place. just do nothin if is now allowed
        if matches[0] == "نتیجه بعدی":
            user.res_number += 1
            user.step = "searching"
            user.save()
        else:
            if matches[0] == "نتیجه قبلی":
                user.res_number -= 1
                user.step = "searching"
                user.save()

        q = House.objects.filter(house_type=user.search_house_type, house_deal=user.search_house_deal,
                                 house_city=user.search_house_city, hidden=False).order_by('-date_time')
        if len(q) > 1:
            try:
                h = q[user.res_number]
                return_text = "کل نتایج : {} \n".format(len(q))
                return_text += "نتیجه شماره : {} \n\n".format(user.res_number + 1)
                return_text += "ثبت کننده آگهی: {}\n".format(h.get_house_owner())
                return_text += "تاریخ ثبت: {}\n".format(h.date_created)
                return_text += "\n اطلاعات تماس: {}".format(h.house_contact_info)
                return_text += "\n شهر : #{}".format(h.house_city)
                return_text += "\n نوع ملک : {}".format(h.house_type)
                return_text += "\n آدرس ملک: {}".format(h.house_address)
                return_text += "\n متراژ: {} متر مربع".format(h.house_surface)
                return_text += "\n نوع معامله: {}".format(h.house_deal)

                if h.house_deal == "رهن و اجاره":

                    return_text += "\n میزان ودیعه :{} میلیون تومان".format(h.house_pre_price)
                    return_text += "\n قیمت اجاره ماهیانه: {}تومان".format(h.house_price)
                    return_text += "\n مدت زمان تقريبي اجاره: {}".format(h.house_ejare_time)

                else:
                    return_text += "\n قیمت کل ملک: {} میلیون تومان".format(h.house_price)
                    if h.house_swap == "بدم نمیاد":
                        return_text += "\nمالک تمایل خود را برای معاوضه ملک با خودرو یا ملک دیگری اعلام میکند.\n"

                if h.house_type not in no_room_houses:
                    return_text += "\n تعداد اتاق: {}".format(h.house_rooms)
                    return_text += "\n امکانات ملک: {}".format(h.house_options)

                return_text += "\n اطلاعات اضافی: {}\n\n".format(h.house_extra_info)
                return_text += "\n لطفا لينك بدوبيا رو به دوستانتون در گروه هاي مختلف معرفي كنيد.به اميد خانه دار شدن همه!@bodobia_bot"
                return_text += "\n Image File ID: {}".format(h.house_file_id)
                bot.sendMessage(msg["from"]["id"], return_text, reply_markup=search_keyboard)
                if not h.house_file_id == "null":
                    bot.sendPhoto(msg["from"]["id"], h.house_file_id, reply_markup=search_keyboard)

            except (IndexError, AssertionError):

                user.step = None
                user.save()
                return bot.sendMessage(msg["from"]["id"], "پایان نتایج -برای بازگشت <بیخیال> رو بزن",
                                       reply_markup=defualt_keyboard)


