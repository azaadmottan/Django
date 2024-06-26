from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mentormentee.models import MenteeProfile, MenteeQuery
import os
from django.conf import settings

# Create your views here.

@login_required(login_url='login_page')
def index(request):
    return render(request, 'mentee/dashboard.html')

@login_required(login_url='login_page')
def mentee_profile(request):
    return render(request, 'mentee/profile.html')

def get_profile_picture(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'GET':
        try:
            mentee = get_object_or_404(MenteeProfile, username=request.user.id)
            profile_picture = mentee.profile_picture.url
            return JsonResponse({
                'status': 200,
                'profile_picture': profile_picture,
                'message': 'Profile picture fetched successfully',
                'process':'success'
            })
        except:
            return JsonResponse({
                'status': 404,
                'message': 'Mentee has no profile picture.',
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
            mentee = get_object_or_404(MenteeProfile, username=request.session.get('user_id'))

            # Check if there is an existing profile picture and delete it
            if mentee.profile_picture:
                old_picture_path = os.path.join(settings.MEDIA_ROOT, mentee.profile_picture.name)
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)

            mentee.profile_picture = profile_picture
            mentee.save()

            return JsonResponse({
                'status': 200,
                'message': 'Mentee profile picture updated successfully',
                'process':'success'
            })
        except:
            return JsonResponse({
                'status': 404,
                'message': 'Mentee profile not found',
                'process': 'failed'
            })

def get_profile_data(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'POST':
        try:
            user = get_object_or_404(User, username=request.user.username)
            mentee_profile = get_object_or_404(MenteeProfile, username=request.session.get('user_id'))

            user_data = {
                'first_name': user.first_name or '',
                'last_name': user.last_name or '',
                'username': user.username,
                'email': user.email or ''
            }

            mentee_profile_data = {
                'dob': mentee_profile.dob.isoformat() if mentee_profile.dob else '',
                'phone': mentee_profile.phone or '',
                'address': mentee_profile.address or '',
                'city': mentee_profile.city or '',
                'region': mentee_profile.region or '',
                'postal_code': mentee_profile.postal_code or '',
                'nationality': mentee_profile.nationality or '',
                'updated_at': (mentee_profile.updated_at or mentee_profile.created_at).isoformat() if mentee_profile.updated_at else mentee_profile.created_at.isoformat()
            }

            return JsonResponse({
                'status': 200,
                'data': {
                    'user': user_data,
                    'mentee_profile': mentee_profile_data
                },
                'message': 'Mentee profile data fetched successfully',
                'process':'success'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'User not found',
                'process': 'failed'
            })
        except MenteeProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Mentee profile not found',
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
        mentee = get_object_or_404(MenteeProfile, username=request.session.get('user_id'))

        user.first_name = firstName
        user.last_name = lastName
        mentee.dob = dob
        mentee.phone = phone

        user.save()
        mentee.save()

        return JsonResponse({
            'status': 200,
            'message': 'Mentee personal information updated successfully',
            'process':'success'
        })
    except User.DoesNotExist:
        return JsonResponse({
            'status': 404,
            'message': 'User not found',
            'process': 'failed'
        })
    except MenteeProfile.DoesNotExist:
        return JsonResponse({
            'status': 404,
            'message': 'Mentee profile not found',
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
            mentee = get_object_or_404(MenteeProfile, username=request.session.get('user_id'))
            mentee.address = address
            mentee.city = city
            mentee.region = region
            mentee.postal_code = postCode
            mentee.nationality = nation

            mentee.save()

            return JsonResponse({
                'status': 200,
                'message': 'Mentee profile location updated successfully',
                'process':'success'
            })

        except MenteeProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Mentee profile not found',
                'process': 'failed'
            })

@login_required(login_url='login_page')
def mentee_query(request):
    return render(request, 'mentee/query.html')

def add_query(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')

        if not subject or not description:
            return JsonResponse({
                'status': 400,
                'message': 'Subject and description must be provided',
                'process': 'failed'
            })

        try:
            mentee = get_object_or_404(User, id=request.session.get('user_id'))
        except:
            return JsonResponse({
                'status': 404,
                'message': 'Mentee not found',
                'process': 'failed'
            })

        try:
            mentor = get_object_or_404(User, id=request.session.get('mentor_id'))
        except:
            return JsonResponse({
                'status': 404,
                'message': 'Mentor not found',
                'process': 'failed'
            })

        query = MenteeQuery.objects.create(
            mentee_name=mentee,
            mentor_name=mentor,
            subject=subject,
            description=description,
        )

        query.save()
        return JsonResponse({
            'status': 200,
            'message': 'Query submitted successfully',
            'process': 'success'
        })
    else:
        return JsonResponse({
            'status': 400,
            'message': 'Invalid request method',
            'process': 'failed'
        })

def get_query(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'POST':
        query = MenteeQuery.objects.filter(mentee_name=request.session.get('user_id')).order_by('-created_at')

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
            'message': 'Queries found successfully',
            'process':'success'
        })
    else:
        return JsonResponse({
            'status': 400,
            'message': 'Invalid request method',
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