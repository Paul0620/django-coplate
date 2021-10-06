from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_no_special_characters, validate_rastaurant_link

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        validators=[validate_no_special_characters],
        error_messages={
            'unique': '이미 사용중인 닉네임 입니다.'
        }
    )
    
    # 마이그레이션시 설정 변경에 대해 질문이 없던 이유 - 이미지에 대해선 디폴트값을 지정해 주었고, intro에선 블랭크값을 True로 지정했기 때문
    profile_pic = models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics')
    
    intro = models.CharField(max_length=60, blank=True)

    # 유저네임대신 이메일을 사용하니깐 __str__메소드의 리턴값을 email로 설정
    def __str__(self):
        return self.email


# 리뷰에 대한 모델
class Review(models.Model):
    title = models.CharField(max_length=30)
    restaurant_name = models.CharField(max_length=20)
    restaurant_link = models.URLField(validators=[validate_rastaurant_link])

    RATING_CHOICES = [
        # (실제값, 디스플레이시 사용되는 값)
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=None)

    image1 = models.ImageField(upload_to="review_pics")
    image2 = models.ImageField(upload_to="review_pics", blank=True)
    image3 = models.ImageField(upload_to="review_pics", blank=True)
    content = models.TextField()
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    # on_dalete=models.CASCADE - 작성자 삭제시 게시글도 같이 삭제
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
