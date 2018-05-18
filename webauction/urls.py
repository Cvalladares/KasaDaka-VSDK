from django.urls import path

from . import views

app_name = 'webauction'
urlpatterns = [
    path('', views.index, name='index'),
    path('schedule/', views.schedule, name='schedule'),
    path('currentauction/', views.currentauction, name='currentauction'),
]