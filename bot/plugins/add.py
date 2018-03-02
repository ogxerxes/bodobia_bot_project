import re
from bot.st import strings
from datetime import datetime
from houses.models import House
from telepot.namedtuple import ReplyKeyboardMarkup
from telegram_users.models import TelegramUser

patterns = [
    "اضافه کردن ملک➕🏠",
    r"##add_house_type (.*)",
    r"##add_deal_type (.*)",
    r"##add_house_pre_price (.*)",
    r"##add_house_ejare_time (.*)",
    r"##add_house_rooms (.*)",
    r"##add_house_surface (.*)",
    r"##add_house_swap (.*)",
    r"##add_house_price (.*)",
    r"##add_house_city (.*)",
    r"##add_house_address (.*)",
    r"##add_house_options (.*)",
    r"##add_house_contact_info (.*)",
    r"##add_house_extra_info (.*)",
    r"##add_house_file_id (.*)",
    r"##create_house (.*)",

]

house_type_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "ویلا"}, {"text": "آ‍‍پارتمان"}, ],
    [{"text": "خانه"}, {"text": "باغ"}],
    [{"text": "زمین"}, {"text": "مغازه"}],
    [{"text": "دفتر کار"}, {"text": "سایر املاک"}],
    [{"text": "بیخیال"}],
], resize_keyboard=True)

deal_type_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بیخیال"}, {"text": "رهن و اجاره"}, {"text": "فروش"}],
], resize_keyboard=True)

yes_no_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بیخیال"}, {"text": "بله مطمئنم!"}]], resize_keyboard=True)

room_number_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "دو اتاق"}, {"text": "یک اتاق"}],
    [{"text": "چهار اتاق"}, {"text": "سه اتاق"}],
    [{"text": "ندارد"}, {"text": "بیش از چهار اتاق"}],
    [{"text": "بیخیال"}],
], resize_keyboard=True)
city_choice_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "#شهسوار"}, {"text": "#خرم #آباد"}],
    [{"text": "#عباس #آباد"}, {"text": "#نشتارود"}],
    [{"text": "#متل #قو"}, {"text": "#کلاردشت"}],
    [{"text": "#شیرود"}, {"text": "#نمک #آبرود"}],
    [{"text": "#سایر #شهر ها"}, {"text": "بیخیال"}],

], resize_keyboard=True)

options_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "مبله"}, {"text": "آسانسور"}],
    [{"text": "مجاز به نگهداری حیوانات خانگی"}, {"text": "انباری"}],
    [{"text": "سرویس فرنگی"}, {"text": "تراس"}],
    [{"text": "شوتینگ"}, {"text": "کولر"}],
    [{"text": "پارکینگ"}, {"text": "درب ریموت دار"}],
    [{"text": "<اتمام>"}, {"text": "مشاهده لیست امکانات"}],
    [{"text": "بیخیال"}, ]

], resize_keyboard=True)

extra_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بیخیال"}, {"text": "در تماس تلفنی اعلام میکنم"}]], resize_keyboard=True)

ejare_time_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "اجاره کوتاه مدت"}, {"text": "اجاره یکساله"}],
    [{"text": "بیخیال"}, ]
], resize_keyboard=True)

empty_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بیخیال"}, {"text": "ندارد"}]], resize_keyboard=True)

swap_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بدم نمیاد"}, {"text": "فعلا ندارم"}]], resize_keyboard=True)

defualt_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بیخیال"}]], resize_keyboard=True)

image_keyboard = ReplyKeyboardMarkup(keyboard=[
    [{"text": "بیخیال"}, {"text": "الان عکسی ندارم"}]], resize_keyboard=True)

allowed_add_house_types = {"خانه", "زمین", "مغازه", "آ‍‍پارتمان", "ویلا", "دفتر کار", "باغ", "سایر املاک", }

allowed_add_house_deals = {"رهن و اجاره", "فروش", }

