import datetime
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from .forms import *

from metaData.models import Item

# Create your views here.

@login_required(login_url='common:login')
def inventoryIndex(request):
    page = request.GET.get('page',1) # 페이지
    kw = request.GET.get('kw','') #검색어
    fromDate = request.GET.get('fromDate','')
    toDate = request.GET.get('toDate','')


    item_list = Item.objects.filter(user__exact = request.user)
    filter_list = Item.objects.filter(user__exact = request.user)

    if kw:
        if kw!='all':
            filter_list = filter_list.filter(pk = kw)

    inventory_list = Inventory.objects.filter(item__in = filter_list).order_by('-referenceDate')
    format = '%Y-%m-%d'
    if fromDate:
        fromDate = datetime.strptime(fromDate, "%Y-%m-%d").replace(hour=0,minute=0,second=0)
        inventory_list= inventory_list.filter(referenceDate__gte = fromDate)
        fromDate = fromDate.strftime("%Y-%m-%d")
    if toDate:
        toDate = datetime.strptime(toDate, "%Y-%m-%d").replace(hour=23,minute=59,second=59)
        inventory_list= inventory_list.filter(referenceDate__lte = toDate)
        toDate = toDate.strftime("%Y-%m-%d")

    paginator = Paginator(inventory_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'inventory_list':page_obj,'item_list':item_list,'page':page,'kw':kw,'fromDate':fromDate,'toDate':toDate}

    return render(request, 'transaction/inventory/inventoryIndex.html', context)

@login_required(login_url='common:login')
def initialInv_modify(request, inv_id):
    initial_inv = Inventory.objects.get(pk =inv_id)
    before_modify = initial_inv.amount
    if initial_inv.item.user != request.user:
        messages.error(request, "인가된 사용자가 아닙니다")
        return HttpResponse('<script type="text/javascript">opener.location.reload();window.close()</script>')
    if initial_inv.is_initial == False:
        messages.error(request, "초기 재고가 아닙니다.")
        return HttpResponse('<script type="text/javascript">opener.location.reload();window.close()</script>')

    if request.method == 'POST':
        initial_amount = int(request.POST['amount'])
        if initial_amount:

            check_inv = Inventory.objects.filter(Q(item__exact = initial_inv.item) & Q(is_initial__exact = False))
            error_inv = check_inv.filter(amount__lt = before_modify - initial_amount)
            if len(error_inv) > 0:
                messages.error(request,"음수가 되는 재고가 있습니다. 최초 수량을 다시 확인해주세요.")
                return redirect("transaction:initialInv_modify", inv_id = inv_id)
            initial_inv.amount = initial_amount
            initial_inv.save()

            for inv in check_inv:
                inv.amount = inv.amount - before_modify + int(initial_amount)
                inv.save()

            return HttpResponse('<script type="text/javascript">opener.location.reload();window.close()</script>')

    context = {'initial_inv':initial_inv}
    return render(request,'transaction/inventory/initialInv_modify.html',context)

@login_required(login_url='common:login')
def buyIndex(request):
    page = request.GET.get('page',1) # 페이지
    kw = request.GET.get('kw','') #검색어
    fromDate = request.GET.get('fromDate','')
    toDate = request.GET.get('toDate','')

    item_list = Item.objects.filter(user__exact = request.user)
    filter_list = Item.objects.filter(user__exact = request.user)

    if kw:
        if kw!='all':
            filter_list = filter_list.filter(pk = kw)

    buy_list = Transaction.objects.filter(Q(item__in = filter_list) & Q(is_buy__exact = True)).order_by('-referenceDate')

    format = '%Y-%m-%d'
    if fromDate:
        fromDate = datetime.strptime(fromDate, "%Y-%m-%d").replace(hour=0,minute=0,second=0)
        buy_list= buy_list.filter(referenceDate__gte = fromDate)
        fromDate = fromDate.strftime("%Y-%m-%d")
    if toDate:
        toDate = datetime.strptime(toDate, "%Y-%m-%d").replace(hour=23,minute=59,second=59)
        buy_list= buy_list.filter(referenceDate__lte = toDate)
        toDate = toDate.strftime("%Y-%m-%d")

    paginator = Paginator(buy_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'buy_list':page_obj,'item_list':item_list,'page':page,'kw':kw,'fromDate':fromDate,'toDate':toDate}

    return render(request, 'transaction/buy/buyIndex.html', context)

@login_required(login_url='common:login')
def buy_add(request):
    company_list = OtherCompany.objects.filter(Q(user__exact = request.user) & Q(is_vendor__exact = True))
    item_list = Item.objects.filter(Q(user__exact = request.user))
    if request.method == 'POST':
        form = transactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.is_buy = True
            transaction.is_sell = False
            transaction.save()

            add_inv = Inventory(item = transaction.item, referenceDate = transaction.referenceDate, is_initial = False)

            inv_afterTransaction = Inventory.objects.filter(Q(item__exact = transaction.item) & Q(referenceDate__gte = transaction.referenceDate)).order_by('-referenceDate')
            if len(inv_afterTransaction) > 0:
                for trs in inv_afterTransaction:
                    temp_amount = trs.amount
                    trs.amount = temp_amount + transaction.amount
                    trs.save()

            latest_inv = Inventory.objects.filter(Q(item__exact = transaction.item) & Q(referenceDate__lte = transaction.referenceDate)).order_by('-referenceDate')[0]
            add_inv.amount = latest_inv.amount + transaction.amount
            add_inv.note = "제품 입고(구매) - " + str(transaction.amount) + "개"
            add_inv.save()

            return redirect("transaction:buyIndex")
    else:
        form = transactionForm()
    context = {'company_list':company_list, 'item_list': item_list, 'form':form}
    return render(request, 'transaction/buy/buyForm.html', context)

@login_required(login_url='common:login')
def buy_delete(request, buy_id):
    buy_transaction = Transaction.objects.get(pk = buy_id)
    after_refDate = Inventory.objects.filter(Q(item__exact = buy_transaction.item) & Q(referenceDate__gte = buy_transaction.referenceDate))

    if buy_transaction.item.user != request.user:
        return redirect("transaction:buyIndex")

    for inv in after_refDate:
        if inv.amount - buy_transaction.amount < 0:
            messages.error(request,"음수가 되는 재고가 존재합니다. 삭제할 수 없음으로 다시 확인해주세요.")
            return redirect("transaction:buyIndex")

    for inv in after_refDate:
        inv.amount  = inv.amount - buy_transaction.amount
        inv.save()
    delete_inv = after_refDate.filter(Q(referenceDate__exact = buy_transaction.referenceDate))
    buy_transaction.delete()
    delete_inv.delete()
    return redirect("transaction:buyIndex")

