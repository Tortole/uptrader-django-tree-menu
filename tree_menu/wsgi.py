"""
WSGI config for tree_menu project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tree_menu.settings")

application = get_wsgi_application()
