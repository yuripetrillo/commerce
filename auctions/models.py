from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=24)
    description = models.CharField(max_length=64)
    startingprice = models.IntegerField()
    imagename = models.CharField(max_length=255)
    categoryname = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    winner = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.startingprice})"
    pass

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='bidder')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='item')
    pass

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='commenter')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='itemCommented')
    timestamp = models.DateTimeField(blank=True, null=True)
    pass

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='watchlister')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='itemWatchlist')
    pass
