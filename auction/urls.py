from django.urls import path

from . import views

app_name = 'auction'
urlpatterns = [
	path('', views.index, name='index'),
    path('product', views.product, name='product'),
    path('bid', views.bid, name='bid'),
    path('vxml', views.vxml, name='vxml'),
    path('new_product', views.add_new_product, name='add_new_product'),
    path('new_auction', views.create_new_auction, name='create_new_auction'),
    path('place_bid', views.place_bid, name='place_bid'),
    path('delete_auction/<int:auction_id>', views.delete_auction, name='delete_auction'),
]