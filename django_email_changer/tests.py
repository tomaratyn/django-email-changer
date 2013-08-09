from mock import patch, Mock

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_email_changer.forms import UserEmailModificationForm
from django_email_changer.models import UserEmailModification
from django_email_changer import urls as email_changer_urls


class TestUserEmailModificationModel(TestCase):

    def test_default_security_code(self):
        """
        Test that the security code is 32 characters long (a valid uuid)
        """
        user_email = "user@example.org"
        user = User.objects.create_user(user_email, user_email, "secert")
        uem = UserEmailModification.objects.create(user=user, new_email="something else")
        self.assertEqual(32, len(uem.security_code))

    def test_activate_new_email(self):
        user_email = "user@example.org"
        new_email = "user@changed.example.org"
        user = User.objects.create_user(user_email, user_email, "secret")
        uem = UserEmailModification.objects.create(user=user, new_email=new_email)
        uem.activate()
        user = User.objects.get(id=user.id)
        self.assertEqual(new_email, user.email)
        self.assertIsNotNone(uem.date_change_accepted)


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

    def test_activate_password(self):
        new_email = "user@changed.example.org"
        email_modification = UserEmailModification.objects.create(new_email=new_email,
                                                                  user=self.user)
        response = self.client.get(reverse("django_change_email_activate_new_email",
                                           kwargs={"code": email_modification.security_code}))

        self.assertEqual(302, response.status_code)
        new_email = "user@changed.example.org"
        email_modification = UserEmailModification.objects.create(new_email=new_email,
                                                                  user=self.user)

        if email_modification.security_code[-1] == 'a':
            security_code = email_modification.security_code[:-1] + 'b'
        else:
            security_code = email_modification.security_code[:-1] + 'a'
        response = self.client.get(reverse("django_change_email_activate_new_email",
                                           kwargs={"code": security_code}))

        self.assertEqual(404, response.status_code)
