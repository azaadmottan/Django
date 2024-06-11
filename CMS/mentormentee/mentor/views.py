from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

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