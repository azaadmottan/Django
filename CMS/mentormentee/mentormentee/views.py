from django.shortcuts import render
from django.contrib.auth.models import User
from .models import WebAdminProfile, MentorProfile, MenteeProfile
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth import authenticate, login, logout

def welcome(request):
    return render(request, 'home/welcome.html')

def login_page(request):
    return render(request, 'pages/login.html')

def get_user_role(user):
    try:
        web_admin = WebAdminProfile.objects.get(username=user[0].id)
        return web_admin
    except WebAdminProfile.DoesNotExist:
        pass
    
    try:
        mentor = MentorProfile.objects.get(username=user[0].id)
        return mentor
    except MentorProfile.DoesNotExist:
        pass

    try:
        mentee = MenteeProfile.objects.get(username=user[0].id)
        return mentee
    except MenteeProfile.DoesNotExist:
        return 'Unknown'

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({
                'status': 400,
                'message': 'Username & Password must be provided',
                'process': 'failed'
            })

        user = User.objects.filter(username=username)

        if not user.exists():
            return JsonResponse({
                'status': 404,
                'message': 'Invalid user credentials ! (Wrong username)',
                'process': 'failed'
            })

        get_user = get_user_role(user)

        user = authenticate(request, username=username, password=password)

        if user is None:
            return JsonResponse({
                'status': 400,
                'message': 'Invalid user credentials! (Wrong password)',
                'process': 'failed'
            })

        login(request, user)

        user_role = get_user.user_type.lower()

        if user_role == 'web_admin':
            request.session['emp_id'] = get_user.emp_id
            request.session['phone'] = get_user.phone
            request.session['address'] = get_user.address
        elif user_role == 'mentor':
            request.session['emp_id'] = get_user.emp_id
            request.session['phone'] = get_user.phone
            request.session['address'] = get_user.address
        elif user_role == 'mentee':
            request.session['roll_no'] = get_user.roll_no
            request.session['course'] = get_user.course
            request.session['branch'] = get_user.branch
            request.session['semester'] = get_user.semester
            request.session['phone'] = get_user.phone
            request.session['address'] = get_user.address

        if request.user.is_authenticated:
            return JsonResponse({
                'status': 200,
                'message': 'Login successful',
                'user_role': user_role,
                'process': 'login success'
            })
        else:
            return JsonResponse({
                'status': 400,
                'message': 'Login failed',
                'process': 'login failed'
            })
    else:
        return JsonResponse({
            'status': 400,
            'message': 'Invalid request method',
            'process': 'failed'
        })

def register(request):
    mentors = MentorProfile.objects.all()
    return render(request, 'pages/register.html', { 'mentors': mentors })

def mentorRegister(request):
    if request.method == 'POST':
        username = request.POST.get('mentorName')
        email_id = request.POST.get('mentorEmail')
        firstName = request.POST.get('mentorFirstName')
        lastName = request.POST.get('mentorLastName')
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
        
        user = User.objects.filter(username=username)

        if user.exists():
            return JsonResponse({
                'status': 402, 
                'message':'Username already exists', 
                'process': 'failed'
            })

        if MentorProfile.objects.filter(emp_id=emp_id).exists():
            return JsonResponse({
                'status': 400   , 
                'message': 'Employee Id already exists', 
                'process': 'failed'
            })
        
        if User.objects.filter(email=email_id).exists():
            return JsonResponse({
                'status': 400   , 
                'message': 'Email address already exists', 
                'process': 'failed'
            })
        
        mentor = User.objects.create(username = username, email = email_id, first_name = firstName, last_name = lastName)
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
        firstName = request.POST.get('menteeFirstName')
        lastName = request.POST.get('menteeLastName')
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
            return JsonResponse({
                'status': 404, 
                'message': 'Mentor does not exist', 
                'process': 'failed'
            })

        user = User.objects.filter(username = username)

        if user.exists():
            return JsonResponse({
                'status': 402, 
                'message':'Username already exists', 
                'process': 'failed'
            })

        try: 
            if MenteeProfile.objects.filter(roll_no=roll_no).exists():
                return JsonResponse({
                'status': 400   , 
                'message': 'Roll number already exists', 
                'process': 'failed'
            })
            if User.objects.filter(email=email_id).exists():
                return JsonResponse({
                'status': 400   , 
                'message': 'Email address already exists', 
                'process': 'failed'
            })
            with transaction.atomic():
                mentee = User.objects.create(username = username, email = email_id, first_name = firstName, last_name = lastName)
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

        except Exception as e:
            return JsonResponse({
                'status': 500,
                'message': str(e),
                'process': 'failed'
            })
    else:
        return JsonResponse({
            'status': 405, 
            'message': 'Method not allowed', 
            'process': 'failed'
        })
