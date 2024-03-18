from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import User, Group 
from .forms import GroupForm, LogForm, ActivityForm, CommentForm
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages

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
    context_dict = {}

    context_dict['mission_summary'] = """At Renova, our mission is to empower individuals to take control of their health and wellbeing. 
    We believe that optimal health is a holistic endeavor, encompassing not just physical fitness, but also mental and emotional wellbeing.
    We aim to provide a platform where users can seamlessly log and monitor their daily activities, calories, hydration, and sleep. 

    Our personalized daily milestones are designed to help users achieve their targeted goals and desired physique.
    But we're not just about individual health. We understand the power of community in promoting wellbeing. 
    That's why we've created Groups, a space where users can share activity guides and support each other on their health journeys.

    We're also committed to providing tools for users to visualize their overall wellbeing through a holistic scoring system. 
    This allows users to track their progress and see the impact of their efforts in real-time.
    In addition, we recognize the importance of adaptability in health and fitness. 
    That's why we offer activity recommendations that align with users' objectives, whether they're looking to lose weight, gain weight, or maintain their current physique.

    At Renova, we're not just building a platform, we're building a community. 
    A community that supports, encourages, and empowers each other to achieve optimal health. 
    Join us on this journey to holistic wellbeing. Together, we can achieve more."""
    # Replace newlines with <br>
    context_dict['mission_summary'] = context_dict['mission_summary'].replace('\n', '<br />')

    context_dict['enquiries_email'] = "enquiries@renova.com"
    context_dict['partnerships_email'] = "partnerships@renova.com"
    context_dict['phone_number'] = "+44 7123456789"

    context_dict['youtube'] = "youtube.com/renova"
    context_dict['facebook'] = "facebook.com/renova"
    context_dict['instagram'] = "instagram.com/renova"
    context_dict['twitter'] = "twitter.com/renova"

    return render(request, 'renova/about_us.html', context=context_dict)


@login_required
def my_logs(request):
    return render(request, 'renova/my_logs.html')


@login_required
def record_log(request):

    if request.method == 'POST':
        log_form = LogForm(request.POST)
        activity_form = ActivityForm(request.POST)

        if log_form.is_valid():
            log = log_form.save(commit=False)
            log.user = request.user 
            log.creation_date = timezone.now()  # Set the creation date to the current date
            log.save()

            # Check if any fields in the activity form are filled out
            if any(value for value in activity_form.data.values()):
                # If any fields are filled out, validate all fields
                if activity_form.is_valid():
                    activity = activity_form.save(commit=False)
                    activity.log = log
                    activity.save()
                    log.total_duration += activity.duration  # Add the duration of the activity to the total duration
                    log.save()
                else:
                    # If the form is not valid, return an error
                    return render(request, 'renova/record_log.html', 
                                  {'log_form': log_form, 'activity_form': activity_form, 'error': 'All fields in the activity form must be filled out.'})
            return redirect(reverse('my_logs'))
    else:
        log_form = LogForm()
        activity_form = ActivityForm()

    return render(request, 'renova/record_log.html', {'log_form': log_form, 'activity_form': activity_form})


@login_required
def my_account(request):
    return render(request, 'renova/my_account.html')


def groups(request):
    popular_groups_list = Group.objects.order_by('members')[:5]
    newest_groups_list = Group.objects.order_by('creation_date')[:5]

    context_dict = {}
    context_dict['make_group_summary'] = "placeholder (make-group summary)"
    return render(request, 'renova/groups.html', context=context_dict)


def group(request, group_name_slug=None):
    context_dict = {}
    
    try:
        group = Group.objects.get(slug=group_name_slug)
        context_dict['group'] = group
        context_dict['form'] = CommentForm()

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.group = group
                comment.user = request.user
                comment.save()
                return redirect(reverse('renova:group', kwargs={'group_name_slug': group.slug}))

    except Group.DoesNotExist:
        context_dict['group'] = None

    if group_name_slug:
        return render(request, 'renova/group.html', context_dict)
    else:
        # Handle the case where group_name_slug is not provided
        return HttpResponse("Group not found")


@login_required
def make_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            new_group = form.save(commit=False)
            # Check if a group with the same name already exists
            if Group.objects.filter(name=new_group.name).exists():
                # If it does, inform the user and ask them to provide a different name
                messages.error(request, "A group with this name already exists. Please provide a different name.")
            else:
                # If it doesn't, create the new group
                new_group.admin = request.user
                new_group.creation_date = timezone.now()
                new_group.save()
                return redirect(reverse('renova:group', kwargs={'group_name_slug': new_group.slug}))
    else:
        form = GroupForm()
    return render(request, 'renova/make_group.html', {'form': form})