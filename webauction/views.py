from django.http import HttpResponse
from django.template import loader

from .models import Bid,Item

def index(request):
    item_list = Item.objects.all()
    template = loader.get_template('webauction/index.html')
    context = {
        'item_list': item_list,
    }
    return HttpResponse(template.render(context, request))


def schedule(request):
    template = loader.get_template('webauction/schedule.html')
    context = { }
    return HttpResponse(template.render(context, request))


def currentauction(request):
    template = loader.get_template('webauction/currentauction.html')
    context = { }
    return HttpResponse(template.render(context, request))