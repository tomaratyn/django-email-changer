
DEBUG = True
TEMPLATE_DEBUG = True

SITE_ID = 1

DATABASES = {
    'default': {
        'NAME': 'db.sqlite',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django_email_changer',
)

ROOT_URLCONF = 'django_email_changer.urls'

SECRET_KEY = 'django_email_changer'

EMAIL_CHANGE_NOTIFICATION_SUBJECT = "Email Change Activation Request"

EMAIL_CHANGE_NOTIFICATION_EMAIL_TEMPLATE = "django_email_changer/email_change_notification.html"

EMAIL_CHANGE_NOTIFICATION_FROM = "from-no-reply@example.com"

EMAIL_CHANGE_ACTIVATION_SUCCESS_URL = "/activated-success"

EMAIL_CHANGE_SUCCESS_URL = "/test-success" #not real