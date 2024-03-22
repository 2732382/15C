import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'group_project.settings')

import django
django.setup()
from renova.models import *

def populate():

    first_admin = User.objects.get_or_create(username="temp_admin", password="12345")[0]
    first_admin.save()

    RB_user = User.objects.get_or_create(username='RedBlue',password='Conglomerate123')[0]
    RB_user.save()
    OG_user = User.objects.get_or_create(username='OrangeGrey',password='Building123')[0]
    OG_user.save()
    YG_user = User.objects.get_or_create(username='YellowGreen',password='Representative123')[0]
    YG_user.save()

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

    for group,group_data in groups.items():
        g = Group.objects.get_or_create(name=group,
                                        admin=group_data["admin"],
                                        description=group_data["description"],
                                        announcements=group_data["announcements"])[0]
        g.save()
        
        for member in group_data["members"]:
            g.members.add(member)
        

        for comm in comments[group]:
            c =Comment.objects.get_or_create(group=g,
                                             user=comm["user"],
                                             text=comm["text"])[0]
            c.save()
        

    

# Start execution here!
if __name__ == '__main__':
    print('Starting Renova population script...')
    populate()
    print('Population complete!')