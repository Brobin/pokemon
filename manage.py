#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokemon.settings")

    from django.core.management import execute_from_command_line

    if 'test' in sys.argv:
        import logging
        from django.conf import settings
        logging.disable(logging.CRITICAL)
        settings.DEBUG = False
        settings.TEMPLATE_DEBUG = False
        settings.INSTALLED_APPS.remove('debug_toolbar')
        settings.PASSWORD_HASHERS = [
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ]
        settings.DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test_database',
            }
        }
        settings.HAYSTACK_CONNECTIONS = {
            'default': {
                'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
            },
        }
        settings.MIDDLEWARE = [
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ]

    execute_from_command_line(sys.argv)
