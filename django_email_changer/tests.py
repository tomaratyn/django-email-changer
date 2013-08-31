# Copyright 2013 Tom Aratyn <tom@aratyn.name>
#
# This program is licensed under the MIT license (see LICENSE or http://opensource.org/licenses/MIT)
#

from datetime import timedelta
from django.utils.timezone import now
from mock import patch, Mock

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_email_changer import settings
from django_email_changer.forms import UserEmailModificationForm
from django_email_changer.models import UserEmailModification
from django_email_changer import urls as email_changer_urls


def refresh(model):
    return model.__class__.objects.get(id=model.id)


class TestUserEmailModificationModel(TestCase):

    def setUp(self):
        self.user_email = "user@example.org"
        self.user = User.objects.create_user(self.user_email, self.user_email, "secert")

    def test_default_security_code(self):
        """
        Test that the security code is 32 characters long (a valid uuid)
        """
        uem = UserEmailModification.objects.create(user=self.user, new_email="something else")
        self.assertEqual(32, len(uem.security_code))

    def test_activate_new_email(self):
        new_email = "user@changed.example.org"
        uem = UserEmailModification.objects.create(user=self.user, new_email=new_email)
        uem.activate()
        self.user = refresh(self.user)
        self.assertEqual(new_email, self.user.email)
        self.assertIsNotNone(uem.date_change_accepted)

    def test_do_not_activate_expired(self):
        new_email = "user@changed.example.org"
        expired_email_modification_request = UserEmailModification.objects.create(new_email=new_email,
                                                                                  user=self.user)
        expired_email_modification_request.date_change_proposed = now() - \
                                                                  timedelta(**settings.CHANGE_EMAIL_CODE_EXPIRY_TIME) - \
                                                                  timedelta(days=1)
        expired_email_modification_request.save()
        rv = expired_email_modification_request.activate()
        self.assertFalse(rv)
        self.assertEqual(self.user_email, self.user.email)



class TestUserEmailModificationForm(TestCase):

    def test_new_email_and_confirmed_email_are_the_same(self):
        form_data = {"new_email": "something@example.com",
                     "confirmed_email": "somethingelse@example.com",
                     "password": "secret", }
        form = UserEmailModificationForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {"new_email": "something@example.com",
                     "confirmed_email": "something@example.com",
                     "password": "secret", }
        form = UserEmailModificationForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestUserEmailUserModificationView(TestCase):

    urls = email_changer_urls

    def setUp(self):
        self.password = "secret"
        self.user = User.objects.create_user(username="user",
                                             password=self.password)
        self.client.login(username="user", password=self.password)

    @patch("django_email_changer.views.Thread")
    def test_post(self, threading_Thread):
        thread = Mock()
        threading_Thread.return_value = thread
        dem_count = UserEmailModification.objects.count()
        form_data = {"new_email": "something@example.com",
                     "confirmed_email": "something@example.com",
                     "password": self.password, }
        response = self.client.post(reverse("django_email_changer_change_view"),
                                    form_data)
        self.assertEqual(302, response.status_code)
        self.assertEqual(dem_count+1, UserEmailModification.objects.count())
        self.assertEqual(1, threading_Thread.call_count)
        self.assertTrue("call.start()" in [str(call) for call in thread.method_calls])

        dem_count = UserEmailModification.objects.count()
        form_data = {"new_email": "something@example.com",
                     "confirmed_email": "something@example.com",
                     "password": self.password + "1", }
        response = self.client.post(reverse("django_email_changer_change_view"),
                                    form_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(dem_count, UserEmailModification.objects.count())


class TestNewEmailActivationView(TestCase):

    urls = email_changer_urls

    def setUp(self):
        self.original_email = "user@original.example.org"
        self.password = "secret"
        self.user = User.objects.create_user(username="user",
                                             email=self.original_email,
                                             password=self.password)
        self.client.login(username=self.user.username, password=self.password)
        self.new_email = "user@changed.example.org"
        self.uem = UserEmailModification.objects.create(new_email=self.new_email, user=self.user)

    def test_activate_password(self):
        response = self.client.get(reverse("django_change_email_activate_new_email",
                                           kwargs={"code": self.uem.security_code}))
        self.assertEqual(200, response.status_code)
        self.user = refresh(self.user)
        self.assertEqual(self.new_email, self.user.email)

    def test_invalid_code_fails(self):
        if self.uem.security_code[-1] == 'a':
            security_code = self.uem.security_code[:-1] + 'b'
        else:
            security_code = self.uem.security_code[:-1] + 'a'
        response = self.client.get(reverse("django_change_email_activate_new_email",
                                           kwargs={"code": security_code}))
        self.assertEqual(404, response.status_code)
        self.user = refresh(self.user)
        self.assertEqual(self.original_email, self.user.email)

    def test_expired_code_fails(self):
        self.uem.date_change_proposed = now() - timedelta(**settings.CHANGE_EMAIL_CODE_EXPIRY_TIME) - timedelta(days=1)
        self.uem.save()
        security_code = self.uem.security_code
        response = self.client.get(reverse("django_change_email_activate_new_email",
                                           kwargs={"code": security_code}))
        self.user = refresh(self.user)
        self.assertEqual(self.original_email, self.user.email)
        self.assertEqual(404, response.status_code)

    def test_used_code_fails(self):
        self.assertTrue(self.uem.activate())
        self.user.email = self.original_email
        self.user.save()
        security_code = self.uem.security_code
        response = self.client.get(reverse("django_change_email_activate_new_email",
                                           kwargs={"code": security_code}))
        self.user = refresh(self.user)
        self.assertEqual(404, response.status_code)
        self.assertEqual(self.original_email, self.user.email)
