from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from mentormentee.decorators import web_admin_required
from django.contrib.auth.models import User
from mentormentee.models import WebAdminProfile, MentorProfile, MenteeProfile, MenteeQuery, Notification
import os
from django.conf import settings

# Create your views here.

@login_required(login_url='login_page')
@web_admin_required
def index(request):
    return render(request, 'web_admin/dashboard.html')

def get_profile_picture(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'GET':
        try:
            web_admin = get_object_or_404(WebAdminProfile, username=request.user.id)
            profile_picture = web_admin.profile_picture.url
            return JsonResponse({
                'status': 200,
                'profile_picture': profile_picture,
                'message': 'Profile picture fetched successfully',
                'process':'success'
            })
        except:
            return JsonResponse({
                'status': 404,
                'message': 'Web admin has no profile picture.',
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
            web_admin = get_object_or_404(WebAdminProfile, username=request.session.get('user_id'))

            # Check if there is an existing profile picture and delete it
            if web_admin.profile_picture:
                old_picture_path = os.path.join(settings.MEDIA_ROOT, web_admin.profile_picture.name)
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)

            web_admin.profile_picture = profile_picture
            web_admin.save()

            return JsonResponse({
                'status': 200,
                'message': 'Web admin profile picture updated successfully',
                'process':'success'
            })
        except:
            return JsonResponse({
                'status': 404,
                'message': 'Web admin profile not found',
                'process': 'failed'
            })

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
        web_admin = get_object_or_404(WebAdminProfile, username=request.session.get('user_id'))

        user.first_name = firstName
        user.last_name = lastName
        web_admin.dob = dob
        web_admin.phone = phone

        user.save()
        web_admin.save()

        return JsonResponse({
            'status': 200,
            'message': 'Web admin personal information updated successfully',
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
            web_admin = get_object_or_404(WebAdminProfile, username=request.session.get('user_id'))
            web_admin.address = address
            web_admin.city = city
            web_admin.region = region
            web_admin.postal_code = postCode
            web_admin.nationality = nation

            web_admin.save()

            return JsonResponse({
                'status': 200,
                'message': 'Web admin profile location updated successfully',
                'process':'success'
            })

        except WebAdminProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Web admin profile not found',
                'process': 'failed'
            })

def update_web_admin_password(request):
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
            if not mentor_id:
                return JsonResponse({
                    'status': 400,
                    'message': 'Mentor ID is required',
                    'process': 'failed'
                })
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

def get_mentees(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")
    
    if request.method == 'POST':
        try:
            mentees = User.objects.filter(
                mentee_profile__user_type='mentee'
            )

            mentees_data = list(mentees.values(
                'id',
                'mentee_profile__id',
                'username',
                'first_name',
                'last_name',
                'mentee_profile__roll_no',
                'mentee_profile__branch',
                'mentee_profile__semester',
                'mentee_profile__phone',
                'mentee_profile__created_at',
            ))
            
            return JsonResponse({
                'status': 200,
                'message': 'Mentees fetched successfully',
                'data': mentees_data,
                'process':'success'
            })
        except MenteeProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Mentees not found',
                'process': 'failed'
            })
    else:
        return JsonResponse({
            'status': 405,
            'message': 'Method not allowed',
            'process': 'failed'
        })

def get_mentee_profile(request):
    if request.headers.get('x-requested-with')!= 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")
    
    if request.method == 'POST':
        try:
            mentee_id = request.POST.get('menteeId')

            if not mentee_id:
                return JsonResponse({
                    'status': 400,
                    'message': 'Mentee ID is required',
                    'process': 'failed'
                })
            mentee = User.objects.get(id=mentee_id)
            mentee_profile = get_object_or_404(MenteeProfile, username=mentee)
            
            mentee_data = {
                'first_name': mentee.first_name or '',
                'last_name': mentee.last_name or '',
                'username': mentee.username,
                'email': mentee.email or '',
                'mentor': str(mentee_profile.mentor.username) if mentee_profile.mentor is not None else 'No mentor has been allocated yet.',
                'user_role': mentee_profile.user_type or '',
                'roll_no': mentee_profile.roll_no or '',
                'branch': mentee_profile.branch or '',
                'semester': mentee_profile.semester or '',
                'phone': mentee_profile.phone or '',
                'dob': mentee_profile.dob or '',
                'father_name': mentee_profile.father_name or '',
                'father_phone': mentee_profile.father_phone or '',
                'father_profession': mentee_profile.father_profession or '',
                'address': mentee_profile.address or '',
                'city': mentee_profile.city or '',
                'region': mentee_profile.region or '',
                'pin_code': mentee_profile.postal_code or '',
                'nation': mentee_profile.nationality or '',
            }

            return JsonResponse({
                'status': 200,
                'message': 'Mentee profile fetched successfully',
                'data': mentee_data,
                'process':'success'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Mentee user not found',
                'process': 'failed'
            })
        except MenteeProfile.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Mentee profile not found',
                'process': 'failed'
            })
    else:
        return JsonResponse({
            'status': 405,
            'message': 'Method not allowed',
            'process': 'failed'
        })

