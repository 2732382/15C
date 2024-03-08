from django.shortcuts import render
from .models import User, Group 

def index(request):
    return render(request, 'renova/index.html')

def login_view(request):

    return render(request, 'login.html')

def register(request):

    user_form = UserForm()
    profile_form = UserProfileForm()

    context_dict = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'registration/register.html', context_dict)

def faq(request):

    return render(request, 'faq.html')

def about_us(request):

    return render(request, 'about_us.html')

def my_logs(request):

    return render(request, 'my_logs.html')

def record_log(request):

    return render(request, 'record_log.html')

def my_account(request):

    return render(request, 'my_account.html')

def groups(request):
    
    return render(request, 'groups.html')

def group_detail(request, group_name_slug):
    
    return render(request, 'group_detail.html', {'group_name_slug': group_name_slug})

def make_group(request):
    
    return render(request, 'make_group.html')
