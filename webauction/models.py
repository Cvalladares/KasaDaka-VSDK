from django.db import models


class Bid(models.Model):
    name = models.CharField(max_length=200)
    bid = models.IntegerField(default=1)
    nrofitems = models.IntegerField(default=1)


class Item(models.Model):
    name = models.CharField(max_length=200)