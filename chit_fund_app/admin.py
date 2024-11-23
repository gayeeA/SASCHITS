# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Subscriber, ChitGroup, Payment

admin.site.register(Subscriber)
admin.site.register(ChitGroup)
admin.site.register(Payment)

