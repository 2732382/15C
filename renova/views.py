from django.shortcuts import render
from .models import User, Group 

def index(request):
    return render(request, 'renova/index.html')

def faq(request):
    return render(request, 'renova/faq.html')

def about_us(request):
    return render(request, 'renova/about_us.html')

def my_logs(request):
    return render(request, 'renova/my_logs.html')

def record_log(request):
    return render(request, 'renova/record_log.html')

def my_account(request):
    return render(request, 'renova/my_account.html')

def groups(request):
    return render(request, 'renova/groups.html')

def group_detail(request, group_name_slug):
    return render(request, 'renova/group_detail.html', {'group_name_slug': group_name_slug})

def make_group(request):
    return render(request, 'renova/make_group.html')
