from django.contrib import admin

from .models import LotteryLot, Lank, Number


admin.site.register(Lank)
admin.site.register(Number)
admin.site.register(LotteryLot)
