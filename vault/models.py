import uuid
from django.db import models

from accounts.models import User

class PasswordEntry(models.Model):
    """
    Model to store password entries.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_entries')
    titel = models.CharField(max_length=255)
    encryted_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title