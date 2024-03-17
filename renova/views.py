from datetime import timezone
from django.shortcuts import render, redirect
from .models import User, Group 
from .forms import GroupForm, LogForm, ActivityForm

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
            return redirect('my_logs')
    else:
        log_form = LogForm()
        activity_form = ActivityForm()

    return render(request, 'renova/record_log.html', {'log_form': log_form, 'activity_form': activity_form})


def my_account(request):
    return render(request, 'renova/my_account.html')


def groups(request):
    popular_groups_list = Group.objects.order_by('members')[:5]
    newest_groups_list = Group.objects.order_by('date')[:5]

    context_dict = {}
    context_dict['make_group_summary'] = "placeholder (make-group summary)"
    return render(request, 'renova/groups.html', context=context_dict)


def group(request, group_name_slug):
    return render(request, 'renova/group.html', {'group_name_slug': group_name_slug})


def make_group(request):
    form = GroupForm()
    return render(request, 'renova/make_group.html', {'form': form})
 