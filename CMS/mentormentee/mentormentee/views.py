from django.shortcuts import render
from django.contrib.auth.models import User
from .models import MentorProfile
from django.http import JsonResponse

def welcome(request):
    return render(request, 'home/welcome.html')

def login(request):
    return render(request, 'pages/login.html')

def register(request):
    return render(request, 'pages/register.html')

def mentorRegister(request):
    if request.method == 'POST':
        username = request.POST.get('mentorName')
        email_id = request.POST.get('mentorEmail')
        password = request.POST.get('mentorPassword')
        emp_id = request.POST.get('empId')
        department = request.POST.get('department')
        phone = request.POST.get('mentorPhone')
        address = request.POST.get('mentorAddress')

        if not username or not email_id or not password or not emp_id or not department or not phone or not address:
            return JsonResponse({'status': 400, 'message': 'All fields must be provided', 'process': 'success'})
        
        user = User.objects.filter(username = username)

        if user.exists():
            return JsonResponse({'status': 400, 'message':'Username already exists', 'process': 'fail'})

        mentor = User.objects.create(username = username, email = email_id)
        mentor.set_password(password)

        mentor.save()

        mentor_profile = MentorProfile(
            username = mentor, 
            emp_id = emp_id, 
            department = department, 
            phone = phone, 
            address = address
        )

        mentor_profile.save()

        return JsonResponse({'status': 200, 'message': 'Mentor registered successfully', 'process': 'success'})
    else:
        return JsonResponse({'status': 405, 'message': 'Method not allowed', 'process': 'fail'})