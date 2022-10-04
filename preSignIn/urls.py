from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'preSignIn'

urlpatterns = [
    # path('', views.mainPage, name = 'mainPage'),
    path('signup/',views.signup, name = 'signup'),
    path('',auth_views.LoginView.as_view(template_name='preSignIn/mainPage.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),

]