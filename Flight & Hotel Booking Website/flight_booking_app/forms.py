from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Hotel, Flight, HotelBooking, HotelReview, FlightReview

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['flight']

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'address']

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_number', 'departure_date', 'departure_time']

class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = ['hotel', 'check_in_date', 'check_out_date']

class HotelReviewForm(forms.ModelForm):
    class Meta:
        model = HotelReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),  # Set min and max attributes for rating
        }

class FlightReviewForm(forms.ModelForm):
    class Meta:
        model = FlightReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),  # Limit rating to 1-5
        }        

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        error_messages={
            'required': 'This field is required.',
            'unique': 'A user with that username already exists.',
        }
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        error_messages={
            'required': 'This field is required.',
        }
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}),
        error_messages={
            'required': 'This field is required.',
        }
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields must match.")
        
        # Add custom validation rules here if needed
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user