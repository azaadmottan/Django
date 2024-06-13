from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='web_admin_dashboard'),
    path('logout_web_admin/', views.logout_user, name='logout_web_admin'),
]
