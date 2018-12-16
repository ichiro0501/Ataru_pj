from django.db import models
from django.conf import settings
from django.utils import timezone

class Lank(models.Model):

    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class LotteryLot(models.Model):

    lank = models.ForeignKey(Lank, on_delete=models.CASCADE, related_name='ticket_lank')
    announced_at = models.DateTimeField(default=timezone.now)
    expired_at = models.DateTimeField(default=timezone.now)
    is_sold_out = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{0} : from {1} to {2}'.format(self.lank, self.created_at, self.announced_at)

class Number(models.Model):

    lot_id = models.ForeignKey(LotteryLot, on_delete=models.CASCADE, related_name='lot_id')
    number = models.IntegerField(default=0)
    is_sold = models.BooleanField(default=False)
    is_winning = models.BooleanField(default=False)

    def __str__(self):
        return '{0} (lot is {1})'.format(self.number, self.lot_id)

    def sold(self):
        self.is_sold = True
        self.save()

class BuyingHistory(models.Model):
    """購入履歴"""
    number = models.ForeignKey(Number, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='購入ユーザー', on_delete=models.PROTECT)
    created_at = models.DateTimeField('日付', default=timezone.now)

    def __str__(self):
        return '{} {} '.format(self.number, self.user.email)
