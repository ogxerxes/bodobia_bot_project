import re
from telepot.namedtuple import ReplyKeyboardMarkup

from houses.models import House

patterns = [
    "آگهی های فروش اختصاصی بدوبیا💰",
    r"##all_sell_search (.*)",
]

defualt_keyboard = ReplyKeyboardMarkup(keyboard=[

    [{"text": "بیخیال"}]], resize_keyboard=True)

search_keyboard = ReplyKeyboardMarkup(keyboard=[

    [{"text": "نتیجه بعدی"}, {"text": "نتیجه قبلی"}],
    [{"text": "بیخیال"}],
])

no_room_houses = {"باغ", "زمین", }

def run(msg, user, matches, bot):  # start adding house
    print(msg["from"]["id"], "   ", msg["from"]["first_name"] if "first_name" in msg["from"] else "no_first_name",
          "   ", msg["from"]["username"] if "username" in msg["from"] else "no_username", "   ", msg["text"])


    if re.match("آگهی های فروش اختصاصی بدوبیا💰", msg["text"]):
        user.set_step("all_sell_search")
        user.save()
        user.res_number = 0
        user.save()
        q = House.objects.filter(house_deal="فروش", owner__is_admin=True,
                                 hidden=False).order_by('-date_time')
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
                bot.sendMessage(msg["from"]["id"], return_text, reply_markup=search_keyboard)
                if not h.house_file_id == "null":
                    bot.sendPhoto(msg["from"]["id"], h.house_file_id, reply_markup=search_keyboard)



                    # TODO: handle unknown charachters like string in this place. just do nothin if is now allowed
    if re.match("##all_sell_search (.*)", msg["text"]):

        if matches[0] == "نتیجه بعدی":
            user.res_number += 1
            user.step = "all_sell_search"
            user.save()
        else:
            if matches[0] == "نتیجه قبلی":
                user.res_number -= 1
                user.step = "all_sell_search"
                user.save()

        q = House.objects.filter(house_deal="فروش",owner__is_admin=True,
                                 hidden=False).order_by('-date_time')

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

                bot.sendMessage(msg["from"]["id"], "پایان نتایج -برای بازگشت <بیخیال> رو بزن",
                                reply_markup=defualt_keyboard)
