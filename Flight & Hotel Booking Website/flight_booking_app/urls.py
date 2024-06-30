from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user-signup/', views.user_signup, name='user_signup'),
    path('user-login/', views.user_login, name='user_login'),
    path('user-logout/', views.user_logout, name='user_logout'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('view-flights/', views.view_flights, name='view_flights'),
    path('flight_reviews/<int:flight_id>/', views.flight_reviews, name='flight_reviews'),
    path('book-ticket/<int:flight_id>/', views.book_ticket, name='book_ticket'),
    path('book-hotel/<int:hotel_id>/', views.book_hotel, name='book_hotel'),
    path('hotel_reviews/<int:hotel_id>/', views.hotel_reviews, name='hotel_reviews'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('admin-signup/', views.admin_signup, name='admin_signup'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-flight/', views.add_flight, name='add_flight'),
    path('remove-flight/<int:flight_id>/', views.remove_flight, name='remove_flight'),
    path('remove-hotel/<int:hotel_id>/', views.remove_hotel, name='remove_hotel'), 
    path('search_hotels/', views.search_hotels, name='search_hotels'),
    path('search_flights/', views.search_flights, name='search_flights'),
    path('user-details/', views.user_details, name='user_details'),
    path('view-hotels/', views.view_hotels, name='view_hotels'),
    path('add-hotels/', views.add_hotels, name='add_hotels')
]
