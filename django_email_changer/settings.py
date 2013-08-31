# Copyright 2013 Tom Aratyn <tom@aratyn.name>
#
# This program is licensed under the MIT license (see LICENSE or http://opensource.org/licenses/MIT)
#

from django.conf import settings

EMAIL_CHANGE_NOTIFICATION_SUBJECT = getattr(settings,
                                            "EMAIL_CHANGE_NOTIFICATION_SUBJECT",
                                            "Email Change Activation")

EMAIL_CHANGE_NOTIFICATION_EMAIL_TEMPLATE = getattr(settings,
                                                   "EMAIL_CHANGE_NOTIFICATION_EMAIL_TEMPLATE",
                                                   "django_email_changer/email_change_notification.txt")

EMAIL_CHANGE_NOTIFICATION_FROM = getattr(settings, "EMAIL_CHANGE_NOTIFICATION_FROM", "no-reply@example.com")

EMAIL_CHANGE_ACTIVATION_SUCCESS_URL = getattr(settings,
                                              "EMAIL_CHANGE_ACTIVATION_SUCCESS_URL", "django_change_email_sent_activation_email")

EMAIL_CHANGE_SUCCESS_URL = getattr(settings, "EMAIL_CHANGE_SUCCESS_URL", "django_change_email_sent_activation_email")

CHANGE_EMAIL_CODE_EXPIRY_TIME = getattr(settings, "CHANGE_EMAIL_CODE_EXPIRY_TIME", {"days": 3})

EMAIL_CHANGE_NOTIFICATION_SENT_TEMPLATE = getattr(settings,
                                                  "EMAIL_CHANGE_NOTIFICATION_SENT_TEMPLATE",
                                                  "django_email_changer/email_notification_sent.html")

EMAIL_CHANGE_SUCCESSS_TEMPLATE = getattr(settings,
                                         "EMAIL_CHANGE_SUCCESSS_TEMPLATE",
                                         "django_email_changer/email_change_success.html")