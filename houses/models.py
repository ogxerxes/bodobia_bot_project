from django.db import models


# Create your models here.
class House(models.Model):
    class Meta:
        db_table = 'houses'

    owner = models.ForeignKey('telegram_users.TelegramUser', null=True, blank=True, on_delete=models.CASCADE)
    house_type = models.CharField(null=True, blank=True, max_length=100)
    house_deal = models.CharField(null=True, blank=True, max_length=100)
    house_city = models.CharField(null=True, blank=True, max_length=100)
    house_price = models.IntegerField(null=True, blank=True)
    house_address = models.CharField(null=True, blank=True, max_length=1000)
    house_file_id = models.CharField(null=True, blank=True, max_length=300)
    house_rooms = models.CharField(null=True, blank=True, max_length=100)
    house_ejare_time = models.CharField(null=True, blank=True, max_length=100)

    house_surface = models.IntegerField(null=True, blank=True)
    house_swap = models.CharField(null=True, blank=True, max_length=100)
    house_contact_info = models.CharField(null=True, blank=True, max_length=200)
    house_options = models.CharField(null=True, blank=True, max_length=500)
    house_extra_info = models.CharField(null=True, blank=True, max_length=5000)
    house_pre_price = models.IntegerField(null=True, blank=True)
    hidden = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.house_address

    def get_contact_info(self):
        return self.house_contact_info

    def get_hidden_status(self):

        if self.hidden:
            return "تایید نشده"
        else:
            return "ملک شما تایید شده است"

    def confirm(self):
        self.hidden = False
        self.save()
        return True

    def get_house_owner(self):
        return self.owner.username if self.owner.username else self.owner.name if self.owner.name else self.owner.telegram_id
