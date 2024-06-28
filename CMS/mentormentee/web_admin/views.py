from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from mentormentee.decorators import web_admin_required
from django.contrib.auth.models import User
from mentormentee.models import WebAdminProfile, MentorProfile, MenteeProfile, MenteeQuery

# Create your views here.

@login_required(login_url='login_page')
@web_admin_required
def index(request):
    return render(request, 'web_admin/dashboard.html')

def get_profile_data(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'POST':
        try:
            user = get_object_or_404(User, username=request.user.username)
            web_admin_profile = get_object_or_404(WebAdminProfile, username=request.session.get('user_id'))

            user_data = {
                'first_name': user.first_name or '',
                'last_name': user.last_name or '',
                'username': user.username,
                'email': user.email or ''
            }

            web_admin_profile_data = {
                'dob': web_admin_profile.dob.isoformat() if web_admin_profile.dob else '',
                'phone': web_admin_profile.phone or '',
                'address': web_admin_profile.address or '',
                'city': web_admin_profile.city or '',
                'region': web_admin_profile.region or '',
                'postal_code': web_admin_profile.postal_code or '',
                'nationality': web_admin_profile.nationality or '',
                'updated_at': (web_admin_profile.updated_at or web_admin_profile.created_at).isoformat() if web_admin_profile.updated_at else web_admin_profile.created_at.isoformat()
            }

            return JsonResponse({
                'status': 200,
                'data': {
                    'user': user_data,
                    'web_admin_profile': web_admin_profile_data
                },
                'message': 'Web admin profile data fetched successfully',
                'process':'success'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'User not found',
                'process': 'failed'
            })
        except WebAdminProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Web admin profile not found',
                'process': 'failed'
            })

@login_required(login_url='login_page')
@web_admin_required
def web_admin_profile(request):
    return render(request, 'web_admin/profile.html')

@login_required(login_url='login_page')
@web_admin_required
def web_admin_profile_settings(request):
    return render(request, 'web_admin/profile_settings.html')

@login_required(login_url='login_page')
@web_admin_required
def mentors(request):
    return render(request, 'web_admin/mentor.html')

def get_mentors(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")
    
    if request.method == 'POST':
        try:
            mentors = User.objects.filter(
                mentor_profile__user_type='mentor'
            )

            mentor_data = list(mentors.values(
                'id',
                'mentor_profile__id',
                'username',
                'first_name',
                'last_name',
                'mentor_profile__emp_id',
                'mentor_profile__department',
                'mentor_profile__phone',
                'mentor_profile__created_at',
            ))
            
            return JsonResponse({
                'status': 200,
                'message': 'Mentors fetched successfully',
                'data': mentor_data,
                'process':'success'
            })
        except MentorProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'No mentors found',
                'process': 'failed'
            })

def get_mentor_profile(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")
    
    if request.method == 'POST':
        try:
            mentor_id = request.POST.get('mentorId')
            mentor = User.objects.get(id=mentor_id)
            mentor_profile = get_object_or_404(MentorProfile, username=mentor)

            mentor_data = {
                'first_name': mentor.first_name or '',
                'last_name': mentor.last_name or '',
                'username': mentor.username,
                'email': mentor.email or '',
                'user_role': mentor_profile.user_type or '',
                'emp_id': mentor_profile.emp_id or '',
                'department': mentor_profile.department or '',
                'dob': mentor_profile.dob or '',
                'phone': mentor_profile.phone or '',
                'address': mentor_profile.address or '',
                'city': mentor_profile.city or '',
                'region': mentor_profile.region or '',
                'pin_code': mentor_profile.postal_code or '',
                'nation': mentor_profile.nationality or '',
            }

            return JsonResponse({
                'status': 200,
                'message': 'Mentor profile fetched successfully',
                'data': mentor_data,
                'process':'success'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Mentor user not found',
                'process': 'failed'
            })
        except MentorProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Mentor profile not found',
                'process': 'failed'
            })

@login_required(login_url='login_page')
@web_admin_required
def mentees(request):
    return render(request, 'web_admin/mentee.html')

@web_admin_required
def queries(request):
    return render(request, 'web_admin/query.html')


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