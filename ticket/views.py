from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import LotteryLot, Lank, Number
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

import random


def buying(request):

    latest_lot = LotteryLot.objects.order_by("-created_at").first()
    n = Number.objects
    # TODO: どのランクを買ったか受け取る
    lank = Lank.objects.order_by("-price").first() # mega
    ticket_num = 3 # 1ロットに発行するチケット数

    if request.method == 'POST':
        if latest_lot.is_sold_out == True:
            # 新しいロットを生成
            LotteryLot.objects.create(lank=lank)
            # 最新ロット更新
            latest_lot = LotteryLot.objects.order_by("-created_at").first()
            # ロットに数字を格納
            numbers = []
            for i in range(ticket_num):
                numbers.append(i+1)
                n.create(lot_id=latest_lot, number=i+1)
            print(numbers)
            # 当選番号をランダムに選択
            winning_num = random.choice(numbers)
            print(winning_num)
            winning_num_in_this_lot = n.get(lot_id=latest_lot, number=winning_num)
            winning_num_in_this_lot.is_winning = True
            winning_num_in_this_lot.save()

        # TODO: チケット購入処理
        return redirect('main:index')

    context = {

    }

    return render(request, 'ticket/buying.html', context)
