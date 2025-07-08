from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from accounts.models import Hotel, HotelBooking, HotelUser


# Create your views here.


def index(request):
    hotels = Hotel.objects.all()
    if request.GET.get('search'):
        hotels = hotels.filter(hotel_name__icontains=request.GET.get('search'))

    if request.GET.get('search'):
        sort_by = request.GET.get('sort_by')
        if sort_by == "sort_low":
            hotels = hotels.order_by('hotel_offer_price')
        elif sort_by == "sort_high":
            hotels = hotels.order_by('-hotel_offer_price')

    return render(request, 'index.html', {'hotels': hotels})


def hotel_details(request, slug):
    hotel = Hotel.objects.get(hotel_slug=slug)
    if request.method == 'POST':
        start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d')
        days_count = (end_date - start_date).days

        if days_count <= 0:
            messages.warning(request, "Invalid Booking Dates.")

        HotelBooking.objects.create(
            hotel=hotel,
            booking_user=HotelUser.objects.get(id=request.user.id),
            booking_start_date=start_date,
            booking_end_date=end_date,
            booking_price=hotel.hotel_offer_price * days_count
        )
        messages.success(request, "Booking confirmed.")
        return HttpResponseRedirect(request.path_info)
    return render(request, 'hotel_detail.html', {'hotel': hotel})
