from django.shortcuts import redirect
from django.urls import reverse

class PreventLoggedInUserAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths where logged-in users should not be allowed
        login_paths = [reverse('login_page'), reverse('register_page')]
        
        if request.user.is_authenticated and request.path in login_paths:
            user_role = request.session.get('user_role').lower()
            if user_role == 'web_admin':
                return redirect(reverse('web_admin_dashboard'))
            elif user_role == 'mentor':
                return redirect(reverse('mentor_dashboard'))
            elif user_role == 'mentee':
                return redirect(reverse('mentee_dashboard'))

        response = self.get_response(request)
        return response
