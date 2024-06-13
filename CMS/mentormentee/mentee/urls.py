from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.index, name='mentee_dashboard'),
    path('logout/', views.logout_user, name='logout_mentee'),
]