allowed_add_house_rooms = {"یک اتاق", "سه اتاق", "چهار اتاق", "ندارد", "بیش از چهار اتاق", "دو اتاق"}

allowed_add_house_city = {"#شهسوار", "#نشتارود", "#عباس #آباد", "#متل #قو", "#شیرود", "#کلاردشت", "#نمک #آبرود",
                          "#خرم #آباد",
                          "#سایر #شهر ها"}

allowed_add_house_options = {"مجاز به نگهداری حیوانات خانگی", "آسانسور", "مبله", "انباری", "سرویس فرنگی", "تراس",
                             "شوتینگ"
    , "کولر", "پارکینگ", "درب ریموت دار", }

allowed_ejare_time = {"اجاره یکساله", "اجاره کوتاه مدت"}

no_room_houses = {"باغ", "زمین", }

maximum_house_price = 50000000
minimum_house_price = 0
maximum_house_surface = 200000
minimum_house_surface = 20


def run(msg, user, matches, bot):  # start adding house
    print("[" ,str(datetime.now()) + "]" , "   " ,msg["from"]["id"], "   ", msg["from"]["first_name"] if "first_name" in msg["from"] else "no_first_name",
          "   ", msg["from"]["username"] if "username" in msg["from"] else "no_username", "   ", msg["text"])


    if re.match("اضافه کردن ملک➕🏠", msg["text"]):
        user.set_step("add_house_type")
        return bot.sendMessage(msg["from"]["id"], "حالا نوبت ملک شماست انتخابش کن!", reply_markup=house_type_keyboard)

    if re.match("##add_house_type (.*)", msg["text"]):

        if not matches[0] in allowed_add_house_types:

            user.step = "add_house_type"
            bot.sendMessage(msg["from"]["id"], "حالا نوبت ملک شماست انتخابش کن!", reply_markup=house_type_keyboard)

        else:
            if not matches[0] in no_room_houses:
                user.step = "add_deal_type"
                user.add_house_type = matches[0]
                user.save()
                return bot.sendMessage(msg["from"]["id"], "نوع معامله ! \nمیخوای اجاره بدی یا بفروشی؟",
                                       reply_markup=deal_type_keyboard)
            else:
                user.step = "add_house_surface"
                user.add_house_type = matches[0]
                user.add_house_deal = "فروش"
                user.save()
                return bot.sendMessage(msg["from"]["id"],
                                       "لطفاً متراژ ملک رو بین ۲۰ تا ۲۰۰۰۰۰ بنویس \n مثلاً اگه ملکتون ۲۰۰ متر هست بنویس فقط ۲۰۰",
                                       reply_markup=defualt_keyboard)

    if re.match("##add_deal_type (.*)", msg["text"]):

        if not matches[0] in allowed_add_house_deals:
            user.step = "add_deal_type"
            bot.sendMessage(msg["from"]["id"], "نوع معامله ! \nمیخوای اجاره بدی یا بفروشی؟",
                            reply_markup=deal_type_keyboard)
        else:

            user.add_house_deal = matches[0]
            user.save()

            if matches[0] == "رهن و اجاره":

                user.step = "add_house_pre_price"
                user.save()
                return bot.sendMessage(msg["from"]["id"],
                                       "لطفاً میزان ودیعه(رهن) رو  با فرمت زیر به میلیون تومان وارد کن:\n مثال: برای ۴۰ میلیون تومان وارد کنید : ۴۰",
                                       reply_markup=defualt_keyboard)
            else:

                user.step = "add_house_rooms"
                user.save()
                return bot.sendMessage(msg["from"]["id"], " روي تعداد اتاق خواب ملكت كليك كن ",
                                       reply_markup=room_number_keyboard)

    if re.match("##add_house_pre_price (.*)", msg["text"]):
        user.step = "add_house_ejare_time"
        user.add_house_pre_price = matches[0]
        user.save()
        return bot.sendMessage(msg["from"]["id"], "مدت زمان تقريبي اجاره ملك خودت رو مشخص كن:",
                               reply_markup=ejare_time_keyboard)

    if re.match("##add_house_ejare_time (.*)", msg["text"]):
        if not matches[0] in allowed_ejare_time:
            return bot.sendMessage(msg["from"]["id"], "مدت زمان تقريبي اجاره ملك خودت رو مشخص كن:",
                                   reply_markup=ejare_time_keyboard)

        else:
            user.step = "add_house_rooms"
            user.add_house_ejare_time = matches[0]
            user.save()
            return bot.sendMessage(msg["from"]["id"], "روي تعداد اتاق خواب ملكت كليك كن",
                                   reply_markup=room_number_keyboard)

    if re.match("##add_house_rooms (.*)", msg["text"]):

        if not matches[0] in allowed_add_house_rooms:

            user.step = "add_house_rooms"
            bot.sendMessage(msg["from"]["id"], "روي تعداد اتاق خواب ملكت كليك كن", reply_markup=room_number_keyboard)

        else:

            user.step = "add_house_surface"
            user.add_house_rooms = matches[0]
            user.save()
            return bot.sendMessage(msg["from"]["id"],
                                   "لطفاً متراژ ملک رو بین ۲۰ تا ۲۰۰۰۰۰ بنویس \n مثلاً اگه ملکتون ۲۰۰ متر هست بنویس فقط ۲۰۰",
                                   reply_markup=defualt_keyboard)


    if re.match("##add_house_surface (.*)", msg["text"]):

        if int(matches[0]) > maximum_house_surface or int(matches[0]) < minimum_house_surface:

            user.step = "add_house_surface"
            bot.sendMessage(msg["from"]["id"],
                            " لطفاً متراژ ملک رو بین ۲۰ تا ۲۰۰۰۰۰ بنویس\n مثلاً اگه ملکتون ۲۰۰ متر هست بنویس فقط ۲۰۰",
                            reply_markup=defualt_keyboard)

        else:

            user.step = "add_house_price"
            user.add_house_surface = matches[0]
            user.save()
            if user.add_house_deal == "رهن و اجاره":
                return bot.sendMessage(msg["from"]["id"],
                                       "لطفاً مبلغ اجاره ماهیانه رو به تومان وارد کن \n مثال: برای یک میلیون و چهارصد هزار تومان بنویس : ۱۴۰۰۰۰۰",
                                       reply_markup=defualt_keyboard)
            else:
                user.step = "add_house_swap"
                user.save()
                return bot.sendMessage(msg["from"]["id"],
                                       "آیا تمایل داری ملکت با اتومبیل یا ملک دیگری معاوضه بشه؟",
                                       reply_markup=swap_keyboard)

    if re.match("##add_house_swap (.*)", msg["text"]):
        if user.add_house_deal == "فروش":
            user.step = "add_house_price"
            user.add_house_swap = matches[0]
            user.save()
            return bot.sendMessage(msg["from"]["id"],
                                       "قیمت ملک رو به میلیون تومان بنویس\n مثال : برای ۲۵۰ میلیون تومان بنویس : ۲۵۰",
                                       reply_markup=defualt_keyboard)


    if re.match("##add_house_price (.*)", msg["text"]):
        if int(matches[0]) > maximum_house_price or int(matches[0]) < minimum_house_price:
            user.step = "add_house_price"
            bot.sendMessage(msg["from"]["id"],
                            "لطفاً مبلغ اجاره ماهیانه رو به تومان وارد کن \n مثال: برای یک میلیون و چهارصد هزار تومان بنویس : ۱۴۰۰۰۰۰",
                            reply_markup=defualt_keyboard)

        else:

            user.step = "add_house_city"
            user.add_house_price = matches[0]
            user.save()
            return bot.sendMessage(msg["from"]["id"], "ملک شما در کدوم شهر قرار داره؟",
                                   reply_markup=city_choice_keyboard)

    if re.match("##add_house_city (.*)", msg["text"]):  # TODO: string or keyboard? ask
        user.step = "add_house_address"
        user.add_house_city = matches[0]
        user.save()
        return bot.sendMessage(msg["from"]["id"], "لطفاً آدرس کامل ملکت رو وارد کن", reply_markup=defualt_keyboard)

    if re.match("##add_house_address (.*)", msg["text"]):
        if user.add_house_type not in no_room_houses:
            user.add_house_options = "لیست امکانات :\n"
            user.step = "add_house_options"
            user.add_house_address = matches[0]
            user.save()
            return bot.sendMessage(msg["from"]["id"],
                                   "بر روي امكانات ملك خودت كليك كن:\n مثال:در صورتي كه ملك شما داراي آسانسور  است بر روي گزينه كليك شود.",
                                   reply_markup=options_keyboard)

        else:
            user.add_house_address = matches[0]
            user.save()
            user.step = "add_house_contact_info"
            user.save()
            return bot.sendMessage(msg["from"]["id"],
                                   "لطفاً شماره تماس خودت رو به همراه کد شهر بین ۱۱ تا ۱۵ رقم وارد کن  \n▪️مثال : 09114235003 یا 01154235003",

                                   reply_markup=defualt_keyboard)

    if re.match("##add_house_options (.*)", msg["text"]):

        if not matches[0] == "<اتمام>":
            if matches[0] == "مشاهده لیست امکانات":
                bot.sendMessage(msg["from"]["id"], user.add_house_options, reply_markup=options_keyboard)
            if matches[0] in allowed_add_house_options:
                if not matches[0] in user.add_house_options:
                    user.add_house_options += "-{}\n".format(matches[0])
                    user.save()
            else:
                return bot.sendMessage(msg["from"]["id"], "لطفاً امکانات ملک رو وارد کن سپس اتمام رو بزن",
                                       reply_markup=options_keyboard)
        else:
            user.step = "add_house_contact_info"
            user.save()
            return bot.sendMessage(msg["from"]["id"],
                                   "لطفاً شماره تماس خودت رو به همراه کد شهر بین ۱۱ تا ۱۵ رقم وارد کن  \n▪️مثال : 09114235003 یا 01154235003",
                                   reply_markup=defualt_keyboard)

    if re.match("##add_house_contact_info (.*)", msg["text"]):
        if len(matches[0]) < 11 or len(matches[0]) > 15:
            user.step = "add_house_contact_info"
            bot.sendMessage(msg["from"]["id"],
                            "لطفاً شماره تماس خودت رو به همراه کد شهر بین ۱۱ تا ۱۵ رقم وارد کن  \n▪️مثال : 09114235003 یا 01154235003",
                            reply_markup=defualt_keyboard)
        else:
            user.step = "add_house_extra_info"
            user.add_house_contact_info = matches[0]
            user.save()
            return bot.sendMessage(msg["from"]["id"],
                                   "اگه دوست داري زودتربه نتيجه برسي توضیحات كامل ملكت رو اينجا بنويس\n ▪️مثال : تعداد طبقات, دسترسی به حمل و نقل عمومی، دانشگاه، مرکز خرید و غیره\n ",
                                   reply_markup=extra_keyboard)

    if re.match("##add_house_extra_info (.*)", msg["text"]):
        user.step = "add_house_file_id"
        user.add_house_extra_info = matches[0]
        user.save()
        return bot.sendMessage(msg["from"]["id"],
                               "يه عكس خوب از ملكت اينجا بزار تا زودتر مشتريش پيدا بشه:\n شما ميتونيدبا انتخاب دكمه📎 در اين قسمت عكس مورد نظر رو انتخاب و ارسال نماييد.\n",
                               reply_markup=image_keyboard)

    if re.match("##add_house_file_id (.*)", msg["text"]):  # dude in akso ok kon plz fln set null minevisam
        if matches[0] != "<img>":
            if matches[0] == "الان عکسی ندارم":
                user.add_house_file_id = "null"
                user.step = "create_house"
                user.save()
                bot.sendMessage(msg["from"]["id"], "آیا از اطلاعات ثبت شده مطمئن هستید؟", reply_markup=yes_no_keyboard)


            else:
                return bot.sendMessage(msg["from"]["id"], "لطفا عکس بده.", reply_markup=image_keyboard)

        if matches[0] == "<img>":
            user.step = "create_house"
            user.add_house_file_id = msg["photo_file_id"]  # TODO: IMAN
            user.save()
            bot.sendMessage(msg["from"]["id"], "آیا از اطلاعات ثبت شده مطمئن هستید؟", reply_markup=yes_no_keyboard)

    if re.match("##create_house (.*)", msg["text"]):
        if matches[0] == "بله مطمئنم!":
            q = House.objects.create(
                owner=user, house_type=user.add_house_type, house_deal=user.add_house_deal,
                house_pre_price=user.add_house_pre_price, house_ejare_time=user.add_house_ejare_time,
                house_price=user.add_house_price, house_city=user.add_house_city, house_address=user.add_house_address,
                house_rooms=user.add_house_rooms, house_swap = user.add_house_swap,
                house_surface=user.add_house_surface, house_contact_info=user.add_house_contact_info,
                house_options=user.add_house_options, house_extra_info=user.add_house_extra_info,
                house_file_id=user.add_house_file_id, hidden=False if user.is_admin else True,

            )
            return_text = "ملک شما با موفقیت ثبت شد \nاطلاعات ملک شما:\n\n"
            return_text += "ثبت کننده آگهی: {}\n".format(q.get_house_owner())
            return_text += "تاریخ ثبت: {}\n".format(q.date_created)

            return_text += "\n اطلاعات تماس: {}".format(q.house_contact_info)
            return_text += "\n شهر : #{}".format(q.house_city)
            return_text += "\n نوع ملک : {}".format(q.house_type)
            return_text += "\n آدرس ملک: {}".format(q.house_address)
            return_text += "\n متراژ: {} متر مربع".format(q.house_surface)
            return_text += "\n نوع معامله: {}".format(q.house_deal)

            if q.house_deal == "رهن و اجاره":

                return_text += "\n میزان ودیعه :{} میلیون تومان".format(q.house_pre_price)
                return_text += "\n قیمت اجاره ماهیانه: {}تومان".format(q.house_price)
                return_text += "\n مدت زمان تقريبي اجاره: {}".format(q.house_ejare_time)

            else:
                return_text += "\n قیمت کل ملک: {} میلیون تومان".format(q.house_price)
                if q.house_swap == "بدم نمیاد":
                    return_text += "\nمالک تمایل خود را برای معاوضه ملک با خودرو یا ملک دیگری اعلام میکند.\n"

            if q.house_type not in no_room_houses:
                return_text += "\n تعداد اتاق: {}".format(q.house_rooms)
                return_text += "\n امکانات ملک: {}".format(q.house_options)

            return_text += "\n اطلاعات اضافی: {}\n\n".format(q.house_extra_info)
            return_text += "از انتخاب شما سپاسگزاريم.\n ملك شما با موفقيت در ربات ملكي بدوبيا ثبت شد و بزودي به نمايش گذاشته ميشود.\n لطفا لينك بدوبيا رو به دوستانتون در گروه هاي مختلف معرفي كنيد.به اميد خانه دار شدن همه!@bodobia_bot"
            return_text += "\n Image File ID: {}".format(q.house_file_id)

            user.step = None
            user.save()

            bot.sendMessage(msg["from"]["id"], return_text, reply_markup=defualt_keyboard)
            return bot.sendMessage(msg["from"]["id"], "انجام شد\nبرای بازگشت به صفحه اصلی گزینه <بیخیال> رو بزنید", reply_markup=defualt_keyboard)
