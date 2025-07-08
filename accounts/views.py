import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import HotelUser, HotelVendor, Hotel, Amenities, HotelImages
from django.db.models import Q
from django.contrib import messages
from .utils import generate_randon_token, send_email_token, send_otp_to_email, generate_slug
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Create your views here.
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelUser.objects.filter(email=email)

        if not hotel_user.exists():
            messages.warning(request, f"No account found with {email}")
            return redirect(reverse('login_page'))

        if not hotel_user[0].is_verified:
            messages.warning(request, f"Account not verified")
            return redirect(reverse('login_page'))

        hotel_user = authenticate(username=hotel_user[0].username, password=password)

        if hotel_user:
            messages.success(request, "Welcome to OYO clone")
            login(request, hotel_user)
            return redirect('/')

        messages.warning(request, f"Invalid credentials")
        return redirect(reverse('login_page'))

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelUser.objects.filter(Q(email=email) | Q(phone_number=phone_number))

        if hotel_user.exists():
            messages.warning(request, "Account with email or phone number already exists")
            return redirect(reverse('register'))

        hotel_user = HotelUser.objects.create(
            username=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            email_token=generate_randon_token()
        )
        hotel_user.set_password(password)
        hotel_user.is_verified = True
        hotel_user.save()
        # commented as gmail is blocked on network
        # send_email_token(email, hotel_user.email_token)

        messages.success(request, f"Account created email is sent on {email}")
        return redirect(reverse('register'))

    return render(request, 'register.html')


def verify_email_token(request, token):
    hotel_user = HotelUser.objects.get(email_token=token)
    try:
        if hotel_user:
            hotel_user.is_verified = True
            hotel_user.save()
    except:
        return HttpResponse("Invalid email token")


def send_otp(request, email):
    hotel_user = HotelUser.objects.filter(email=email)
    if not hotel_user.exists():
        messages.warning(request, f"No account found with {email}")
        return redirect(reverse('login'))

    hotel_user.update(otp=random.randint(1000, 9999))

    # commented as gmail is blocked on network
    # send_otp_to_email(email, hotel_user.otp)

    return redirect(f'/account/{email}/verify-otp/')


def verify_otp(request, email):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        hotel_user = HotelUser.objects.get(email=email)

        if otp == hotel_user.otp:
            messages.success(request, "Login Success")
            login(request, hotel_user)
            return redirect('/')
        messages.warning(request, "Invalid OTP")
        return redirect(f'/account/{email}/verify-otp/')
    return render(request, 'verify_otp.html')


# vendor login and registration handling

def login_vendor(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_vendor = HotelVendor.objects.filter(email=email)

        if not hotel_vendor.exists():
            messages.warning(request, f"No account found with {email}")
            return redirect(reverse('login_vendor'))

        if not hotel_vendor[0].is_verified:
            messages.warning(request, f"Account not verified")
            return redirect(reverse('login_vendor'))

        hotel_vendor = authenticate(username=hotel_vendor[0].username, password=password)

        if hotel_vendor:
            messages.success(request, "Welcome to OYO clone")
            login(request, hotel_vendor)
            return redirect(reverse('dashboard'))

        messages.warning(request, f"Invalid credentials")
        return redirect(reverse('login_vendor'))

    return render(request, 'vendor/login_vendor.html')


def register_vendor(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_vendor = HotelVendor.objects.filter(Q(email=email) | Q(phone_number=phone_number))

        if hotel_vendor.exists():
            messages.warning(request, "Account with email or phone number already exists")
            return redirect(reverse('register_vendor'))

        hotel_vendor = HotelVendor.objects.create(
            username=phone_number,
            first_name=first_name,
            last_name=last_name,
            business_name=business_name,
            email=email,
            phone_number=phone_number,
            email_token=generate_randon_token()
        )
        hotel_vendor.set_password(password)
        hotel_vendor.is_verified = True
        hotel_vendor.save()
        # commented as gmail is blocked on network
        # send_email_token(email, hotel_user.email_token)

        messages.success(request, f"Account created email is sent on {email}")
        return redirect(reverse('register_vendor'))

    return render(request, 'vendor/register_vendor.html')


@login_required(login_url='login_vendor')
def dashboard(request):
    context = {'hotels': Hotel.objects.filter(hotel_owner=request.user)}
    return render(request, 'vendor/vendor_dashboard.html', context=context)


@login_required(login_url='login_vendor')
def add_hotel(request):
    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        amenities = request.POST.getlist('amenities')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')
        hotel_slug = generate_slug(hotel_name)
        hotel_vendor = HotelVendor.objects.get(id=request.user.id)
        hotel_obj = Hotel.objects.create(
            hotel_name=hotel_name,
            hotel_description=hotel_description,
            hotel_address=hotel_location,
            hotel_price=hotel_price,
            hotel_offer_price=hotel_offer_price,
            hotel_location=hotel_location,
            hotel_slug=hotel_slug,
            hotel_owner=hotel_vendor
        )
        for amenity in amenities:
            amenity = Amenities.objects.get(id=amenity)
            hotel_obj.amenities.add(amenity)
            hotel_obj.save()
        messages.success(request, "Hotel created")
        return redirect(reverse('add_hotel'))
    amenities = Amenities.objects.all()
    return render(request, 'vendor/add_hotel.html', context={'amenities': amenities})


@login_required(login_url='login_vendor')
def upload_images(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    if request.method == 'POST':
        image = request.FILES['image']
        HotelImages.objects.create(
            hotel=hotel_obj,
            image=image
        )
        return HttpResponseRedirect(request.path_info)

    return render(request, 'vendor/upload_images.html',
                  context={'images': hotel_obj.hotel_images.all()})


@login_required(login_url='login_vendor')
def delete_images(request, image_id):
    hotel_image = HotelImages.objects.get(id=image_id)
    hotel_image.delete()
    messages.success(request, "hotel image deleted")
    return redirect(reverse('dashboard'))


@login_required(login_url='login_vendor')
def edit_hotel(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    if request.user.id != hotel_obj.hotel_owner.id:
        return HttpResponse("You are not authorized for this action")
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')

        # update hotel details
        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location
        hotel_obj.save()
        messages.success(request, "Hotel details updated")

    return render(request, 'vendor/edit_hotel.html', context={'hotel': hotel_obj})


def logout_view(request):
    logout(request)
    return redirect('/account/login/')
