

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat.settings')
from channels.routing import ProtocolTypeRouter, URLRouter

application = get_asgi_application()
from channels.auth import AuthMiddlewareStack
import app.routing

application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket": AuthMiddlewareStack(
            URLRouter(app.routing.websocket_urlpatterns)
        ),
    }
)

