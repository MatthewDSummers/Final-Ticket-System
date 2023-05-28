
from .models import User
from django.shortcuts import redirect
from django.urls import reverse

def user_level_required(*levels):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if 'user_id' in request.session:
                user = User.objects.get(id=request.session['user_id'])
                if user and user.level in levels:
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect(reverse('ticket-easy:new-ticket-page'))
            else:
                return redirect(reverse('login-app:login-page'))
        return wrapper
    return decorator

def get_user(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        return user
    else:
        return None

def if_not_logged_in(view_func):
    def wrapper(request, *args, **kwargs):
        if not get_user(request):
            return view_func(request, *args, **kwargs)
        else:
            print("we have a user")
            if get_user(request).level in [8,9]:
                return redirect(reverse('ticket-easy:dashboard'))
            else:
                return redirect(reverse('ticket-easy:new-ticket-page'))
    return wrapper