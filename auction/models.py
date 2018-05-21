from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    audio_url = models.CharField(max_length=300, default='http://django-static.vps.abaart.nl/group10/django/undefined_audio.wav')
    creation_date = models.DateTimeField('date published')

    def __str__(self):
        return self.product_name

class Auction(models.Model):
    auction_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=200, default="")
    quantity = models.PositiveIntegerField()
    starting_price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    auction_start = models.DateTimeField()
    auction_end = models.DateTimeField()
    creation_date = models.DateTimeField('date published')

    def __str__(self):
        return "Auction of {}".format(product.product_name)

class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField()
    owner = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date published')
