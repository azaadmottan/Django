from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mentormentee.models import MenteeProfile, MentorProfile

# Create your views here.

@login_required(login_url='login_page')
def index(request):
    return render(request, 'mentor/dashboard.html')

def logout_user(request):
    logout(request)

    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 200,
            'message': 'Logout successful',
            'process': 'logout success'
        })
    else:
        return JsonResponse({
            'status': 400,
            'message': 'Failed to logout',
            'process': 'failed'
        })

@login_required(login_url='login_page')
def mentee(request):
    mentees = User.objects.filter(mentee_profile__user_type='mentee')

    return render(request, 'mentor/mentee.html', {'mentees': mentees})

def get_mentee_profile(request):
    if request.method == 'POST':
        mentee_id = request.POST.get('menteeId')

        if not mentee_id:
            return JsonResponse({
                'status': 400,
                'message': 'Mentee Id must be provided',
                'process': 'failed'
            })
        
        try:
            mentee = User.objects.get(id=mentee_id)
            m_profile = mentee.mentee_profile
            
            data = {
                'username': mentee.username,
                'email': mentee.email,
                'roll_no': m_profile.roll_no,
                'course': m_profile.course,
                'branch': m_profile.branch,
                'semester': m_profile.semester,
                'mentor': str(m_profile.mentor.username) if m_profile.mentor is not None else 'No mentor has been allocated yet.',
                'phone': m_profile.phone,
                'father_name': m_profile.father_name,
                'father_phone': m_profile.father_phone,
                'father_profession': m_profile.father_profession,
                'address': m_profile.address,
            }
            return JsonResponse({
                'status': 200,
                'message': 'Mentee profile data fetched successfully',
                'data': data,
                'process':'success'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Mentee does not exist',
                'process': 'failed'
            })

def get_mentees_of_mentor(request):
    if request.method == 'POST':

        try:
            mentor = MentorProfile.objects.get(username=User.objects.get(id=request.session.get('user_id')))

            mentees = MenteeProfile.objects.filter(mentor=mentor)

            mentees_data = []
            for mentee in mentees:
                mentees_data.append({
                    'id': mentee.username.id,
                    'username': mentee.username.username,  # Assuming username is the related User model
                    'roll_no': mentee.roll_no,
                    'course': mentee.course,
                    'branch': mentee.branch,
                    'semester': mentee.semester,
                    'phone': mentee.phone,
                    'address': mentee.address,
                    'mentor_username': mentor.username.username,
                })
            return JsonResponse({
                "mentees": mentees_data,
            })
        except MenteeProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'No mentee found'
            })

def add_mentee(request):
    if request.method == 'POST':
        mentee_id = request.POST.get('menteeId')

        mentor = get_object_or_404(MentorProfile, username=request.user.id)

        if not mentee_id:
            return JsonResponse({
                'status': 400,
                'message': 'Mentee Id must be provided',
                'process': 'failed'
            })

        mentee_profile = get_object_or_404(MenteeProfile, username=mentee_id)

        mentee_profile.mentor = mentor
        mentee_profile.save()

        return JsonResponse({
            'status': 200,
            'message': 'Mentee added successfully',
            'process':'success'
        })
    else:
        return JsonResponse({
            'status': 405,
            'message': 'Method not allowed',
            'process': 'failed'
        })


@login_required(login_url='login_page')
def query(request):
    return render(request, 'mentor/query.html')