from django import forms
from .models import User, Post


# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['nickname', 'kakao_id', 'address']

#     def signup(self, request, user):
#         user.nickname = self.cleaned_data['nickname']
#         user.kakao_id = self.cleaned_data['kakao_id']
#         user.address = self.cleaned_data['address']
#         user.save()


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'item_price',
            'item_condition',
            'item_details',
            'image1',
            'image2',
            'image3',
        ]
        widgets = {
            'item_condition':forms.RadioSelect,
        }
        

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'item_price',
            'item_condition',
            'item_details',
            'image1',
            'image2',
            'image3',
            'is_sold',
        ]
        widgets = {
            'item_condition':forms.RadioSelect,
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'profile_pic',
            'nickname',
            'kakao_id',
            'address',
        ]