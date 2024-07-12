from django.shortcuts import redirect
from functools import wraps

def user_is_shreeys(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.username != 'shreeys':
            return redirect('store')
        return view_func(request, *args, **kwargs)
    return _wrapped_view