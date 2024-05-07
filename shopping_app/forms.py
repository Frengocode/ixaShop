from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.forms import ModelForm
from django import forms
from .models import UserProfile, CommentModel, ShopModel


class ProfileUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserProfile
        fields = ['username', 'country']


class ProductUploudForm(ModelForm):
    class Meta:
        model = ShopModel
        fields = '__all__'
        exclude = ('user', 'best_product',)

    def __init__(self, *args, user=None, **kwargs):
        super(ProductUploudForm, self).__init__(*args, **kwargs)
        self.user = user

class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ['username', 'country', 'password1', 'password2',]



class ProfilePhotoUploudForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_profile_photo']



class SerachProductForm(forms.Form):
    search  = forms.CharField(max_length=50, label='Search')

class CommentForm(ModelForm):
    class Meta:
        model = CommentModel
        fields = ['review','text']