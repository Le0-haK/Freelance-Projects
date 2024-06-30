from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from .models import Flight, Booking, Hotel, HotelBooking, HotelReview, FlightReview
from .forms import BookingForm, HotelForm, FlightForm, HotelBookingForm, HotelReviewForm, FlightReviewForm, CustomUserCreationForm

def home(request):
    return render(request, 'home.html')

def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'user_login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

@login_required
def view_flights(request):
    flights = Flight.objects.all()
    return render(request, 'view_flights.html', {'flights': flights})

@login_required
def book_ticket(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    available_seats = 60 - Booking.objects.filter(flight=flight).count()
    
    if request.method == 'POST':
        if available_seats > 0:
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.user = request.user
                booking.flight = flight
                booking.save()
                return redirect('my_bookings')
        else:
            return HttpResponse("Sorry, all seats on this flight are booked.")
    else:
        form = BookingForm()
    
    return render(request, 'book_ticket.html', {'form': form, 'flight': flight, 'available_seats': available_seats})


@login_required
def flight_reviews(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    reviews = FlightReview.objects.filter(flight=flight)
    
    if request.method == 'POST':
        form = FlightReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flight = flight
            review.save()
            return redirect('flight_reviews', flight_id=flight.id)
    else:
        form = FlightReviewForm()
    
    return render(request, 'flight_reviews.html', {'flight': flight, 'form': form, 'reviews': reviews})
    

@login_required
def my_bookings(request):
    flight_bookings = Booking.objects.filter(user=request.user)
    hotel_bookings = HotelBooking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'flight_bookings': flight_bookings, 'hotel_bookings': hotel_bookings})
      

def admin_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'admin_signup.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'admin_login.html', {'form': form})

@login_required
def admin_dashboard(request):
    if request.user.is_staff:
        # Fetch all bookings
        bookings = Booking.objects.all()
        # Fetch all flights
        flights = Flight.objects.all()
        # Fetch all hotels
        hotels = Hotel.objects.all()
        # Fetch all users (if needed)
        users = User.objects.all()
        return render(request, 'admin_dashboard.html', {'bookings': bookings, 'flights': flights, 'hotels': hotels, 'users': users})
    else:
        # Handling the case where the user is not authorized to view the admin dashboard
        return render(request, 'admin_dashboard.html', {'error_message': 'You are not authorized to view this page'})

@login_required
def add_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = FlightForm()
    return render(request, 'add_flight.html', {'form': form})

@login_required
def remove_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    flight.delete()
    return redirect('admin_dashboard')

from django.db.models import Q

def search_flights(request):
    query = request.GET.get('query')
    if query:
        flights = Flight.objects.filter(
            Q(flight_number__icontains=query) |  # Search by flight number
            Q(departure_date__icontains=query) |  # Search by departure date
            Q(departure_time__icontains=query)  # Search by departure time
        ).distinct()
    else:
        flights = Flight.objects.all()
    return render(request, 'view_flights.html', {'flights': flights})


@login_required
def user_details(request):
    users = User.objects.all()
    return render(request, 'user_details.html', {'users': users})

# Hotel's function
@login_required
def view_hotels(request):
    hotels = Hotel.objects.all()
    return render(request, 'view_hotels.html', {'hotels': hotels})


@login_required
def add_hotels(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = HotelForm()
    return render(request, 'add_hotels.html', {'form': form})

@login_required
def book_hotel(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)

    if request.method == 'POST':
        form = HotelBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.hotel = hotel
            booking.save()
            return redirect('my_bookings')
    else:
        form = HotelBookingForm()

    return render(request, 'book_hotel.html', {'form': form, 'hotel': hotel})    


@login_required
def hotel_reviews(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    reviews = HotelReview.objects.filter(hotel=hotel)
    
    if request.method == 'POST':
        form = HotelReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.hotel = hotel
            review.save()
            return redirect('hotel_reviews', hotel_id=hotel.id)
    else:
        form = HotelReviewForm()
    
    return render(request, 'hotel_reviews.html', {'hotel': hotel, 'form': form, 'reviews': reviews})


def search_hotels(request):
    query = request.GET.get('query')
    if query:
        hotels = Hotel.objects.filter(name__icontains=query) | Hotel.objects.filter(address__icontains=query)
    else:
        hotels = Hotel.objects.all()
    return render(request, 'view_hotels.html', {'hotels': hotels})

@login_required
def remove_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.delete()
    return redirect('admin_dashboard')
