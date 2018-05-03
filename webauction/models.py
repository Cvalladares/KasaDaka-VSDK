from django.db import models
from django.utils import timezone


#class Schedule(models.Model):
#    datetime = models.DateTimeField('date of auction')
#    item = models.CharField(max_length=200)
#    nameofseller = models.CharField(max_length=200,default='john doe')
#    startingprice = models.IntegerField(default=1)


#    def __str__(self):
#            return self.nameofseller



class Bid(models.Model):
#    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    potentialbuyer = models.CharField(max_length=200, default='noName')
    offerinzedi = models.IntegerField(default=1)
    nrofitems = models.IntegerField(default=1)

    def __str__(self):
            return self.name

    def bid_is_higher_than_1(self):
            return self.bid > 1

class Item(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
            return self.name




# from webauction.models import Shedule, Bid, Item
# from django.utils import timezone