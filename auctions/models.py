from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=24)
    description = models.CharField(max_length=64)
    startingprice = models.IntegerField()
    imagename = models.CharField(max_length=255)
    categoryname = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return f"{self.title} ({self.startingprice})"
    
    pass

class Bids:
    def __init__(self, amount):
        self.amount = amount
    pass

class Comment:
    def __init__(self, content):
        self.content = content
    pass
