from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('main.urls'), name = 'main'),
    path('register', include('register.urls')),
    path('ticket', include('ticket.urls')),
]
