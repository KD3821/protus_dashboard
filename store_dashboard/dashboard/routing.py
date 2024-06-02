from django.urls import path

from .consumers import StoreConsumer


websocket_urlpatterns = [
    path('ws/stores/<str:store_id>', StoreConsumer.as_asgi())
]
