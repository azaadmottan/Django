from django.http import HttpResponse

def index(req):
    return HttpResponse("Hello, User.<br/>Welcome to our website !")

def about(req):
    return HttpResponse("This is about page")

def contact(req):
    return HttpResponse("This is contact page")