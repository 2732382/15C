import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'group_project.settings')

import django
django.setup()
from renova.models import *

def populate():

    first_admin = User.objects.create_user(username="temp_admin",
                                           password="12345")
    first_admin.save()
    first_admin_profile = UserProfile.objects.get_or_create(user=first_admin)[0]
    first_admin_profile.save()

    RB_user = User.objects.create_user(username='RedBlue',
                                       password='Conglomerate123')
    RB_user.save()
    RB_profile = UserProfile.objects.get_or_create(user=RB_user)[0]
    RB_profile.save()

    OG_user = User.objects.create_user(username='OrangeGrey',
                                       password='Building123')
    OG_user.save()
    OG_profile = UserProfile.objects.get_or_create(user=OG_user)[0]
    OG_profile.save()

    YG_user = User.objects.create_user(username='YellowGreen',
                                       password='Representative123')
    YG_user.save()
    YG_profile = UserProfile.objects.get_or_create(user=YG_user)[0]
    YG_profile.save()

    groups = {
        'Running group': {"admin": first_admin,
                          "members": [RB_user,OG_user],
                          "description": "We are a group that likes to go running regularly, please join!",
                          "announcements": "Run tomorrow is cancelled due to rain"},
        'Climbing group': {"admin": first_admin,
                           "members": [OG_user,YG_user],
                           "description": "We are a local glasgow group that likes rocks and climbing them.",
                           "announcements": "TCA new set session tomorrow."}
    }

    comments = {
        'Running group': [
            {"user":first_admin, "text": "Look I have a special admin role."},
            {"user":RB_user, "text":"I love running"},
            {"user":OG_user, "text":"Example comment"}
        ],
        'Climbing group': [
            {"user":first_admin, "text": "I'm the climbing admin."},
            {"user":YG_user, "text":"I love climbing"},
            {"user":OG_user, "text":"Another example comment"}
        ],
    }

    logs = [
        {"user":first_admin,
         "water":2000,
         "calories":1200,
         "sleep":6,
         "activities":{"running":10,
                       "climbing":20}}
    ]

    for group,group_data in groups.items():
        g = Group.objects.get_or_create(name=group,
                                        admin=group_data["admin"],
                                        description=group_data["description"],
                                        announcements=group_data["announcements"])[0]
        g.save()
        
        for member in group_data["members"]:
            g.members.add(member)
        

        for comment in comments[group]:
            c = Comment.objects.get_or_create(group=g,
                                             user=comment["user"],
                                             text=comment["text"])[0]
            c.save()
        
    for log in logs:
        l = Log.objects.get_or_create(user = log["user"],
                                        water = log["water"],
                                        calories = log["calories"],
                                        sleep = log["sleep"])[0]
        l.save()

        for name,duration in log["activities"].items():
            a = Activity.objects.get_or_create(name=name,
                                               duration=duration,
                                               log = l)[0]
            a.save()

if __name__ == '__main__':
    print('Starting Renova population script...')
    populate()
    print('Population complete!')