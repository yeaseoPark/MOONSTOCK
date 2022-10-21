from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from .models import User as U
# Create your views here.
def mainPage(request):
    if request.user:
        return redirect("metaData:endItemIndex")
    return render(request, 'common/mainPage.html')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password = raw_password)
            return redirect("common:login")
    else:
        form = UserForm()
    return render(request,'common/signUp.html',{'form':form})

@login_required(login_url='common:login')
def editMemberInfo(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            return redirect("common:editMemberInfo")
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form':form}
    return render(request,"common/signUp.html", context)