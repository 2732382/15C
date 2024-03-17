#It's platonic in here
from django import forms
from renova.models import User, UserProfile, Group, Log, Activity

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


class LogForm(forms.ModelForm):
    water = forms.IntegerField(required=False, initial=0)
    calories = forms.IntegerField(required=False, initial=0)
    sleep = forms.IntegerField(required=False, initial=0)

    class Meta:
        model = Log
        fields = ['water', 'calories', 'sleep']


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'duration']