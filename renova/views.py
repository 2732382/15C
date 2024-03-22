from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from renova.models import *
from renova.forms import *
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count
from django.db.models import Prefetch


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

    context_dict['group_summary'] = """groups within Renova serve as hubs for knowledge sharing, 
    motivation, and collective progress. 
    Whether users want to explore new activities, seek advice, or simply connect with others, 
    participating in groups enhances their overall wellbeing journey. 
    Encourage users to explore existing groups or create their own 
    to maximize the benefits of community engagement!"""
    # Replace newlines with <br>
    context_dict['group_summary'] = context_dict['group_summary'].replace('\n', '<br />')
    
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

from django.db.models import Sum, Avg

@login_required
def my_logs(request):
    logs = Log.objects.all().filter(user=request.user).order_by("-creation_date")
    today_logs = Log.objects.all().filter(user=request.user).filter(creation_date=timezone.now())
    total_water = today_logs.aggregate(Sum('water'))['water__sum'] or 0
    total_calories = today_logs.aggregate(Sum('calories'))['calories__sum'] or 0
    total_sleep = today_logs.aggregate(Sum('sleep'))['sleep__sum'] or 0
    total_duration = today_logs.aggregate(total_duration=Sum('total_duration'))['total_duration'] or 0

    # Get the goals from the user's profile
    user_profile = UserProfile.objects.get(user=request.user)
    target_calories = user_profile.target_calories
    target_water = user_profile.target_water
    target_sleep = user_profile.target_sleep
    target_duration = user_profile.target_duration

    context_dict = {
        'logs' : logs,
        'total_water': total_water,
        'total_calories': total_calories,
        'total_sleep': total_sleep,
        'total_duration': total_duration,
        'target_calories': target_calories,
        'target_water': target_water,
        'target_sleep': target_sleep,
        'target_duration': target_duration,
    }

    return render(request, 'renova/my_logs.html', context=context_dict)


@login_required
def record_log(request):
    activity_form = ActivityForm()  # Initialize activity_form here
    if request.method == 'POST':
        log_form = LogForm(request.POST)
        if log_form.is_valid():
            log = log_form.save(commit=False)
            log.user = request.user
            log.creation_date = timezone.now()

            # If any data was entered for the activity, process the activity form
            if request.POST.get('activity_name') != "" or request.POST.get('activity_duration') != "":
                activity_form = ActivityForm(request.POST)
                if activity_form.is_valid():
                    activity = activity_form.save(commit=False)
                    log.total_duration += activity.duration
                    activity.save()
                    log.activities.add(activity)
                else:
                    messages.error(request, 'Activity form invalid.')

            log.save()
            return redirect(reverse('renova:my_logs'))
    else:
        log_form = LogForm(initial={'water': 0, 'calories': 0, 'sleep': 0})

    return render(request, 'renova/record_log.html', {'log_form': log_form, 'activity_form': activity_form})

@login_required
def my_account(request):

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if created:
        
        user_profile.picture = 'profile_images/default.jpg'
        user_profile.save()

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            
    else:
        user_profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'renova/my_account.html', {'user_profile_form': user_profile_form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        # Log the user out (optional but recommended)
        request.user.delete()  # Delete the user account
        return redirect(reverse(index))  # Redirect to the homepage

    return render(request, 'renova/delete_account.html')  # Confirmation page


def groups(request):
    popular_groups = Group.objects.annotate(num_members=Count('members')).order_by('-num_members')[:5]
    recent_groups = Group.objects.order_by('creation_date')[:5]

    context_dict = {}
    context_dict['popular_groups'] = popular_groups
    context_dict['recent_groups'] = recent_groups
    context_dict['make_group_summary'] = """Creating a group within Renova empowers you to take charge of your wellbeing journey. 
    Here's why you might want to start your own group:

    Shared Interests: Connect with others who share your passion
     — whether it's fitness, nutrition, or mindfulness.

    Accountability: Set collective goals and motivate each other to stay on track.

    Curated Content: Share valuable insights and personalized recommendations.

    Community Building: Engage in discussions and celebrate achievements together.

    Event Planning: Organize virtual meetups, challenges, and workshops.

    Safe Space: Create an inclusive environment where everyone feels welcome.
    
    Ready to inspire others? Start your group today! 🌟"""
    # Replace newlines with <br>
    context_dict['make_group_summary'] = context_dict['make_group_summary'].replace('\n', '<br />')

    return render(request, 'renova/groups.html', context=context_dict)

@login_required
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
                return redirect(reverse('renova:group', kwargs={'group_name_slug': group_name_slug}))

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
                form.save_m2m()
                return redirect(reverse('renova:group', kwargs={'group_name_slug': new_group.slug}))
    else:
        form = GroupForm()
    return render(request, 'renova/make_group.html', {'form': form})


@login_required
def leave_group(request, group_name_slug):
    try:
        group = Group.objects.get(slug=group_name_slug)
        group.members.remove(request.user)
        return redirect(reverse('renova:group', kwargs={'group_name_slug': group.slug}))
    except Group.DoesNotExist:
        return HttpResponse("Group not found")
    

@login_required
def join_group(request, group_name_slug):
    try:
        group = Group.objects.get(slug=group_name_slug)
        group.members.add(request.user)
        return redirect(reverse('renova:group', kwargs={'group_name_slug': group.slug}))
    except Group.DoesNotExist:
        return HttpResponse("Group not found")
