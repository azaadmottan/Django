from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('userPosts/', views.userPosts, name='userPosts'),
    path('previewPost/<slug>/', views.previewPost, name='previewPost'),
]