import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_management.settings')

import django
django.setup()

from django.core.asgi import get_asgi_application

from finance.middleware.jwt import JwtAuthMiddlewareStack

application = get_asgi_application()