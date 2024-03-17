#It's platonic in here
from django import forms
from renova.models import User, UserProfile, Group

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'activities', 'description', 'announcements', 'icon']