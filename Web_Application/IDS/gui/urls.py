from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('alarm',views.alarmon,name='alarm'),
    path('led',views.toggleLED,name='led'),
    path('ids',views.toggleIDS,name='ids'),
    path('rpi',views.rpi,name='rpi'),
    path('history',views.history,name='history'),
    path('client',views.client,name='client'),
    path('idsstate',views.ids,name='idsstate'),
    path('stream',views.stream,name='stream'),
    ]