from django.urls import path
from . import views

app_name = 'ticket'

urlpatterns = [
    path('', views.buying, name = 'buying'),
    path('buying_done', views.buying_done, name = 'buying_done'),
]
