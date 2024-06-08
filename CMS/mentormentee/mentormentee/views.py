from django.shortcuts import render

def welcome(request):
    return render(request, 'home/welcome.html')

def login(request):
    return render(request, 'pages/login.html')

def register(request):
    return render(request, 'pages/register.html')