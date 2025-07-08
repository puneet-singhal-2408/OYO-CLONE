from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register, name='register'),
    path('verify-account/<token>/', views.verify_email_token, name='verify_token'),
    path('send_otp/<email>', views.send_otp, name='send_otp'),
    path('<email>/verify-otp/', views.verify_otp, name='verify_otp'),

    path('vendor-login/', views.login_vendor, name='login_vendor'),
    path('vendor-register/', views.register_vendor, name='register_vendor'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-hotel/', views.add_hotel, name='add_hotel'),
    path('<slug>/upload-images', views.upload_images, name='upload_images'),
    path('delete-images/<image_id>', views.delete_images, name='delete_images'),
    path('<slug>/edit-hotel', views.edit_hotel, name='edit_hotel'),
    path('logout/', views.logout_view, name='logout_view'),
    ]

