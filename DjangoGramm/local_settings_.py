# Local Db.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangogramm',
        'PORT': '5432',
        'USER': 'tester',
        'PASSWORD': 'tester',
        'HOST': 'localhost'
    }
}

STATIC_URL = '/static/'
