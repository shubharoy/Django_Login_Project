from django.urls import path
from . import views

app_name = "loginapp"
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('requestLogin', views.requestLogin, name='requestLogin'),
    path('logoutUser', views.logoutUser, name="logout-user"),
    path('userindex', views.userindex, name='userindex'),
    path('change-password', views.changepassword, name='change-password'),
    path('forgotpassword', views.ForgotPassword, name="forgotpassword"),
] 
 