@web_admin_required
def queries(request):
    return render(request, 'web_admin/query.html')

def get_query(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")

    if request.method == 'POST':
        query = MenteeQuery.objects.filter().order_by('-created_at')
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

def delete_query(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")
    
    if request.method == 'POST':
        query_id = request.POST.get('queryId')
        
        if not query_id:
            return JsonResponse({
                'status': 400,
                'message': 'Query ID is required',
                'process': 'failed'
            })
        
        query = MenteeQuery.objects.get(id=query_id)
        
        if not query:
            return JsonResponse({
                'status': 404,
                'message': 'Query not found',
                'process': 'failed'
            })
        
        query.delete()
        
        return JsonResponse({
            'status': 200,
            'message': 'Query deleted successfully',
            'process':'success'
        })
    else:
        return JsonResponse({
            'status': 405,
            'message': 'Method not allowed',
            'process': 'failed'
        })

def add_notification(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        notification_type = request.POST.get('notificationType')

        if not title or not description or not notification_type:
            return JsonResponse({
                'status': 400,
                'message': 'Title, description, and notification type must be provided',
                'process': 'failed'
            })
        
        notification = Notification(
            title=title,
            description=description,
            user_notification_type=notification_type,
        )
        notification.save()
        
        return JsonResponse({
            'status': 200,
            'message': f'Notification added successfully for {notification_type} users.',
            'process':'success'
        })
    else:
        return JsonResponse({
            'status': 405,
            'message': 'Method not allowed',
            'process': 'failed'
        })

def get_notifications(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")
    
    if request.method == 'POST':
        notifications = Notification.objects.all()

        if not notifications:
            return JsonResponse({
                'status': 404,
                'message': 'No notification found',
                'process': 'failed'
            })

        notification_data = list(notifications.values(
            'id',
            'title',
            'description',
            'user_notification_type',
            'created_at',
            'updated_at',
        ))
        
        return JsonResponse({
            'status': 200,
            'data': notification_data,
            'message': 'Notifications fetched successfully',
            'process':'success'
        })
    else:
        return JsonResponse({
            'status': 405,
            'message': 'Method not allowed',
            'process': 'failed'
        })

def remove_notification(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest("<h2>You do not have permission to access this endpoint.</h2>")
    
    if request.method == 'POST':
        notification_id = request.POST.get('notificationId')

        if not notification_id:
            return JsonResponse({
                'status': 400,
                'message': 'Notification ID is required',
                'process': 'failed'
            })
        
        notification = Notification.objects.get(id=notification_id)
        
        if not notification:
            return JsonResponse({
                'status': 404,
                'message': 'Notification not found',
                'process': 'failed'
            })
        
        notification.delete()
        
        return JsonResponse({
            'status': 200,
            'message': 'Notification removed successfully',
            'process':'success'
        })
    else:
        return JsonResponse({
            'status': 405,
            'message': 'Method not allowed',
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