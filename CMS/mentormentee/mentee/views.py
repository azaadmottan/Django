from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mentormentee.models import MenteeQuery

# Create your views here.

@login_required(login_url='login_page')
def index(request):
    return render(request, 'mentee/dashboard.html')

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