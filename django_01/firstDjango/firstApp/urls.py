from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('userPosts/', views.userPosts, name='userPosts'),
    path('previewPost/<int:postId>', views.previewPost, name='previewPost'),
]