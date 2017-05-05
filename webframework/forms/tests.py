from django.test import TestCase
from django.test import Client

# Create your tests here.
class FormsViewTestCase(TestCase):
    def test_index(self):
        client = Client()
        resp = self.client.get('/forms/')
        self.assertFalse(resp.status_code == 200)

class FormsMealViewTestCase(TestCase):
    def test_index(self):
        client = Client()
        resp = self.client.get('/forms/addmeal/')
        self.assertFalse(resp.status_code == 200)

class FormsExpenseViewTestCase(TestCase):
    def test_index(self):
        client = Client()
        resp = self.client.get('/forms/addexpense/')
        self.assertFalse(resp.status_code == 200)

class FormsDailyViewTestCase(TestCase):
    def test_index(self):
        client = Client()
        resp = self.client.get('/forms/dailyexpenses')
        self.assertFalse(resp.status_code == 200)
