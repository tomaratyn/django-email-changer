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

SECRET_KEY = 'django_email_changer'