@login_required(login_url='common:login')
def buy_modify(request, buy_id):
    company_list = OtherCompany.objects.filter(Q(user__exact = request.user) & Q(is_vendor__exact = True))
    item_list = Item.objects.filter(Q(user__exact = request.user))

    buy_transaction = Transaction.objects.get(pk=buy_id)
    before_modify_refDate = buy_transaction.referenceDate
    before_modify_amount = buy_transaction.amount
    before_note = buy_transaction.note

    if buy_transaction.item.user != request.user:
        messages.error(request, "인가된 사용자가 아닙니다")
        return redirect("transaction:buyIndex")

    if request.method == 'POST':
        form = transactionForm(request.POST, instance=buy_transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            after_modify_refDate = transaction.referenceDate
            after_modify_amount = transaction.amount
            after_note = "제품 입고(구매) - " + str(transaction.amount) + "개"

            # 날자를 더 나중으로 옮긴다 (before 이 더 빠르다)
            # btw_dates 영향력이 사라진다 --> 재고가 줄어든다 --> 검사 필요

            if before_modify_refDate < after_modify_refDate:
                btw_dates = Inventory.objects.filter(Q(item__exact = buy_transaction.item) & Q(referenceDate__gte = before_modify_refDate) & Q(referenceDate__lt = after_modify_refDate)).order_by('-referenceDate')
                after_modifyDate = Inventory.objects.filter(Q(item__exact = buy_transaction.item) & Q(referenceDate__gt = after_modify_refDate))

                for inv in btw_dates:
                    if inv.amount - before_modify_amount < 0:
                        messages.error(request, "재고가 부족해지는 날이 있습니다. 다시 확인해주세요")
                        return redirect("transaction:buy_modify", buy_id = buy_id)

                for inv in after_modifyDate:
                    if inv.amount - before_modify_amount + after_modify_amount < 0:
                        messages.error(request, "재고가 부족해지는 날이 있습니다. 다시 확인해주세요")
                        return redirect("transaction:buy_modify", buy_id = buy_id)

                for inv in btw_dates:
                    inv.amount = inv.amount - before_modify_amount
                    inv.save()
                for inv in after_modifyDate:
                    inv.amount = inv.amount - before_modify_amount + after_modify_amount
                    inv.save()

                delete_inv = Inventory.objects.get(Q(item__exact = buy_transaction.item) & Q(referenceDate__exact = before_modify_refDate))
                delete_inv.delete()
                latest_inv = Inventory.objects.filter(Q(item__exact = buy_transaction.item) & Q(referenceDate__lt = after_modify_refDate)).order_by('-referenceDate')[0]
                print(latest_inv)
                print(latest_inv.amount)
                print(latest_inv.item)
                add_inv = Inventory(item = buy_transaction.item, referenceDate = after_modify_refDate,
                                    amount = latest_inv.amount + after_modify_amount,
                                    is_initial = False, note = after_note)
                add_inv.save()

            # 날자를 더 빠르게 옮긴다
            elif before_modify_refDate > after_modify_refDate:
                btw_dates = Inventory.objects.filter(Q(item__exact = buy_transaction.item) & Q(referenceDate__gt = after_modify_refDate) & Q(referenceDate__lt = before_modify_refDate)).order_by('-referenceDate')
                after_nonModifyDate = Inventory.objects.filter(Q(item__exact = buy_transaction.item) & Q(referenceDate__gt = before_modify_refDate))

                for inv in after_nonModifyDate:
                    if inv.amount - before_modify_amount + after_modify_amount<0:
                        messages.error(request, "재고가 부족해지는 날이 있습니다. 다시 확인해주세요")
                        return redirect("transaction:buy_modify", buy_id = buy_id)

                add_inv = Inventory(item=buy_transaction.item, referenceDate=after_modify_refDate,
                                    amount=Inventory.objects.filter(Q(item__exact = buy_transaction.item) & Q(referenceDate__lte = after_modify_refDate)).order_by('-referenceDate')[0].amount + after_modify_amount, is_initial=False,
                                    note=after_note)
                add_inv.save()

                after_nonModifyDate = Inventory.objects.filter(Q(item__exact = buy_transaction.item) & Q(referenceDate__gte = before_modify_refDate))

                for inv in after_nonModifyDate:
                    inv.amount = inv.amount - before_modify_amount + after_modify_amount
                    inv.save()

                for inv in btw_dates:
                    inv.amount = inv.amount + after_modify_amount
                    inv.save()

                delete_inv = Inventory.objects.get(
                    Q(item__exact=buy_transaction.item) & Q(referenceDate__exact=before_modify_refDate))
                delete_inv.delete()


            else:
                after_modifyDate = Inventory.objects.filter(Q(item__exact = buy_transaction.item) & Q(referenceDate__gte = after_modify_refDate))

                for inv in after_modifyDate:
                    if inv.amount - before_modify_amount + after_modify_amount < 0:
                        messages.error(request, "재고가 부족해지는 날이 있습니다. 다시 확인해주세요")
                        return redirect("transaction:buy_modify", buy_id = buy_id)

                for inv in after_modifyDate:
                    if inv.referenceDate == after_modify_refDate:
                        inv.note = after_note
                    inv.amount = inv.amount - before_modify_amount + after_modify_amount
                    inv.save()

            transaction.is_buy = True
            transaction.is_sell = False
            transaction.save()
            return redirect("transaction:buyIndex")

    else:
        form = transactionForm(instance=buy_transaction)
    context = {'company_list': company_list, 'item_list': item_list, 'form': form,'buy_id':buy_id}
    return render(request, 'transaction/buy/buyForm.html', context)

@login_required(login_url='common:login')
def buy_detail(request, buy_id):
    buy_transaction = get_object_or_404(Transaction, pk = buy_id)
    if buy_transaction.item.user != request.user:
        messages.error(request, "인가된 사용자가 아닙니다")
        return redirect("transaction:buyIndex")

    form = transactionForm(instance=buy_transaction)
    context = {'form':form,'buy_transaction':buy_transaction,'buy_id':buy_id}
    return render(request, 'transaction/buy/buyDetail.html', context)


@login_required(login_url='common:login')
def sellIndex(request):
    page = request.GET.get('page',1) # 페이지
    kw = request.GET.get('kw','') #검색어
    fromDate = request.GET.get('fromDate','')
    toDate = request.GET.get('toDate','')

    item_list = Item.objects.filter(user__exact = request.user)
    filter_list = Item.objects.filter(user__exact = request.user)

    if kw:
        if kw!='all':
            filter_list = filter_list.filter(pk = kw)

    sell_list = Transaction.objects.filter(Q(item__in = filter_list) & Q(is_sell__exact = True)).order_by('-referenceDate')

    format = '%Y-%m-%d'
    if fromDate:
        fromDate = datetime.strptime(fromDate, "%Y-%m-%d").replace(hour=0,minute=0,second=0)
        sell_list= sell_list.filter(referenceDate__gte = fromDate)
        fromDate = fromDate.strftime("%Y-%m-%d")
    if toDate:
        toDate = datetime.strptime(toDate, "%Y-%m-%d").replace(hour=23,minute=59,second=59)
        sell_list= sell_list.filter(referenceDate__lte = toDate)
        toDate = toDate.strftime("%Y-%m-%d")

    paginator = Paginator(sell_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'sell_list':page_obj,'item_list':item_list,'page':page,'kw':kw,'fromDate':fromDate,'toDate':toDate}

    return render(request, 'transaction/sell/sellIndex.html', context)



@login_required(login_url='common:login')
def sell_add(request):
    company_list = OtherCompany.objects.filter(Q(user__exact = request.user) & Q(is_customer__exact = True))
    item_list = Item.objects.filter(Q(user__exact = request.user))
    if request.method == 'POST':
        form = transactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.is_buy = False
            transaction.is_sell = True

            check_inv_list = Inventory.objects.filter(Q(item__exact = transaction.item) & Q(referenceDate__gt = transaction.referenceDate))
            latest_inv = Inventory.objects.filter(Q(item__exact = transaction.item) & Q(referenceDate__lt = transaction.referenceDate)).order_by('-referenceDate')[0]
            for inv in check_inv_list:
                if inv.amount - transaction.amount < 0:
                    messages.error(request, "음수가 되는 재고가 있습니다. 수량 혹은 날짜를 다시 확인해주세요")
                    return redirect("transaction:sell_add")

            if latest_inv.amount - transaction.amount < 0:
                messages.error(request, "음수가 되는 재고가 있습니다. 수량 혹은 날짜를 다시 확인해주세요")
                return redirect("transaction:sell_add")

            for inv in check_inv_list:
                inv.amount = inv.amount - transaction.amount
                inv.save()

            new_inv = Inventory(referenceDate = transaction.referenceDate,
                                item = transaction.item,
                                amount = latest_inv.amount - transaction.amount,
                                is_initial = False,
                                note = f"제품 출고(판매) - {transaction.amount}개")

            new_inv.save()
            transaction.save()

            return redirect("transaction:sellIndex")
    else:
        form = transactionForm()
    context = {'company_list':company_list, 'item_list': item_list, 'form':form}
    return render(request, 'transaction/sell/sellForm.html', context)

@login_required(login_url='common:login')
def sell_detail(request, sell_id):
    sell_transaction = get_object_or_404(Transaction, pk = sell_id)
    if sell_transaction.item.user != request.user:
        messages.error(request, "인가된 사용자가 아닙니다")
        return redirect("transaction:sellIndex")

    form = transactionForm(instance=sell_transaction)
    context = {'sell_transaction':sell_transaction, 'form':form, 'sell_id': sell_id}
    return render(request, 'transaction/sell/sellDetail.html', context)

@login_required(login_url='common:login')
def sell_delete(request, sell_id):
    sell_transaction = get_object_or_404(Transaction, pk = sell_id)
    if sell_transaction.item.user != request.user:
        messages.error(request, "인가된 사용자가 아닙니다")
        return redirect("transaction:sellIndex")

    check_inventory = Inventory.objects.filter(Q(item__exact = sell_transaction.item) & Q(referenceDate__gt = sell_transaction.referenceDate))
    for inv in check_inventory:
        inv.amount = inv.amount + sell_transaction.amount
        inv.save()

    delete_inventory = Inventory.objects.filter(Q(item__exact = sell_transaction.item) & Q(referenceDate__exact = sell_transaction.referenceDate))
    delete_inventory.delete()
    sell_transaction.delete()
    return redirect("transaction:sellIndex")

@login_required(login_url='common:login')
def sell_modify(request, sell_id):
    sell_transaction = get_object_or_404(Transaction, pk = sell_id)
    notModified_amount = sell_transaction.amount
    notModified_refDate = sell_transaction.referenceDate

    if sell_transaction.item.user != request.user:
        messages.error(request, "인가된 사용자가 아닙니다")
        return redirect("transaction:sellIndex")

    if request.method == 'POST':
        form = transactionForm(request.POST, instance=sell_transaction)
        if form.is_valid():
            sell_transaction_modified = form.save(commit=False)
            modified_amount = int(sell_transaction_modified.amount)
            modified_refDate = sell_transaction_modified.referenceDate

            # 시간대를 더 나중으로 옮긴다. -> 다음 transaction 의 영향권이 적어진다.
            # transaction 의 영향권이 사라진 곳 = 두 시간대의 중간 (재고가 수정 전 수량만큼 늘어난다) -> check 필요 x
            # transaction 의 영향권이 있는 곳 = modified_refDate 이후 -> check 필요 0
            # notModified_refDate -> modified_refDate 시간 순서
            if notModified_refDate < modified_refDate:
                lost_influence_inv = Inventory.objects.filter(Q(item__exact = sell_transaction.item) &
                                                              Q(referenceDate__gt = notModified_refDate) &
                                                              Q(referenceDate__lt = modified_refDate))
                influence_inv = Inventory.objects.filter(Q(item__exact = sell_transaction.item) &
                                                         Q(referenceDate__gt = modified_refDate))


                error_inv = influence_inv.filter(Q(amount__lt = modified_amount - notModified_amount))
                if len(error_inv) > 0:
                    messages.error(request, "재고량이 부족합니다. 시간대 혹은 수량을 다시 확인하세요")
                    return redirect("transaction:sell_modify", sell_id = sell_id)

                for inv in lost_influence_inv:
                    inv.amount = inv.amount + notModified_amount
                    inv.save()

                for inv in influence_inv:
                    inv.amount = inv.amount + notModified_amount - modified_amount
                    inv.save()

                latest_inv = Inventory.objects.filter(Q(item__exact=sell_transaction.item) &
                                                      Q(referenceDate__lt=modified_refDate)).order_by('-referenceDate')[0]

                modify_inv = Inventory.objects.filter(Q(item__exact = sell_transaction.item) &
                                                      Q(referenceDate__exact = notModified_refDate))[0]
                modify_inv.referenceDate = modified_refDate
                modify_inv.amount = latest_inv.amount - modified_amount
                print(latest_inv.amount)
                modify_inv.note = f"제품 출고(판매) - {modified_amount}개"
                modify_inv.save()

                sell_transaction_modified.save()
            elif notModified_refDate > modified_refDate:
                '''
                시간대를 더 이전으로 옮긴다 -> 다음 transaction 의 영향권이 커진다
                transaction 의 영향권이 커지는 곳 = 두 시간대의 중간 (재고가 수정 전 수량만큼 늘어난다) -> check 필요 ㅇ
                transaction 의 영향권이 원래 있는 곳 = notModified_refDate 이후 -> check 필요 ㅇ
                modified_refDate -> 영향권이 커진 곳 -> notModified_refDate -> 영향권이 원래 있던 곳 시간 순서
                '''
                expand_influence_inv = Inventory.objects.filter(Q(item__exact=sell_transaction.item) &
                                                              Q(referenceDate__gt=modified_refDate) &
                                                              Q(referenceDate__lt=notModified_refDate))
                origin_incluence_inv =  Inventory.objects.filter(Q(item__exact = sell_transaction.item) &
                                                                 Q(referenceDate__gt = notModified_refDate))

                error_expand = expand_influence_inv.filter(amount__lt = modified_amount)
                error_origin = origin_incluence_inv.filter(amount__lt = modified_amount - notModified_amount)

                if (len(error_origin) > 0) or (len(error_expand) > 0):
                    messages.error(request, "재고량이 부족합니다. 시간대 혹은 수량을 다시 확인하세요")
                    return redirect("transaction:sell_modify", sell_id= sell_id)

                for inv in expand_influence_inv:
                    inv.amount = inv.amount - modified_amount
                    inv.save()

                for inv in origin_incluence_inv:
                    inv.amount = inv.amount - modified_amount + notModified_amount
                    inv.save()

                just_before_modifiedInv = Inventory.objects.filter(Q(item__exact = sell_transaction.item) &
                                                                   Q(referenceDate__lt = modified_refDate)).order_by('-referenceDate')[0]

                modify_inv = Inventory.objects.filter(Q(item__exact = sell_transaction.item) &
                                                      Q(referenceDate__exact = notModified_refDate))[0]

                modify_inv.referenceDate = modified_refDate
                modify_inv.amount = just_before_modifiedInv.amount - modified_amount
                modify_inv.note = f"제품 출고(판매) - {modified_amount}개"
                modify_inv.save()

                sell_transaction_modified.save()
            else:
                '''
                시간대가 동일하다 -> 영향권이 동일하다. (시간대에 따른 check 와 저장을 따로 하지 않아도 괜찮다)
                시간대 이후만 check 해주면 된다.
                '''
                influence_inv = Inventory.objects.filter(Q(item__exact=sell_transaction.item) & Q(referenceDate__gte=notModified_refDate))

                error_inv = influence_inv.filter(Q(amount__lt = modified_amount - notModified_amount))

                if len(error_inv) > 0:
                    messages.error(request, "재고량이 부족합니다. 시간대 혹은 수량을 다시 확인하세요")
                    return redirect("transaction:sell_modify", sell_id = sell_id)

                for inv in influence_inv:
                    inv.amount = inv.amount + notModified_amount - modified_amount
                    if inv.referenceDate == notModified_refDate:
                        inv.note = f"제품 출고(판매) - {modified_amount}개"
                    inv.save()

                sell_transaction_modified.save()
            return redirect("transaction:sellIndex")
    else:
        form = transactionForm(instance=sell_transaction)

    company_list = OtherCompany.objects.filter(Q(user__exact = request.user) & Q(is_customer__exact = True))
    item_list = Item.objects.filter(Q(user__exact = request.user))
    context = {'company_list': company_list, 'item_list': item_list, 'form': form, 'sell_id': sell_id}
    return render(request,"transaction/sell/sellForm.html", context)

@login_required(login_url='common:login')
def produceIndex(request):
    page = request.GET.get('page',1) # 페이지
    kw = request.GET.get('kw','') #검색어
    fromDate = request.GET.get('fromDate','')
    toDate = request.GET.get('toDate','')

    item_list = Item.objects.filter(user__exact = request.user)
    filter_list = Item.objects.filter(user__exact = request.user)

    if kw:
        if kw!='all':
            filter_list = filter_list.filter(pk = kw)

    produce_list = Produce.objects.filter(itemNode__item__in = filter_list).order_by('-referenceDate')

    if fromDate:
        fromDate = datetime.strptime(fromDate, "%Y-%m-%d").replace(hour=0,minute=0,second=0)
        produce_list= produce_list.filter(referenceDate__gte = fromDate)
        fromDate = fromDate.strftime("%Y-%m-%d")
    if toDate:
        toDate = datetime.strptime(toDate, "%Y-%m-%d").replace(hour=23,minute=59,second=59)
        produce_list= produce_list.filter(referenceDate__lte = toDate)
        toDate = toDate.strftime("%Y-%m-%d")

    consume_dict = dict()

    for produce in produce_list:
        produceAmount = produce.amount
        ingredientQuery = produce.itemNode.get_children()
        ingredientList = list()
        for ingredientNode in ingredientQuery:
            ingredient = ingredientNode.item
            ingredientConsume = ingredientNode.required * produceAmount
            ingredientList.append((ingredient, ingredientConsume))
        consume_dict[produce.id] = ingredientList

    paginator = Paginator(produce_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'produce_list':page_obj,'item_list':item_list,'page':page,'kw':kw,'fromDate':fromDate,'toDate':toDate,'consume_dict':consume_dict}

    return render(request, 'transaction/produce/produceIndex.html', context)

@login_required(login_url='common:login')
def produce_add(request):
    allNode = list(Node.objects.filter(item__user__exact = request.user))
    item_node_list = list()
    for node in allNode:
        if node.is_leaf() == False:
            item_node_list.append(node)

    if request.method == 'POST':
        form = produceForm(request.POST)
        if form.is_valid():
            produce = form.save(commit=False)
            produceItem = produce.itemNode.item
            ingredientQuery = produce.itemNode.get_children()

            for node in ingredientQuery:
                ingredient = node.item
                required_amount = node.required * produce.amount

                affected_inv = Inventory.objects.filter(Q(item__exact = ingredient) & Q(referenceDate__gt = produce.referenceDate))
                error_inv = affected_inv.filter(amount__lt = required_amount)
                latest_inv = Inventory.objects.filter(Q(referenceDate__lt=produce.referenceDate)
                                                      & Q(item__exact=ingredient)).order_by('-referenceDate')[0]

                if latest_inv.amount - required_amount < 0:
                    messages.error(request, f"{ingredient.name}의 재고가 부족합니다. 재고 수량을 확인해주세요.")
                    return redirect("transaction:produce_add")

                if len(error_inv)> 0:
                    messages.error(request,f"{ingredient.name}의 재고가 부족합니다. 재고 수량을 확인해주세요.")
                    return redirect("transaction:produce_add")

                error_inv = affected_inv.filter(Q(referenceDate__lt = produce.referenceDate))
                if len(error_inv)>0:
                    messages.error(request, f"최초 등록일 이전에 생산하실 수 없습니다. 최초 등록일을 다시 확인해주세요.({ingredient.name})")
                    return redirect("transaction:produce_add")

                error_inv = Inventory.objects.filter(Q(referenceDate__exact = produce.referenceDate) &
                                                Q(item__exact = ingredient))

                if len(error_inv)>0:
                    messages.error(request, f"동시에 입출고 될 수 없습니다. 시간을 다시 확인해주시거나 바꾸어주세요.({ingredient.name})")
                    return redirect("transaction:produce_add")

            for node in ingredientQuery:

                ingredient = node.item
                required_amount = node.required * produce.amount
                latest_inv = Inventory.objects.filter(Q(referenceDate__lt=produce.referenceDate)
                                                      & Q(item__exact=ingredient)).order_by('-referenceDate')[0]
                affected_inv = Inventory.objects.filter(Q(item__exact=ingredient) & Q(referenceDate__gt=produce.referenceDate))

                for inv in affected_inv:
                    inv.amount = inv.amount - required_amount
                    inv.save()


                ingredient_inv = Inventory(referenceDate = produce.referenceDate,
                                           item = ingredient,
                                           amount = latest_inv.amount - required_amount,
                                           note = f"[{produceItem}]생산(소비) - {required_amount}개")
                ingredient_inv.save()
            produce.save()

            latest_inv = Inventory.objects.filter(Q(referenceDate__lt=produce.referenceDate) & Q(item__exact=produceItem)).order_by('-referenceDate')[0]
            produce_inventory = Inventory(referenceDate = produce.referenceDate,
                                           item = produceItem,
                                           amount = latest_inv.amount + produce.amount,
                                           note = f"생산 - {produce.amount}개")
            produce_inventory.save()

            update_produceInv = Inventory.objects.filter(Q(item__exact = produceItem) & Q(referenceDate__gt = produce.referenceDate)).order_by('referenceDate')
            for inv in update_produceInv:
                inv.amount = inv.amount + produce.amount
                inv.save()

            return HttpResponse('<script type="text/javascript">opener.location.reload();window.close()</script>')

    else:
        form = produceForm()
    context = {'form':form,'item_node_list':item_node_list}
    return render(request,"transaction/produce/produceForm.html", context)

@login_required(login_url='common:login')
def produce_detail(request, produce_id):
    produce = get_object_or_404(Produce, pk = produce_id)
    if produce.itemNode.item.user != request.user:
        messages.error(request, "인가된 사용자가 아닙니다")
        return redirect("transaction:sellIndex")
    form = produceForm(instance=produce)
    context = {'form': form, 'produce_id':produce_id,'produce':produce}
    return render(request, 'transaction/produce/produceDetail.html', context)

@login_required(login_url='common:login')
def produce_modify(request, produce_id):
    produce = get_object_or_404(Produce, pk=produce_id)
    notModifiedDate = produce.referenceDate
    notModifiedAmount = produce.amount

    producedItem = produce.itemNode.item
    ingredientQuerySet = produce.itemNode.get_children()

    if produce.itemNode.item.user != request.user:
        messages.error(request, "인가된 사용자가 아닙니다")
        return redirect("transaction:sellIndex")
    if request.method == 'POST':
        form = produceForm(request.POST, instance = produce)
        if form.is_valid():
            modifiedProduce = form.save(commit = False)
            modifiedDate = modifiedProduce.referenceDate
            modifiedAmount = modifiedProduce.amount

            # 에러검사 1) 생산된 아이템의 inventory 의 unique 키 검사
            error_inv = Inventory.objects.filter(Q(item__exact=producedItem) & Q(referenceDate__exact=modifiedDate))
            if modifiedDate != notModifiedDate and len(error_inv) > 0:
                messages.error(request, "생산 품목에서 해당 시간에 입출고된 기록이 있습니다. 동시에 입출고를 하실 수 없으니 다시 확인해주세요.")
                return redirect("transaction:produce_modify", produce_id=produce_id)

            # 에러검사 2) 재료에 대한 unique 검사
            for node in ingredientQuerySet:
                ingredient = node.item
                error_inv = Inventory.objects.filter(Q(item__exact=ingredient) & Q(referenceDate__exact=modifiedDate))
                if modifiedDate != notModifiedDate and len(error_inv) > 0:
                    messages.error(request,
                                   f"{ingredient.name} 품목 에서 해당 시간에 입출고된 기록이 있습니다. 동시에 입출고를 하실 수 없으니 다시 확인해주세요.")
                    return redirect("transaction:produce_modify", produce_id=produce_id)

                # 에러검사 3) 재료의 modifiedDate 는 최초 입고일 이후여야 한다.
                initial_date = Inventory.objects.filter(Q(is_initial__exact=True) & Q(item__exact=ingredient))[0].referenceDate
                if modifiedDate < initial_date:
                    messages.error(request, f"재료, {ingredient.name}의 최초 등록일 이전에 생산하실 수 없습니다.")
                    return redirect("transaction:produce_modify", produce_id=produce_id)

            # 에러검사 4) 생산품의 modifiedDate 는 최초 입고일 이후여야 한다.
            initial_date = Inventory.objects.filter(Q(is_initial__exact = True) & Q(item__exact=producedItem))[0].referenceDate
            if modifiedDate < initial_date :
                messages.error(request, "생산품의 최초 등록일 이전에 생산하실 수 없습니다.")
                return redirect("transaction:produce_modify", produce_id=produce_id)

            if notModifiedDate < modifiedDate:
                '''
                1. 수정 전 날짜가 더 빠르다 : 시간 순서는 수정 전 -> 수정 후
                2. 영향권이 더 줄어든다.
                3.
                두 날짜 사이(lost_influenced_inv)에서 
                - 생산된 품목은 영향권이 줄어들었으니 수가 작아지고
                - 생산에 쓰인 소모품은 영향권이 줄어들었으니 수가 늘어난다.
                - 원래는 notModifiedAmount 의 영향을 받았는데 없어진 것임으로 이것 만큼 수가 작아지고 늘어난다.
                - notModifiedAmount은 항상 양수임으로 소모품에 대한 검사는 필요 없다.
                4. 수정 후 이후의 날짜()는 
                - notModifiedAmount, modifiedAmount 양 측에 영향을 받는다.
                - 그런데 modifiedAmount 로 영향이 수정되어야 함으로
                - 생산된 품목은 modifiedAmount - notModifiedAmount 만큼 늘어나고
                - 소모품은 modifiedAmount - notModifiedAmount 만큼 줄어든다.
                5. notModifiedDate 이전에는 바뀐 것이 없다.
                6. notModifiedDate의 Inventory 는 위의 사항을 수정한 후 modifiedDate 직전의 Inventory 를 기준으로 수정한다.
                '''
                # 1. 수량에 대한 에러 검사 시작
                lost_influenced_inv_producedItem = Inventory.objects.filter(Q(item__exact = producedItem) &
                                                               Q(referenceDate__gt = notModifiedDate) &
                                                               Q(referenceDate__lt = modifiedDate))

                modify_influence_inv_producedItem = Inventory.objects.filter(Q(item__exact = producedItem) &
                                                                Q(referenceDate__gt = modifiedDate))

                # 1) lost_influenced_inv_producedItem 에 대한 검사
                error_inv = lost_influenced_inv_producedItem.filter(amount__lt = notModifiedAmount)
                if len(error_inv) > 0:
                    messages.error(request,"생산품 수량이 부족해지는 구간이 있습니다. 날짜 혹은 수량을 다시 확인해주세요")
                    return redirect("transaction:produce_modify", produce_id=produce_id)

                # 2) modifiedAmount 에 대한 검사
                # 2-1) 생산 품목에 대한 검사
                error_inv = modify_influence_inv_producedItem.filter(amount__lt = notModifiedAmount - modifiedAmount)
                if len(error_inv) > 0:
                    messages.error(request,"생산품 수량이 부족해지는 구간이 있습니다. 날짜 혹은 수량을 다시 확인해주세요")
                    return redirect("transaction:produce_modify", produce_id=produce_id)

                check_inv = Inventory.objects.filter(Q(item__exact = producedItem) &
                                                     Q(referenceDate__lt = modifiedDate) & ~Q(referenceDate__exact =notModifiedDate)).order_by('referenceDate')[0]

                if check_inv.amount - notModifiedAmount + modifiedAmount < 0:
                    messages.error(request, "생산품 수량이 부족해지는 구간이 있습니다. 날짜 혹은 수량을 다시 확인해주세요")
                    return redirect("transaction:produce_modify", produce_id=produce_id)
                
                # 2-2) 소모품에 대한 검사
                for node in ingredientQuerySet:
                    ingredient = node.item
                    # 2-2-1) 날짜 이후 해당 소모품의 부족 검사
                    requirement_per_unit = node.required
                    error_inv = Inventory.objects.filter(Q(item__exact = ingredient) &
                                                         Q(referenceDate__gt = modifiedDate) &
                                                         Q(amount__lt = (modifiedAmount - notModifiedAmount) * requirement_per_unit))
                    if len(error_inv) > 0:
                        messages.error(request, f"{ingredient.name}의 수량이 부족해지는 구간이 있습니다. 날짜 혹은 수량을 다시 확인해주세요")
                        return redirect("transaction:produce_modify", produce_id=produce_id)
                    # 2-2-2) 날짜의 소모품의 부족 검사
                    check_inv = Inventory.objects.filter(Q(item__exact = ingredient) &Q(referenceDate__lt = modifiedDate) & ~Q(referenceDate__exact =notModifiedDate)).order_by('-referenceDate')[0]
                    if check_inv.amount + notModifiedAmount * requirement_per_unit - modifiedAmount * requirement_per_unit < 0:
                        messages.error(request, f"{ingredient.name}의 수량이 부족해지는 구간이 있습니다. 날짜 혹은 수량을 다시 확인해주세요")
                        return redirect("transaction:produce_modify", produce_id=produce_id)

                # 수량에 대한 에러 검사 끝
                
                # 2. Inventory 수정 시작
                # 2-1) 생산품 수정
                # 2-1-1) 두 날짜 사이에서 생산품이 notModifiedAmount만큼 줄어든다.
                for inv in lost_influenced_inv_producedItem:
                    inv.amount = inv.amount - notModifiedAmount
                    inv.save()

                # 2-1-2) modify 이후의 생산품이 modifiedAmount- notModifiedAmount 만큼 늘어난다.
                for inv in modify_influence_inv_producedItem:
                    inv.amount = inv.amount -notModifiedAmount + modifiedAmount
                    inv.save()

                # 2-1-3) 기존의 notModifiedDate
                latest_inventory = Inventory.objects.filter(Q(item__exact=producedItem) &
                                                            Q(referenceDate__lt=modifiedDate)).order_by('-referenceDate')[0]
                current_inventory = Inventory.objects.filter(Q(item__exact=producedItem) &
                                                             Q(referenceDate__exact = notModifiedDate))[0]

                current_inventory.amount = latest_inventory.amount + modifiedAmount
                current_inventory.note = f"생산 - {modifiedAmount}개"
                current_inventory.referenceDate = modifiedDate
                current_inventory.save()

                # 2-2) 재료 수정
                for node in ingredientQuerySet:
                    ingredient = node.item
                    requirement_per_unit = node.required

                    lost_influenced_inv_ingredient = Inventory.objects.filter(Q(item__exact = ingredient) &
                                                                              Q(referenceDate__gt = notModifiedDate) &
                                                                              Q(referenceDate__lt = modifiedDate))

                    modify_influence_inv_ingredient = Inventory.objects.filter(Q(item__exact = ingredient) &
                                                                               Q(referenceDate__gt = modifiedDate))

                    for inv in lost_influenced_inv_ingredient:
                        inv.amount = inv.amount + notModifiedAmount * requirement_per_unit
                        inv.save()

                    for inv in modify_influence_inv_ingredient:
                        inv.amount = inv.amount + notModifiedAmount * requirement_per_unit - modifiedAmount * requirement_per_unit
                        inv.save()

                    latest_inventory = Inventory.objects.filter(Q(item__exact=ingredient) &
                                                                Q(referenceDate__lt=modifiedDate) &
                                                                ~Q(referenceDate__exact =notModifiedDate)).order_by('-referenceDate')[0]
                    current_inventory = Inventory.objects.filter(Q(item__exact=ingredient) &
                                                                 Q(referenceDate__exact = notModifiedDate))[0]

                    current_inventory.amount = latest_inventory.amount - modifiedAmount * requirement_per_unit
                    print(current_inventory.amount)
                    print(latest_inventory.amount)
                    print(latest_inventory.referenceDate)
                    current_inventory.note = f"[{producedItem}]생산(소비) - {modifiedAmount * requirement_per_unit}개"
                    current_inventory.referenceDate = modifiedDate
                    current_inventory.save()
                # 2. Inventory 수정 끝

                # 3. Produce 수정
                modifiedProduce.save()
                return HttpResponse('<script type="text/javascript">alert("수정 성공");opener.location.reload();window.close()</script>')
            elif modifiedDate < notModifiedDate:
                '''
                1. 수정 후 날짜가 더 빠르다 : 시간 순서는 수정 후 -> 수정 전
                2. 영향권이 더 늘어난다
                3. 두 날짜 사이(expand_influence)에서 
                - 생산된 품목은 영향권이 늘어났으니 수가 modifiedAmount 만큼 많아지고
                - 생산에 쓰인 소모품은 영향권이 늘어났으니 modifiedAmount 만큼 수가 줄어든다. (검사필)
                4. 수정 전 이후의 날짜(original_influecne)는 
                - notModifiedAmount, modifiedAmount 양 측에 영향을 받는다.
                - 그런데 modifiedAmount 로 영향이 수정되어야 함으로
                - 생산된 품목은 modifiedAmount - notModifiedAmount 만큼 늘어나고
                - 소모품은 modifiedAmount - notModifiedAmount 만큼 줄어든다.
                5. ModifiedDate 이전에는 바뀐 것이 없다.
                6. notModifiedDate의 Inventory 는 위의 사항을 수정한 후 modifiedDate 직전의 Inventory 를 기준으로 수정한다.
                '''
                # 1. Inventory 검사 시작
                # 1) 생산품 검사 시작
                total_Inv_producedItem = Inventory.objects.filter(item__exact = producedItem)
                expand_influence_producedItem = total_Inv_producedItem.filter(Q(referenceDate__gt = modifiedDate) &
                                                                              Q(referenceDate__lt = notModifiedDate))
                original_influence_producedItem = total_Inv_producedItem.filter(Q(referenceDate__gt = notModifiedDate))

                # 1-1) 두 기간 사이의 검사 --> 늘어난 것이니 검사 필요 X
                # 1-2) 원래 영향을 받던 곳의 검사
                error_inv = original_influence_producedItem.filter(amount__lt = notModifiedAmount - modifiedAmount)
                if len(error_inv) > 0:
                    messages.error(request, "생산품 수량이 부족해지는 구간이 있습니다. 날짜 혹은 수량을 다시 확인해주세요")
                    return redirect("transaction:produce_modify", produce_id=produce_id)
                # 1-3) modifiedDate 의 검사 --> 늘어난 것이니 검사 필요 X

                # 2) 소모품 검사 시작
                for node in ingredientQuerySet:
                    ingredient = node.item
                    requirement_per_unit = node.required

                    total_inv_ingredient = Inventory.objects.filter(item__exact = ingredient)
                    expand_influence_ingredient = total_inv_ingredient.filter(Q(referenceDate__gt = modifiedDate) &
                                                                              Q(referenceDate__lt = notModifiedDate))
                    original_influence_ingredient = total_inv_ingredient.filter(Q(referenceDate__gt = notModifiedDate))

                    # 2-1) 두 기간 사이의 검사
                    error_inv = expand_influence_ingredient.filter(amount__lt = modifiedAmount * requirement_per_unit)
                    if len(error_inv) > 0:
                        messages.error(request, f"{ingredient.name}의 수량이 부족해지는 구간이 있습니다. 날짜 혹은 수량을 다시 확인해주세요")
                        return redirect("transaction:produce_modify", produce_id=produce_id)
                    # 2-2) 원래 영향을 받았던 곳의 검사
                    error_inv = original_influence_ingredient.filter(amount__lt = (modifiedAmount - notModifiedAmount) * requirement_per_unit)
                    if len(error_inv) > 0:
                        messages.error(request, f"{ingredient.name}의 수량이 부족해지는 구간이 있습니다. 날짜 혹은 수량을 다시 확인해주세요")
                        return redirect("transaction:produce_modify", produce_id=produce_id)
                    # 2-3) modifiedDate 의 검사
                    latest_inv = total_inv_ingredient.filter(Q(referenceDate__lt = modifiedDate) & ~Q(referenceDate__exact =notModifiedDate)).order_by('-referenceDate')[0]
                    if latest_inv.amount - modifiedAmount * requirement_per_unit < 0:
                        messages.error(request, f"{ingredient.name}의 수량이 부족해지는 구간이 있습니다. 날짜 혹은 수량을 다시 확인해주세요")
                        return redirect("transaction:produce_modify", produce_id=produce_id)
                # 1. Inventory 검사 끝

                # 2. Inventory 수정 시작
                # 1) 생산품 수정
                # 1-1) 두 기간 사이의 생산품 수정
                for inv in expand_influence_producedItem:
                    inv.amount = inv.amount + modifiedAmount
                    inv.save()

                # 1-2) 원래 영향을 받았던 기간의 생산품 수정
                for inv in original_influence_producedItem:
                    inv.amount = inv.amount + modifiedAmount - notModifiedAmount
                    inv.save()

                # 1-3) notModifiedDate 에 있는 inventory 를 modifiedDate 로 옮긴다.
                latest_inv = total_Inv_producedItem.filter(Q(referenceDate__lt = modifiedDate) & ~Q(referenceDate__exact =notModifiedDate)).order_by('-referenceDate')[0]
                current_inv = total_Inv_producedItem.filter(referenceDate__exact = notModifiedDate)[0]

                current_inv.referenceDate = modifiedDate
                current_inv.amount = latest_inv.amount + modifiedAmount
                current_inv.note = f"생산 - {modifiedAmount}개"
                current_inv.save()

                # 2) 소모품 수정
                for node in ingredientQuerySet:
                    ingredient = node.item
                    requirement_per_unit = node.required

                    total_inv_ingredient = Inventory.objects.filter(item__exact = ingredient)
                    expand_influence_ingredient = total_inv_ingredient.filter(Q(referenceDate__gt=modifiedDate) &
                                                                              Q(referenceDate__lt=notModifiedDate))
                    original_influence_ingredient = total_inv_ingredient.filter(Q(referenceDate__gt=notModifiedDate))
                    # 2-1) 두 기간 사이의 Inventory 수정
                    for inv in expand_influence_ingredient:
                        inv.amount = inv.amount - modifiedAmount * requirement_per_unit
                        inv.save()

                    # 2-2) 원래 영향을 받았던 곳 수정
                    for inv in original_influence_ingredient:
                        inv.amount = inv.amount - modifiedAmount * requirement_per_unit + notModifiedAmount * requirement_per_unit
                        inv.save()

                    # 2-2) notModifiedDate 에 있는 inventory 를 modifiedDate 로 옮긴다.
                    latest_inv = total_inv_ingredient.filter(Q(referenceDate__lt=modifiedDate) & ~Q(referenceDate__exact =notModifiedDate)).order_by('-referenceDate')[0]
                    current_inv = total_inv_ingredient.filter(referenceDate__exact=notModifiedDate)[0]

                    current_inv.referenceDate = modifiedDate
                    current_inv.amount = latest_inv.amount - modifiedAmount * requirement_per_unit
                    current_inv.note = f"[{producedItem}]생산(소비) - {modifiedAmount * requirement_per_unit}개"
                    current_inv.save()

                # 2. Inventory 수정 끝
                # 3. Produce 수정
                modifiedProduce.save()
                return HttpResponse('<script type="text/javascript">alert("수정 성공");opener.location.reload();window.close()</script>')
            else:
                '''
                1. 수정 전후의 날짜가 같다 (수량만 바뀌었다)
                2. 수량 체크만 해주면 된다.
                '''
                # 1. 수량 체크
                # 1-1) 생산품
                total_Inv_producedItem = Inventory.objects.filter(item__exact=producedItem)
                affected_producedItem = total_Inv_producedItem.filter(referenceDate__gte = modifiedDate)

                error_inv = affected_producedItem.filter(amount__lt = notModifiedAmount - modifiedAmount)
                if len(error_inv) > 0:
                    messages.error(request, "생산품 수량이 부족해지는 구간이 있습니다. 날짜 혹은 수량을 다시 확인해주세요")
                    return redirect("transaction:produce_modify", produce_id=produce_id)

                # 1-2) 소모품
                for node in ingredientQuerySet:
                    ingredient = node.item
                    requirement_per_unit = node.required

                    total_inv_ingredient = Inventory.objects.filter(item__exact = ingredient)
                    affected_ingredient = total_inv_ingredient.filter(referenceDate__gte = modifiedDate)

                    error_inv =affected_ingredient.filter(amount__lt = (modifiedAmount - notModifiedAmount) * requirement_per_unit)
                    if len(error_inv) > 0:
                        messages.error(request, "생산품 수량이 부족해지는 구간이 있습니다. 날짜 혹은 수량을 다시 확인해주세요")
                        return redirect("transaction:produce_modify", produce_id=produce_id)

                # 2. Inventory 수정
                # 2-1) 생산품 수정
                for inv in affected_producedItem:
                    inv.amount = inv.amount - notModifiedAmount + modifiedAmount
                    if inv.referenceDate == modifiedDate:
                        inv.note = f"생산 - {modifiedAmount}개"
                    inv.save()

                # 2-2) 소모품 수정
                for node in ingredientQuerySet:
                    ingredient = node.item
                    requirement_per_unit = node.required

                    total_inv_ingredient = Inventory.objects.filter(item__exact=ingredient)
                    affected_ingredient = total_inv_ingredient.filter(referenceDate__gte=modifiedDate)

                    for inv in affected_ingredient:
                        inv.amount = inv.amount + (notModifiedAmount - modifiedAmount) * requirement_per_unit
                        if inv.referenceDate == modifiedDate:
                            inv.note = f"[{producedItem}]생산(소비) - {modifiedAmount * requirement_per_unit}개"
                        inv.save()
                # 3. Produce 저장
                modifiedProduce.save()
                return HttpResponse('<script type="text/javascript">alert("수정 성공");opener.location.reload();window.close()</script>')

    else:
        form = produceForm(instance = produce)

    allNode = list(Node.objects.filter(item__user__exact = request.user))
    item_node_list = list()
    for node in allNode:
        if node.is_leaf() == False:
            item_node_list.append(node)
    context = {'form':form, 'produce_id':produce_id,'item_node_list':item_node_list,'produce':produce}
    return render(request,"transaction/produce/produceForm.html", context)

@login_required(login_url='common:login')
def produce_delete(request, produce_id):
    produce = get_object_or_404(Produce, pk = produce_id)
    if produce.itemNode.item.user != request.user:
        messages.error(request, "인가된 사용자가 아닙니다")
        return redirect("transaction:sellIndex")
    '''
    삭제하는 것 = 영향력이 사라진다
    -> 생산품은 줄어들고 소모품은 늘어난다
    -> 생산품에 대해서만 수량 조사를 한다.
    '''
    delete_date = produce.referenceDate
    delete_amount = produce.amount

    check_inv = Inventory.objects.filter(Q(item__exact = produce.itemNode.item) & Q(referenceDate__gt = delete_date))
    error_inv = check_inv.filter(amount__lt = delete_amount)
    if len(error_inv) >0:
        messages.error(request, "생산품 수량이 부족해지는 구간이 있습니다. 날짜 혹은 수량을 다시 확인해주세요")
        return redirect("transaction:produce_detail", produce_id=produce_id)

    # Inventory 삭제
    # 1) 생산품 삭제
    for inv in check_inv:
        inv.amount = inv.amount - delete_amount
        inv.save()
    Inventory.objects.filter(Q(item__exact = produce.itemNode.item) & Q(referenceDate__exact = delete_date)).delete()
    # 2) 소모품 삭제
    ingredient_queryset = produce.itemNode.get_children()
    for node in ingredient_queryset:
        ingredient = node.item
        requirement_per_unit = node.required

        delete_inv = Inventory.objects.filter(Q(item__exact = ingredient) & Q(referenceDate__exact = delete_date))
        check_inv = Inventory.objects.filter(Q(item__exact=ingredient) & Q(referenceDate__gt =delete_date))
        for inv in check_inv:
            inv.amount = inv.amount + delete_amount * requirement_per_unit
            inv.save()
        delete_inv.delete()

    # produce 삭제
    produce.delete()
    return HttpResponse('<script type="text/javascript"> alert("삭제 성공");opener.location.reload();window.close()</script>')





