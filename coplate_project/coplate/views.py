from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress
from allauth.account.views import PasswordChangeView
from coplate.models import Review, User
from coplate.forms import ReviewForm, ProfileForm
from coplate.functions import confirmation_required_redirect


# Create your views here.
class IndexView(ListView):
    model = Review # 가저올 정보
    template_name = 'coplate/index.html' # 내보낼 template
    context_object_name = 'reviews' 
    paginate_by = 4 # 페이지 수 
    ordering = ['-dt_created'] # 내림차순


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'coplate/review_detail.html'
    pk_url_kwarg = 'review_id'


# 왼쪽에서 오른쪽 순서로 진행되기 때문에 Mixin이 먼저 실행될 수 있도록 왼쪽에 작성 (로그인 여부, 특정조건 충족 여부, 제너릭 뷰)
class ReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'coplate/review_form.html'
    
    # 유저 이메일 인증 확인 여부에 따라 로그인 페이지 또는 인증 알림 페이지로 이동
    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect
    
    # 리뷰 작성시 author 필드의 값들을 자동으로 들어갈 수 있게 설정
    # form_valid 메소드 - 폼 데이터를 새로운 오브젝트에 저장해 주는 역할
    def form_valid(self, form):
        form.instance.author = self.request.user # author필드를 현재 유저로 설정
        return super().form_valid(form) # super()를 통해 기존의 form_valid메소드 호출
    
    # 리디렉트 페이지 설정 - 작성 완료 후 이동할 페이지
    # reverse 함수를 통해 게시글 상세 페이지의 url 리턴 이 때 파라미터가 들어가면 kwargs 옵션을 통해 넣어 줄 수 있다.
    # 생성된 게시글의 id값은 self.object로 접근하여 가져옴
    def get_success_url(self):
        return reverse('review-detail', kwargs={'review_id': self.object.id})
    
    # 이메일 인증 설정
    def test_func(self, user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'coplate/review_form.html'
    pk_url_kwarg = 'review_id'
    
    # 유저가 접근하지 못한다면 403에러창을 보여줌
    raise_exception = True
    # redirect_unauthenticated_users = False # 기본값이 False라 입력안해도됨
    
    def get_success_url(self):
        return reverse('review-detail', kwargs={'review_id': self.object.id})
    
    # UserPassesTestMixin 작성자와 유저가 같은지 확인
    def test_func(self, user):
        review = self.get_object()
        return review.author == user


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'coplate/review_confirm_delete.html'
    pk_url_kwarg = 'review_id'
    
    raise_exception = True
    
    def get_success_url(self):
        return reverse('index')
    
    def test_func(self, user):
        review = self.get_object()
        return review.author == user


# porofile
class ProfileView(DetailView):
    model = User
    template_name = 'coplate/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user' # user_id가 user라는 이름의 템플릿에 전달될 때 덮어쓰여버려서 덮어지지 않게 별도의 이름 설정
    
    # 해당 유저의 작성 리뷰를 가져오기 위해
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 기존의 context를 가져옴
        user_id = self.kwargs.get('user_id') # url로 전달되는 user_id 파라미터를 가져온다
        # 작성자 리뷰만 가져올 수 있게 리스트를 담아줌
        context['user_reviews'] = Review.objects.filter(author_id=user_id).order_by('-dt_created')[:4]
        return context


class UserReviewListView(ListView):
    moodel = Review
    template_name = 'coplate/user_review_list.html'
    context_object_name = 'user_reviews'
    paginate_by = 4
    
    # 해당 유저의 작성 게시글만 가져오기 위해 queryset 사용
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Review.objects.filter(author_id=user_id).order_by('-dt_created')
    
    # ListView를 사용하여 게시글 리스트만 전달되고 유저정보는 전달이 안되기에 context_data로 정보를 가져옴
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, id=self.kwargs.get('user_id'))
        return context


class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'coplate/profile_set_form.html'
    
    # set-prifile url에는 유저 id가 없음 그래서 UpdateView가 다룰 오브젝트를 직접 설정해주어야 함
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse('index')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'coplate/profile_update_form.html'
    
    # set-prifile url에는 유저 id가 없음 그래서 UpdateView가 다룰 오브젝트를 직접 설정해주어야 함
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})
