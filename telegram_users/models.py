from django.db import models
from telepot import Bot

from bodobia import settings

bot = Bot(settings.BOT_TOKEN)


class TelegramUser(models.Model):
    class Meta:
        db_table = 'telegram_users'

    name = models.CharField(max_length=300)
    telegram_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    messages = models.IntegerField(default=1)
    step = models.CharField(max_length=500, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    search_house_type = models.CharField(null=True, blank=True, max_length=100)
    search_house_deal = models.CharField(null=True, blank=True, max_length=100)
    search_house_city = models.CharField(null=True, blank=True, max_length=100)

    add_house_type = models.CharField(null=True, blank=True, max_length=100)
    add_house_deal = models.CharField(null=True, blank=True, max_length=100)
    add_house_ejare_time = models.CharField(null=True, blank=True, max_length=100)
    add_house_price = models.IntegerField(null=True, blank=True)
    add_house_city = models.CharField(null=True, blank=True, max_length=100)
    add_house_address = models.CharField(null=True, blank=True, max_length=1000)
    add_house_file_id = models.CharField(null=True, blank=True, max_length=300)
    add_house_rooms = models.CharField(null=True, blank=True, max_length=100)
    add_house_surface = models.IntegerField(null=True, blank=True)
    add_house_swap = models.CharField(null=True, blank=True, max_length=100)
    add_house_contact_info = models.CharField(null=True, blank=True, max_length=200)
    add_house_options = models.CharField(null=True, blank=True, max_length=500)
    add_house_extra_info = models.CharField(null=True, blank=True, max_length=5000)
    add_house_pre_price = models.IntegerField(null=True, blank=True)

    res_number = models.IntegerField(null=True, blank=True, default=1)
    admin_start_range = models.IntegerField(null=True, blank=True, default=0)
    admin_end_range = models.IntegerField(null=True, blank=True, default=4)
    user_comment = models.CharField(null=True, blank=True, max_length=1000)

    bot = bot

    def __str__(self):
        if self.username:
            return self.username
        else:
            return str(self.telegram_id)

    def set_step(self, step):
        self.step = step
        self.save()


class Comment(models.Model):
    class Meta:
        db_table = 'comments'

    owner = models.ForeignKey('telegram_users.TelegramUser', null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=5000, null=True, blank=True)

    def get_comment_owner(self):
        if self.owner.username:
            return "@{}".format(self.owner.username)

        else:
            return self.owner.name if self.owner.name else self.owner.telegram_id
