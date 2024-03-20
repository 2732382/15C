from django.test import TestCase
from django.urls import reverse

from renova.models import *

class ViewTests(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse('renova:index'))
        self.assertEqual(response.status_code, 200)

    def test_faq_view(self):
        response = self.client.get(reverse('renova:faq'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_view(self):
        response = self.client.get(reverse('renova:about_us'))
        self.assertEqual(response.status_code, 200)
    
    def test_my_logs_view_no_login(self):
        response = self.client.get(reverse('renova:my_logs'))
        self.assertEqual(response.status_code, 302)
    
    def test_record_log_view_no_login(self):
        response = self.client.get(reverse('renova:record_log'))
        self.assertEqual(response.status_code, 302)

    def test_my_account_view_no_login(self):
        response = self.client.get(reverse('renova:my_account'))
        self.assertEqual(response.status_code, 302)

    def test_make_group_view_no_login(self):
        response = self.client.get(reverse('renova:make_group'))
        self.assertEqual(response.status_code, 302)

class GroupsViewTests(TestCase):

    def test_groups_view(self):
        response = self.client.get(reverse('renova:groups'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no groups present.")
        self.assertContains(response, "There are no new groups present.")
    
    def test_groups_view_with_content(self):
        example_admin = User.objects.get_or_create(username="temp_admin")[0]
        running_group = Group.objects.get_or_create(name="Running Example")[0]
        running_group.admin = example_admin
        running_group.save()
        
        swimming_group = Group.objects.get_or_create(name="Swimming Example")[0]
        swimming_group.admin = example_admin
        swimming_group.save()

        
        response = self.client.get(reverse('renova:groups'))

        self.assertContains(response, "Running Example")
        self.assertContains(response, "Swimming Example")

        num_popular_groups = len(response.context['popular_groups'])
        num_recent_groups = len(response.context['recent_groups'])
        self.assertEquals(num_popular_groups, 2)
        self.assertEquals(num_recent_groups, 2)