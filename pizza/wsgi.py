"""
WSGI config for pizza project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizza.settings")

application = get_wsgi_application()
SECRET_KEY = os.environ["i0&iq&e9u9h6(4_7%pt2s9)f=c$kso=k$c$w@fi9215s=1q0^d"]
