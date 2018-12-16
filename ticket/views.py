from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import LotteryLot, Lank, Number, BuyingHistory
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

        # 購入枚数
        ticket_count = 1
        # 購入時点の最新ロット
        latest_lot = LotteryLot.objects.order_by("-created_at").first()
        # チケットの在庫
        remain_tickets = n.filter(lot_id=latest_lot, is_sold=False).order_by('number')
        # TODO: 在庫枚数を超える注文が来た場合の処理
        if len(remain_tickets) < ticket_count:
            return redirect('ticket:buying')
        for i in random.sample(range(len(remain_tickets)), k=ticket_count):
            sold_ticket = remain_tickets[i]
            sold_ticket.is_sold = True
            sold_ticket.save()
            if len(n.filter(lot_id=latest_lot, is_sold=False)) == 0:
                latest_lot.is_sold_out = True
                latest_lot.save()
            BuyingHistory.objects.create(number=sold_ticket, user=request.user)

        return redirect('ticket:buying_done')

    context = {}

    return render(request, 'ticket/buying.html', context)

def buying_done(request):

    context = {}

    return render(request, 'ticket/buying_done.html', context)
