from django.shortcuts import render, redirect
from .models import User, Group 

def index(request):
    context_dict = {}
    context_dict['summary'] = """Welcome to Renova, your personal haven for holistic wellbeing tracking and community engagement.
    Seamlessly log and monitor your daily activities, calories, hydration, and sleep.
    Dive into Groups where users share activity guides, fostering a supportive community.
    Renova empowers you to achieve optimal health.
    With personalized daily milestones, hit your targeted goals and dream physique.
    Receive activity recommendations aligned with your objectives and engage 
    with others through Groups and interact with likes and comments."""
    # Replace newlines with <br>
    context_dict['summary'] = context_dict['summary'].replace('\n', '<br />')

    context_dict['group_summary'] = "placeholder (group summary)"
    return render(request, 'renova/index.html', context=context_dict)


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
    popular_groups_list = Group.objects.order_by('members')[:5]
    newest_groups_list = Group.objects.order_by('date')[:5]

    context_dict = {}
    context_dict['make_group_summary'] = "placeholder (make-group summary)"
    return render(request, 'renova/groups.html', context=context_dict)


def group(request, group_name_slug):
    return render(request, 'renova/groups/group.html', {'group_name_slug': group_name_slug})


def make_group(request):
    return render(request, 'renova/groups/make_group.html')
