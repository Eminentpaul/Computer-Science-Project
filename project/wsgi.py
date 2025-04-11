"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()








# import os

# from django.core.wsgi import get_wsgi_application
# from dj_static import Cling
# from wsgi_django_media import DjangoMedia

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# # application = Cling(get_wsgi_application())
# application = DjangoMedia(Cling(get_wsgi_application()))
