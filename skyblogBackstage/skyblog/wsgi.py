"""
WSGI config for SkyBlog backend project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skyblog.settings')

application = get_wsgi_application()