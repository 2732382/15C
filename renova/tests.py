from django.test import TestCase
from django.urls import reverse

from renova.models import *

class LoadViewTestsNoLogin(TestCase):

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

class LoadViewTestsLogin(TestCase):

    def setUp(self):
        self.example_user = User.objects.create_user(username='exampleuser',
                                                     password="12345")
        self.example_user.save()
        self.example_profile = UserProfile.objects.get_or_create(user=self.example_user)[0]
        self.example_profile.save()

        self.client.force_login(self.example_user)
    
    def test_my_logs_view_no_login(self):
        response = self.client.get(reverse('renova:my_logs'))
        self.assertEqual(response.status_code, 200)
    
    def test_record_log_view_no_login(self):
        response = self.client.get(reverse('renova:record_log'))
        self.assertEqual(response.status_code, 200)

    def test_my_account_view_no_login(self):
        response = self.client.get(reverse('renova:my_account'))
        self.assertEqual(response.status_code, 200)

    def test_make_group_view_no_login(self):
        response = self.client.get(reverse('renova:make_group'))
        self.assertEqual(response.status_code, 200)

class GroupsViewTests(TestCase):

    def test_groups_view_empty(self):
        response = self.client.get(reverse('renova:groups'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no groups present.")
        self.assertContains(response, "There are no new groups present.")
    
    def test_groups_view_with_groups(self):
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

class MyLogsViewTests(TestCase):

    def setUp(self):
        self.example_user = User.objects.create_user(username='exampleuser',
                                                     password="12345")
        self.example_user.save()
        self.example_profile = UserProfile.objects.get_or_create(user=self.example_user)[0]
        self.example_profile.save()

        self.client.force_login(self.example_user)

    def test_my_logs_view_empty(self):
        response = self.client.get(reverse('renova:my_logs'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have no logs at the moment.")

    def test_my_logs_view_with_logs(self):
        running_activity = Activity.objects.get_or_create(name="RunActExample", duration=10)[0]
        running_activity.save()
        running_log = Log.objects.get_or_create(user = self.example_user)[0]
        running_log.activities.add(running_activity)
        running_log.save()

        response = self.client.get(reverse('renova:my_logs'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Activity Name: RunActExample")
        self.assertContains(response, "Duration mins: 10")

class IndividualGroupViewTests(TestCase):

    def setUp(self):
        self.example_user = User.objects.create_user(username='exampleuser',
                                                     password="12345")
        self.example_user.save()
        self.example_profile = UserProfile.objects.get_or_create(user=self.example_user)[0]
        self.example_profile.save()

        self.client.force_login(self.example_user)

        self.test_group = Group.objects.get_or_create(name = "TestGroup",
                                                     admin = self.example_user,
                                                     description = "Testing code",
                                                     announcements = "This is a test")[0]
        self.test_group.save()

    def test_individual_group_view_empty(self):
        group_name_slug = self.test_group.slug
        response = self.client.get(reverse('renova:group', args = [group_name_slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are the admin of this group")
        self.assertContains(response, "Testing code")
        self.assertContains(response, "This is a test")

    def test_individual_group_view_with_comment(self):
        test_comment = Comment.objects.get_or_create(group = self.test_group,
                                                     user = self.example_user,
                                                     text="test comment")[0]
        test_comment.save()

        group_name_slug = self.test_group.slug
        response = self.client.get(reverse('renova:group', args = [group_name_slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test comment")
        self.assertContains(response, "<strong>exampleuser</strong> (Admin)")
        
    def test_individual_group_view_member(self):
        self.client.logout()
        example_member = User.objects.create_user(username='examplemember',
                                                  password="12345")
        example_member.save()
        example_profile = UserProfile.objects.get_or_create(user=example_member)[0]
        example_profile.save()

        self.client.force_login(example_member)

        group_name_slug = self.test_group.slug
        response = self.client.get(reverse('renova:group', args = [group_name_slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Join Group")
        self.assertNotContains(response, "Post comment")

        # Now make this user a member and check that
        self.test_group.members.add(example_member)
        response = self.client.get(reverse('renova:group', args = [group_name_slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Leave Group")
        self.assertContains(response, "Post comment")