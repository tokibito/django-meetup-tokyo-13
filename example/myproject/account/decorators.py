from django.http import HttpResponse
from .models import get_user_profile


def user_profile_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        user_profile = get_user_profile(request.user)
        if not user_profile:
            return HttpResponse("ユーザープロフィールがありません", status=400)
        return view_func(request, *args, **kwargs)

    return _wrapped_view_func
