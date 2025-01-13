from django.shortcuts import redirect
from django.urls import reverse_lazy

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'userprofile') and request.user.userprofile.force_password_change:
                # Avoid redirect loop
                if request.path != reverse_lazy('password_change'):
                    return redirect('password_change')
        return self.get_response(request)
