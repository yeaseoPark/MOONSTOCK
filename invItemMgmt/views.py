from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *

@login_required(login_url='preSignIn:login')
def Index(request):
    page = request.GET.get('page',1) # 페이지
    endItem_list = Item.objects.filter(Q(is_endItem__exact = True) & Q(user__exact = request.user)).order_by('registration_date')
    paginator = Paginator(endItem_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'endItem_list' : page_obj}
    return render(request, 'invItemMgmt/invItemMgmt_main.html', context)

