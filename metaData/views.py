from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *

@login_required(login_url='common:login')
def endItemIndex(request):
    page = request.GET.get('page',1) # 페이지
    kw = request.GET.get('kw','') #검색어
    endItem_list = Item.objects.filter(Q(is_endItem__exact = True) & Q(user__exact = request.user)).order_by('registration_date')

    if kw:
        endItem_list = endItem_list.filter(
            Q(code__icontains= kw) |
            Q(name__icontains=kw) |
            Q(note__icontains=kw)
        ).distinct()

    paginator = Paginator(endItem_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'endItem_list' : page_obj, 'page':page, 'kw':kw}
    return render(request, 'metaData/endItemIndex.html', context)

