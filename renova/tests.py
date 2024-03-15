from django.test import TestCase

from django.urls import reverse

class ViewTests(TestCase):
    def test_index_view_basic(self):
        response = self.client.get(reverse('renova:index'))
        self.assertEqual(response.status_code, 200)