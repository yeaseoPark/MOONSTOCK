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
        fromDate = datetime.datetime.strptime(fromDate, "%Y-%m-%d").replace(hour=0,minute=0,second=0)
        inventory_list= inventory_list.filter(referenceDate__gte = fromDate)
        fromDate = fromDate.strftime("%Y-%m-%d")
    if toDate:
        toDate = datetime.datetime.strptime(toDate, "%Y-%m-%d").replace(hour=23,minute=59,second=59)
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
        initial_amount = request.POST['amount']
        if initial_amount:
            if before_modify > int(initial_amount):
                error_inv = Inventory.objects.filter(Q(item__exact = initial_inv.item) & Q(amount__lt = 0))
                if len(error_inv) > 0 or int(initial_amount) < 0:
                    return HttpResponse("<script type='text/javascript'>alert('음수가 되는 재고가 있습니다. 다시 확인해주세요'); window.close();</script>")
            initial_inv.amount = initial_amount
            initial_inv.save()
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
        fromDate = datetime.datetime.strptime(fromDate, "%Y-%m-%d").replace(hour=0,minute=0,second=0)
        buy_list= buy_list.filter(referenceDate__gte = fromDate)
        fromDate = fromDate.strftime("%Y-%m-%d")
    if toDate:
        toDate = datetime.datetime.strptime(toDate, "%Y-%m-%d").replace(hour=23,minute=59,second=59)
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
    delete_inv = after_refDate.filter(Q(referenceDate__exact = buy_transaction.referenceDate) & Q(amount__exact = 0))
    buy_transaction.delete()
    delete_inv.delete()
    return redirect("transaction:buyIndex")

