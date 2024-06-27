from django.http import HttpResponseForbidden
from functools import wraps

from django.shortcuts import redirect

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.session.get('user_role') == role:
                return view_func(request, *args, **kwargs)
            # return HttpResponseForbidden("You do not have permission to access this endpoint.")
            return redirect('welcome_page')
        return _wrapped_view
    return decorator

def web_admin_required(view_func):
    return role_required('web_admin')(view_func)

def mentor_required(view_func):
    return role_required('mentor')(view_func)

def mentee_required(view_func):
    return role_required('mentee')(view_func)