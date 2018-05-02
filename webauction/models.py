from django.db import models
from django.utils import timezone


class Bid(models.Model):
    name = models.CharField(max_length=200, default='noName')
    bid = models.IntegerField(default=1)
    nrofitems = models.IntegerField(default=1)

    def __str__(self):
            return self.name

    def bid_is_higher_than_1(self):
            return self.bid > 1

class Item(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
            return self.name

# from webauction.models import Bid, Item
# from django.utils import timezone