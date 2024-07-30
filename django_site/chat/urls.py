# chat/urls.py
from django.urls import path

from .views import *


urlpatterns = [
   path("", index, name="index"),

   path("<str:room_name>/", room, name="room"),
   path('start_chat/<str:username>',start_chat,name="start_chat"),
      
]