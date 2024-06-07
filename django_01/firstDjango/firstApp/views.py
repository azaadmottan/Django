from django.shortcuts import render, get_object_or_404
from .models import UserPost

# Create your views here.

def home(request):
    return render(request, 'firstApp/home.html')

def userPosts(request):
    posts = UserPost.objects.all()

    return render(request, 'firstApp/userPosts.html', { 'posts': posts })

def previewPost(request, slug):
    post = get_object_or_404(UserPost, slug=slug)

    return render(request, 'firstApp/previewPost.html', { 'post': post })