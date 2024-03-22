import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'group_project.settings')

import django
django.setup()
from renova.models import *

def populate():

    first_admin = User.objects.get_or_create(username="temp_admin", password="12345")[0]

    groups = {
        'Running': {"name": "Running group",
                    "admin": first_admin,
                    "description": "We are a group that likes to go running regularly, please join!",
                    "announcements": "Run tomorrow is cancelled due to rain"},
        'Climbing': {"name": "Climbing 123",
                    "admin": first_admin,
                    "description": "We are a local glasgow group that likes rocks and climbing them.",
                    "announcements": "TCA new set session tomorrow."}
    }

    for group,group_data in groups.items():
        g = add_group(group_data['name'],group_data['admin'],group_data['description'],group_data['announcements'])


def add_group(name, admin, description, announcements):
    g = Group.objects.get_or_create(name=name,admin=admin,description=description,announcements=announcements)[0]
    g.save()
    return g

# Start execution here!
if __name__ == '__main__':
    print('Starting Renova population script...')
    populate()
    print('Population complete!')