from django.contrib import admin
from .models import UserTable, Property, Units, TenentRentAggriment, Documents

# Register your models here.
admin.site.register([UserTable, Property, Units, TenentRentAggriment, Documents])
