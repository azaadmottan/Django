from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mentormentee.models import MenteeProfile, MentorProfile, MenteeQuery

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
    return render(request, 'mentor/mentee.html')

def get_mentee_profile(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

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
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'POST':

        try:
            mentor = MentorProfile.objects.get(username=User.objects.get(id=request.session.get('user_id')))

            mentees = MenteeProfile.objects.filter(mentor=mentor)

            mentees_data = []
            for mentee in mentees:
                mentees_data.append({
                    'id': mentee.username.id,
                    'profile_id': mentee.id,
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

def get_unassigned_mentees(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'POST':
        try:
            mentor = MentorProfile.objects.get(username=User.objects.get(id=request.session.get('user_id')))

            # Retrieve all mentees excluding those already assigned to the current mentor
            mentees = User.objects.filter(
                mentee_profile__user_type='mentee'
            ).exclude(mentee_profile__mentor=mentor)

            mentees_data = list(mentees.values(
                'id',
                'mentee_profile__id',
                'username',
                'mentee_profile__roll_no',
                'mentee_profile__course',
                'mentee_profile__branch',
                'mentee_profile__semester',
                'mentee_profile__phone',
                'mentee_profile__address',
                'mentee_profile__mentor__username__username'
            ))

            return JsonResponse({
                'status': 200,
                'mentees': mentees_data,
                'process': 'success'
            })

        except MenteeProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'No mentee were found',
                'process': 'failed'
            })
    else:
        return JsonResponse({
            'status': 405,
            'message': 'Method not allowed',
            'process': 'failed'
        })

def add_mentee(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

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

def remove_mentee(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'POST':
        mentee_id = request.POST.get('menteeId')

        if not mentee_id:
            return JsonResponse({
                'status': 400,
                'message': 'Mentee Id must be provided',
                'process': 'failed'
            })
        try:
            mentee_profile = get_object_or_404(MenteeProfile, username=mentee_id)

            if str(request.user.username) == str(mentee_profile.mentor.username):
                mentee_profile.mentor = None
                mentee_profile.save()
                
                return JsonResponse({
                    'status': 200,
                    'message': 'Mentee removed successfully',
                    'process':'success'
                })
            else:
                return JsonResponse({
                    'status': 403,
                    'message': 'You are not authorized to remove this mentee',
                    'process': 'failed'
                })
        except MenteeProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Mentee does not exist',
                'process': 'failed'
            })
    else:
        return JsonResponse({
            'status': 405,
            'message': 'Method not allowed',
            'process': 'failed'
        })

def get_query(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'POST':
        query = MenteeQuery.objects.filter(mentor_name=request.session.get('user_id')).order_by('-created_at')
        query_data = list(query.values(
            'id',
            'mentee_name__username',
            'mentor_name__username',
            'subject',
            'description',
            'status',
            'created_at',
            'updated_at',
        ))

        return JsonResponse({
            'status': 200,
            'data': query_data,
            'message': 'Queries fetched successfully',
            'process':'success'
        })
    else:
        return JsonResponse({
            'status': 400,
            'message': 'Invalid request method',
            'process': 'failed'
        })

def update_query_status(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")
    
    if request.method == 'POST':
        query_id = request.POST.get('queryId')
        status = request.POST.get('queryStatus')

        if not query_id or not status:
            return JsonResponse({
                'status': 400,
                'message': 'Query Id and status must be provided',
                'process': 'failed'
            })

        query = MenteeQuery.objects.get(id=query_id)

        if not query:
            return JsonResponse({
                'status': 404,
                'message': 'Query not found',
                'process': 'failed'
            })
        
        query.status = status
        query.save()

        return JsonResponse({
            'status': 200,
            'message': 'Query status updated successfully',
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