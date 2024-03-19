from django.test import TestCase
from django.urls import reverse

from renova.models import *

class BasicViewTests(TestCase):
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

    def test_groups_view(self):
        response = self.client.get(reverse('renova:groups'))
        self.assertEqual(response.status_code, 200)
    
    def test_make_group_view(self):
        response = self.client.get(reverse('renova:make_group'))
        self.assertEqual(response.status_code, 302)