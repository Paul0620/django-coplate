from django.urls import reverse
from django.shortcuts import redirect

class ProfileSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if (
            request.user.is_authenticated and # 유저가 로그인 했는지
            not request.user.nickname and # 프로필 설정이 됐는지
            request.path_info != reverse('profile-set') # 유저가 어디로 reqeust를 보냈는지
        ):
            return redirect('profile-set')
        
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response