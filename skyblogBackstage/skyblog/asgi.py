"""
ASGI config for SkyBlog backend project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skyblog.settings')

application = get_asgi_application()