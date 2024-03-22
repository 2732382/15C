import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'group_project.settings')

import django
django.setup()
from renova.models import *

def populate():

    first_admin = User.objects.get_or_create(username="temp_admin", password="12345")[0]

    RB_user = User.objects.get_or_create(username='RedBlue',password='Conglomerate123')
    OG_user = User.objects.get_or_create(username='OrangeGrey',password='Building123')
    YG_user = User.objects.get_or_create(username='YellowGreen',password='Representative123')

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

    for group,group_data in groups.items():
        g = Group.objects.get_or_create(name=group,
                                        admin=group_data["admin"],
                                        description=group_data["description"],
                                        announcements=group_data["announcements"])[0]
        for member in group_data["members"]:
            g.members.add(member)
        g.save()

    

# Start execution here!
if __name__ == '__main__':
    print('Starting Renova population script...')
    populate()
    print('Population complete!')