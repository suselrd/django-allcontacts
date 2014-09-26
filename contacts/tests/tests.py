# coding=utf-8
from django.test import TestCase
from django.conf import settings
from ..models import Contact, ContactType, ContactTypeIcon


class TestContacts(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        pass

    def test_basics(self):
        # TODO implement!
        pass

    def test_site_awareness(self):
        # TODO implement!
        pass
