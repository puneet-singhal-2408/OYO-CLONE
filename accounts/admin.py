from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(HotelUser)
admin.site.register(HotelVendor)

admin.site.register(Amenities)
admin.site.register(Hotel)
admin.site.register(HotelBooking)
