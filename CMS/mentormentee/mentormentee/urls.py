from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name='welcome_page'),
    path('account/login/', views.login, name='login_page'),
    path('account/register/', views.register, name='register_page'),
    path('mentor/mentorRegister/', views.mentorRegister, name='mentor_register'),
    path('mentee/menteeRegister/', views.menteeRegister, name='mentee_register'),
]