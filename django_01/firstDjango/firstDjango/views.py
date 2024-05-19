from django.http import HttpResponse
from django.shortcuts import render

def index(req):
    # return HttpResponse("Hello, User.<br/>Welcome to our website !")
    return render(req, 'pages/index.html')

def about(req):
    # return HttpResponse("This is about page")
    return render(req, 'pages/about.html')

def contact(req):
    # return HttpResponse("This is contact page")
    return render(req, 'pages/contact.html')