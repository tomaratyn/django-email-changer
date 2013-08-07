from django.contrib.auth.models import User
from django.test import TestCase
from django_email_changer.models import UserEmailModification


class TestUserEmailModification(TestCase):

    def test_default_security_code(self):
        """
        Test that the security code is 32 characters long (a valid uuid)
        """
        user_email = "user@example.org"
        user = User.objects.create_user(user_email, user_email, "secert")
        model = UserEmailModification.objects.create(user=user, new_email="something else")
        self.assertEqual(32, len(model.security_code))
