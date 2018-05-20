import time
import datetime

from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Product, Auction, Bid


def index(request):
    template_name = 'auction/index.html'
    products = Product.objects.all()

    start_range = datetime.datetime.now()
    end_range = start_range + datetime.timedelta(days=6)
    auctions = Auction.objects.filter(auction_end__range=[start_range, end_range])

    current_auction = None
    for auction in auctions:
        if auction.auction_start.replace() <= datetime.datetime.now() <= auction.auction_end:
            current_auction = auction

    return render(request, template_name,
                  {'products': products, 'auctions': auctions, 'current_auction': current_auction})


def product(request):
    model = Product
    template_name = 'product/index.html'
    query_results = Product.objects.all()
    return render(request, template_name, {'query_results': query_results})


def bid(request):
    template_name = 'bid/index.html'

    start_range = datetime.datetime.now()
    end_range = start_range + datetime.timedelta(days=6)
    auctions = Auction.objects.filter(auction_end__range=[start_range, end_range])

    current_auction = None
    for auction in auctions:
        if auction.auction_start.replace() <= datetime.datetime.now() <= auction.auction_end:
            current_auction = auction

    # filter bids to only show those corresponding to this auction
    bids = Bid.objects.filter(auction__auction_id=current_auction.auction_id)

    # If there is no auction, redirect to auction page
    if current_auction is None:
        return HttpResponseRedirect("/auction/")

    return render(request, template_name, {'auction': current_auction, 'bids': bids})


def vxml(request):
    template = loader.get_template('vxml/default.xml')

    # Fetch acutions
    start_range = datetime.datetime.now()
    end_range = start_range + datetime.timedelta(days=6)
    auctions = Auction.objects.filter(auction_end__range=[start_range, end_range])

    current_auction = None
    for auction in auctions:
        if auction.auction_start.replace() <= datetime.datetime.now() <= auction.auction_end:
            current_auction = auction

    # Generate the URL for the Wav file.  All wave files must be named as <number>_en.wav in
    #   order for this to work
    quantity_for_sale = '{}{}{}'.format('http://django-static.vps.abaart.nl/group10/django/',
                                        current_auction.quantity,
                                        '_en.wav')
    item = current_auction.product.audio_url

    return render(request, template, {'quantity_for_sale': quantity_for_sale}, content_type='text/xml')


def add_new_product(request):
    new_product = Product()
    new_product.product_name = request.POST['product_name']
    new_product.audio_url = request.POST['audio_url']
    new_product.creation_date = timezone.now()
    new_product.save()

    return HttpResponseRedirect("/auction/product")


def create_new_auction(request):
    create_new_auction_now(request)

    # start_time = datetime.datetime.today().replace(hour=11, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)

    # if len(Auction.objects.all()):
    # 	start = Auction.objects.latest('auction_start').auction_start
    # 	start_time = start + datetime.timedelta(seconds=15*60)

    # 	if datetime.datetime.now() >= Auction.objects.latest('auction_start').auction_start.replace(tzinfo=None):
    # 		start_time = datetime.datetime.today().replace(hour=11, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)

    # end_time = start_time + datetime.timedelta(seconds=15*60-1)

    # new_auction = Auction()
    # new_auction.product = Product.objects.get(pk=request.POST['product'])
    # new_auction.quantity = request.POST['quantity']
    # new_auction.starting_price = request.POST['starting_price']
    # new_auction.auction_start = start_time
    # new_auction.auction_end = end_time
    # new_auction.creation_date = timezone.now()
    # new_auction.save()

    return HttpResponseRedirect("/auction/")


def create_new_auction_now(request):
    start_time = datetime.datetime.now().replace(second=0, microsecond=0)
    end_time = start_time + datetime.timedelta(seconds=15 * 60 - 1)

    new_auction = Auction()
    new_auction.product = Product.objects.get(pk=request.POST['product'])
    new_auction.quantity = request.POST['quantity']
    new_auction.starting_price = request.POST['starting_price']
    new_auction.auction_start = start_time
    new_auction.auction_end = end_time
    new_auction.creation_date = timezone.now()
    new_auction.save()

    return HttpResponseRedirect("/auction/")


def delete_auction(request, auction_id):
    Auction.objects.filter(auction_id=auction_id).delete()
    return HttpResponseRedirect("/auction/")


def place_bid(request):
    template_name = 'bid/index.html'
    auction = Auction.objects.get(pk=request.POST['auction_id'])

    # if invalid bid price
    if float(request.POST['bid']) < auction.starting_price or auction.quantity < float(request.POST['quantity']):

        error_message = ""
        if auction.quantity < float(request.POST['quantity']):
            error_message = "Your order is too large"
        if float(request.POST['bid']) < auction.starting_price:
            error_message = "The price you entered is to low"

        return render(request, template_name, {
            'auction': auction,
            'owner': request.POST['owner'],
            'bid': request.POST['bid'],
            'price_error': error_message,
            'quantity': request.POST['quantity']})

    new_bid = Bid()
    new_bid.auction = auction
    new_bid.owner = request.POST['owner']
    new_bid.bid = request.POST['bid']
    new_bid.quantity = request.POST['quantity']
    new_bid.creation_date = timezone.now()
    new_bid.save()

    return HttpResponseRedirect("/auction/bid")
