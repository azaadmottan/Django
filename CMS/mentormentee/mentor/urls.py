from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='mentor_dashboard'),
    path('logout/', views.logout_user, name='logout_mentor'),
]
