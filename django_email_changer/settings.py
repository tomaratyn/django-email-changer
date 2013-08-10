from django.conf import settings

EMAIL_CHANGE_NOTIFICATION_SUBJECT = getattr(settings,
                                            "EMAIL_CHANGE_NOTIFICATION_SUBJECT",
                                            "Email Change Activation")

EMAIL_CHANGE_NOTIFICATION_EMAIL_TEMPLATE = getattr(settings,
                                                   "EMAIL_CHANGE_NOTIFICATION_EMAIL_TEMPLATE",
                                                   "django_email_changer/email_change_notification.txt")

EMAIL_CHANGE_NOTIFICATION_FROM = getattr(settings, "EMAIL_CHANGE_NOTIFICATION_FROM", "no-reply@example.com")

EMAIL_CHANGE_ACTIVATION_SUCCESS_URL = getattr(settings, "EMAIL_CHANGE_ACTIVATION_SUCCESS_URL", "/user-email-changed")

EMAIL_CHANGE_SUCCESS_URL = getattr(settings, "EMAIL_CHANGE_SUCCESS_URL", "/new-email-activation-sent")

CHANGE_EMAIL_CODE_EXPIRY_TIME = getattr(settings, "CHANGE_EMAIL_CODE_EXPIRY_TIME", {"days": 3})