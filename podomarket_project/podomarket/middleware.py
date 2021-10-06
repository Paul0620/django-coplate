from django.urls import reverse
from django.shortcuts import redirect


class ProfileSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if (
            request.user.is_authenticated and # 유저가 로그인이 돼있고, 
            not (request.user.nickname or request.user.kakao_id or request.user.address) and # 프로필을 설정하지 않았고, 
            request.path_info != reverse('profile-set') # 프로필 설정 페이지가 아닌 다른 페이지로 들어가려고 하면
        ):
            return redirect('profile-set') # 프로필 설정 페이지로 리디렉트한다.
        
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
