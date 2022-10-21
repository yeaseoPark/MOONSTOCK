from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'common'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='common/mainPage.html'), name = 'login'),
    path('signup/',views.signup, name = 'signup'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('modifyMemberInfo/', views.editMemberInfo, name = 'editMemberInfo'),
]