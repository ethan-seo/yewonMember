from django.contrib import admin

# Register your models here.
from .models import Customer, Newsletter

admin.site.register(Customer)
admin.site.register(Newsletter)