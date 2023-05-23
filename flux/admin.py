from django.contrib import admin

# Register your models here.

from .models import Ticket, Review

admin.site.register(Ticket)
admin.site.register(Review)
