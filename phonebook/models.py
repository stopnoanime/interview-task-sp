from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=128, unique=True)
    phone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Name: {self.name} - Phone: {self.phone}"