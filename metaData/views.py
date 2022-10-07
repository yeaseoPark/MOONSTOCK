from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from .forms import *

#end Item
@login_required(login_url='common:login')
def endItemIndex(request):
    page = request.GET.get('page',1) # 페이지
    kw = request.GET.get('kw','') #검색어
    endItem_list = Item.objects.filter(Q(is_endItem__exact = True) & Q(user__exact = request.user)).order_by('-registration_date')

    if kw:
        endItem_list = endItem_list.filter(
            Q(code__icontains= kw) |
            Q(name__icontains=kw) |
            Q(note__icontains=kw)
        ).distinct()

    paginator = Paginator(endItem_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'endItem_list' : page_obj, 'page':page, 'kw':kw}
    return render(request, 'metaData/endItem/endItemIndex.html', context)


@login_required(login_url='common:login')
def endItem_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            endItem = form.save(commit=False)

            if len(Item.objects.filter(Q(code__exact = endItem.code) & Q(user__exact = request.user) )) >=1:
                messages.error(request, "중복된 코드입니다. 다시 확인해주세요.")
            else:
                endItem.is_endItem = True
                endItem.user = request.user
                endItem.save()
                return redirect('metaData:endItemIndex')
    else:
        form = ItemForm()
    context = {'form':form}
    return render(request, 'metaData/endItem/endItemForm.html', context)

@login_required(login_url='common:login')
def endItem_detail(request, endItem_id):
    end_item = Item.objects.get(id = endItem_id)
    if end_item.user != request.user:
        return redirect('metaData:endItemIndex')
    context = {'end_item': end_item}
    return render(request, 'metaData/endItem/endItem_detail.html', context)

@login_required(login_url='common:login')
def endItem_modify(request,endItem_id):
    end_item = get_object_or_404(Item, pk = endItem_id)
    if end_item.user != request.user:
        messages.error(request, "부적절한 사용")
        return redirect('metaData:endItemIndex')
    if request.method == 'POST':
        form = ItemForm(request.POST, instance = end_item)
        if form.is_valid():
            endItem = form.save(commit=False)
            endItem.user = request.user
            endItem.is_endItem = True
            endItem.save()
            return redirect("metaData:endItem_detail", endItem_id = endItem_id)
    else:
        form = ItemForm(instance=end_item)
    context = {'end_item': end_item, 'form':form}
    return render(request, 'metaData/endItem/endItemForm.html', context)

@login_required(login_url='common:login')
def endItem_delete(request,endItem_id):
    endItem = get_object_or_404(Item, pk=endItem_id)
    if request.user != endItem.user:
        messages.error(request,"부적절한 사용입니다")
        return redirect('metaData:endItemIndex')
    endItem.delete()
    return redirect("metaData:endItemIndex")


'''
BOM views
'''
@login_required(login_url='common:login')
def bomIndex(request):
    endItem_list = Item.objects.filter(Q(is_endItem__exact = True) & Q(user__exact = request.user))
    bomOrderList = list()
    for endItem in endItem_list:
        bom = BOM.objects.filter(Q(end_item__exact = endItem)).order_by('level')
        bomOrderList.append(bom)

    context = {'bomOrderList' : bomOrderList}
    return render(request, 'metaData/BOM/bomIndex.html', context)






