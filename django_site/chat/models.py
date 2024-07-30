import uuid
from django.contrib.auth.models import User
from django.db import models

# Room Model, aur Message Model define kar rahe hain

class Room(models.Model):
    # Room ka unique identifier UUID field se define kar rahe hain
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_user = models.ForeignKey(User, related_name="room_first", on_delete=models.CASCADE,null=True)
    second_user = models.ForeignKey(User, related_name="room_second", on_delete=models.CASCADE,null=True)


class Message(models.Model):
    # Message model me user ko associate kar rahe hain
    user = models.ForeignKey(User, related_name="messages", verbose_name="User", on_delete=models.CASCADE)
    # Message ko room ke saath link kar rahe hain
    room = models.ForeignKey(Room, related_name="messages", verbose_name="Room", on_delete=models.CASCADE)
    # Message content ko text field me store kar rahe hain
    content = models.TextField(verbose_name="Message Content")
    # Message create hote hi uska timestamp auto add hota hai
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")  # Accurate timestamp ke liye DateTimeField use kiya
