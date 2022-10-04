from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def mainPage(request):
    return render(request, 'common/mainPage.html')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password = raw_password)
            login(request, user)
            return redirect("common:login")
    else:
        form = UserForm()
    return render(request,'common/signUp.html',{'form':form})
