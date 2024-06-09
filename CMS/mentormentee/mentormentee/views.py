from django.shortcuts import render
from django.contrib.auth.models import User
from .models import MentorProfile, MenteeProfile
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
            return JsonResponse({
                'status': 400, 
                'message': 'All fields must be provided', 
                'process': 'failed'
            })
        
        user = User.objects.filter(username = username)

        if user.exists():
            return JsonResponse({
                'status': 402, 
                'message':'Username already exists', 
                'process': 'failed'
            })

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

        return JsonResponse({
            'status': 200, 
            'message': 'Mentor registered successfully', 
            'process': 'success'
        })
    else:
        return JsonResponse({
            'status': 405, 
            'message': 'Method not allowed', 
            'process': 'failed'
        })

def menteeRegister(request):
    if request.method == 'POST':
        username = request.POST.get('menteeName')
        email_id = request.POST.get('menteeEmail')
        password = request.POST.get('menteePassword')
        roll_no = request.POST.get('roll_no')
        course = request.POST.get('course')
        branch = request.POST.get('branch')
        semester = request.POST.get('semester')
        mentor_id = request.POST.get('mentor')
        phone = request.POST.get('menteePhone')
        father_name = request.POST.get('fatherName')
        father_phone = request.POST.get('fatherPhone')
        father_profession = request.POST.get('fatherProfession')
        address = request.POST.get('menteeAddress')
        profile_picture = request.FILES.get('menteeProfilePicture')

        if not username or not email_id or not password or not roll_no or not course or not branch or not semester or not mentor_id or not phone or not father_name or not father_phone or not father_profession or not address or not profile_picture:
            return JsonResponse({
                'status': 400, 
                'message': 'All fields must be provided', 
                'process': 'failed'
            })
        
        try:
            mentor_id = MentorProfile.objects.get(id=mentor_id)
        except MentorProfile.DoesNotExist:
            return JsonResponse({'status': 404, 'message': 'Mentor does not exist', 'process': 'failed'})

        user = User.objects.filter(username = username)

        if user.exists():
            return JsonResponse({
                'status': 402, 
                'message':'Username already exists', 
                'process': 'failed'
            })

        mentee = User.objects.create(username = username, email = email_id)
        mentee.set_password(password)

        mentee.save()

        mentee_profile = MenteeProfile(
            username = mentee, 
            roll_no = roll_no, 
            course = course, 
            branch = branch, 
            semester = semester, 
            mentor = mentor_id, 
            phone = phone, 
            father_name = father_name,
            father_phone = father_phone,
            father_profession = father_profession,
            address = address,
            profile_picture = profile_picture
        )

        mentee_profile.save()

        return JsonResponse({
            'status': 200, 
            'message': 'Mentee registered successfully', 
            'process': 'success'
        })
    else:
        return JsonResponse({
            'status': 405, 
            'message': 'Method not allowed', 
            'process': 'failed'
        })
