from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class HotelUser(User):
    profile_picture = models.ImageField(upload_to='profile', null=True)
    phone_number = models.CharField(unique=True, max_length=100)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'hotel_user'


class HotelVendor(User):
    profile_picture = models.ImageField(upload_to='profile', null=True)
    business_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(unique=True, max_length=100)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'hotel_vendor'


class Amenities(models.Model):
    amenity_name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='hotels')

    def __str__(self):
        return self.amenity_name


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=100)
    hotel_description = models.TextField()
    hotel_slug = models.SlugField(max_length=1000, null=True, blank=True)
    hotel_owner = models.ForeignKey(HotelVendor, on_delete=models.CASCADE, related_name='hotel_owner')
    hotel_address = models.CharField(max_length=100)
    amenities = models.ManyToManyField(Amenities)
    hotel_price = models.FloatField()
    hotel_offer_price = models.FloatField()
    hotel_location = models.TextField()
    is_active = models.BooleanField(default=True)


class HotelImages(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images')
    image = models.ImageField(upload_to='hotels')


class HotelManager(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_manager')
    manager_name = models.CharField(max_length=100)
    manager_contact = models.CharField(max_length=100)


class HotelBooking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='Bookings')
    booking_user = models.ForeignKey(HotelUser, on_delete=models.CASCADE)
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    booking_price = models.FloatField()


