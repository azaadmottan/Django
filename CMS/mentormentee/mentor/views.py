from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mentormentee.models import MenteeProfile, MentorProfile, MenteeQuery
from mentormentee.decorators import mentor_required
import os
from django.conf import settings

# Create your views here.

@login_required(login_url='login_page')
@mentor_required
def index(request):
    return render(request, 'mentor/dashboard.html')

@login_required(login_url='login_page')
@mentor_required
def mentor_profile(request):
    return render(request, 'mentor/profile.html')

def get_profile_picture(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'GET':
        try:
            mentor = get_object_or_404(MentorProfile, username=request.user.id)
            profile_picture = mentor.profile_picture.url
            return JsonResponse({
                'status': 200,
                'profile_picture': profile_picture,
                'message': 'Profile picture fetched successfully',
                'process':'success'
            })
        except:
            return JsonResponse({
                'status': 404,
                'message': 'Mentor has no profile picture.',
                'process': 'failed'
            })

def update_profile_picture(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')

        if not profile_picture:
            return JsonResponse({
                'status': 400,
                'message': 'Profile picture must be provided',
                'process': 'failed'
            })
        
        try:
            mentor = get_object_or_404(MentorProfile, username=request.session.get('user_id'))

            # Check if there is an existing profile picture and delete it
            if mentor.profile_picture:
                old_picture_path = os.path.join(settings.MEDIA_ROOT, mentor.profile_picture.name)
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)

            mentor.profile_picture = profile_picture
            mentor.save()

            return JsonResponse({
                'status': 200,
                'message': 'Mentor profile picture updated successfully',
                'process':'success'
            })
        except:
            return JsonResponse({
                'status': 404,
                'message': 'Mentor profile not found',
                'process': 'failed'
            })

def get_profile_data(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'POST':
        try:
            user = get_object_or_404(User, username=request.user.username)
            mentor_profile = get_object_or_404(MentorProfile, username=request.session.get('user_id'))

            user_data = {
                'first_name': user.first_name or '',
                'last_name': user.last_name or '',
                'username': user.username,
                'email': user.email or ''
            }

            mentor_profile_data = {
                'dob': mentor_profile.dob.isoformat() if mentor_profile.dob else '',
                'phone': mentor_profile.phone or '',
                'address': mentor_profile.address or '',
                'city': mentor_profile.city or '',
                'region': mentor_profile.region or '',
                'postal_code': mentor_profile.postal_code or '',
                'nationality': mentor_profile.nationality or '',
                'updated_at': (mentor_profile.updated_at or mentor_profile.created_at).isoformat() if mentor_profile.updated_at else mentor_profile.created_at.isoformat()
            }

            return JsonResponse({
                'status': 200,
                'data': {
                    'user': user_data,
                    'mentor_profile': mentor_profile_data
                },
                'message': 'Mentor profile data fetched successfully',
                'process':'success'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'User not found',
                'process': 'failed'
            })
        except MentorProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Mentor profile not found',
                'process': 'failed'
            })

def update_profile_info(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    firstName = request.POST.get('first_name')
    lastName = request.POST.get('last_name')
    dob = request.POST.get('dob')
    phone = request.POST.get('phone_number')

    if not firstName or not lastName or not dob or not phone:
        return JsonResponse({
            'status': 400,
            'message': 'All fields must be provided',
            'process': 'failed'
        })

    try:
        user = get_object_or_404(User, username=request.user.username)
        mentor = get_object_or_404(MentorProfile, username=request.session.get('user_id'))

        user.first_name = firstName
        user.last_name = lastName
        mentor.dob = dob
        mentor.phone = phone

        user.save()
        mentor.save()

        return JsonResponse({
            'status': 200,
            'message': 'Mentor personal information updated successfully',
            'process':'success'
        })
    except User.DoesNotExist:
        return JsonResponse({
            'status': 404,
            'message': 'User not found',
            'process': 'failed'
        })
    except MentorProfile.DoesNotExist:
        return JsonResponse({
            'status': 404,
            'message': 'Mentor profile not found',
            'process': 'failed'
        })
    except Exception as e:
        return JsonResponse({
            'status': 404,
            'message': 'Something went wrong, while updating personal profile information',
            'process': 'failed'
        })

def update_profile_location(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")
    
    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        region = request.POST.get('region')
        postCode = request.POST.get('post_code')
        nation = request.POST.get('nation')

        if not address or not city or not region or not postCode or not nation:
            return JsonResponse({
                'status': 400,
                'message': 'All fields must be provided',
                'process': 'failed'
            })

        try:
            mentor = get_object_or_404(MentorProfile, username=request.session.get('user_id'))
            mentor.address = address
            mentor.city = city
            mentor.region = region
            mentor.postal_code = postCode
            mentor.nationality = nation

            mentor.save()

            return JsonResponse({
                'status': 200,
                'message': 'Mentor profile location updated successfully',
                'process':'success'
            })

        except MentorProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Mentor profile not found',
                'process': 'failed'
            })

@login_required(login_url='login_page')
@mentor_required
def profile_settings(request):
    return render(request,'mentor/profile_settings.html')

def update_mentor_password(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'POST':
        username = request.POST.get('username')
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmPassword')

        if not username or not oldPassword or not newPassword or not confirmPassword:
            return JsonResponse({
                'status': 400,
                'message': 'All fields must be provided',
                'process': 'failed'
            })

        if not (username == request.user.username):
            return JsonResponse({
                'status': 400,
                'message': 'Provided username is invalid. Please enter valid username',
                'process': 'failed'
            })

        try:
            user = User.objects.get(username=username)

            if not user.check_password(oldPassword):
                return JsonResponse({
                    'status': 400,
                    'message': 'Old password is incorrect',
                    'process': 'failed'
                })

            if not (newPassword == confirmPassword):
                return JsonResponse({
                    'status': 400,
                    'message': 'New password & Confirm password do not match',
                    'process': 'failed'
                })
            user.set_password(newPassword)
            user.save()
            return JsonResponse({
                'status': 200,
                'message': 'Password updated successfully',
                'process':'success'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'User not found',
                'process': 'failed'
            })

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
@mentor_required
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

@login_required(login_url='login_page')
@mentor_required
def query(request):
    return render(request, 'mentor/query.html')

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
