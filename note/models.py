from django.db import models
from user.models import CustomUser

# model for Note Object
class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255, blank=False, null=False)
    text = models.TextField()
