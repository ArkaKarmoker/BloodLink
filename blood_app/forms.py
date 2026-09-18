from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from datetime import date
from .models import DonorProfile, BloodRequest, BloodDonationHistory
from .utils import validate_phone_number, BLOOD_GROUP_CHOICES



class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Last Name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input', 'placeholder': 'Email Address'
    }))
    phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Phone Number (e.g. 017XXXXXXXX)'
    }))
    blood_group = forms.ChoiceField(choices=[('', '-- Select Blood Group --')] + BLOOD_GROUP_CHOICES, required=True, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    location = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Location (e.g. Dhaka, Tangail, Chittagong)'
    }))
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'class': 'form-input', 'type': 'date'
    }))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-input-file'
    }))
    register_as_donor = forms.BooleanField(required=False, initial=True, label="Register me as an available blood donor", widget=forms.CheckboxInput(attrs={
        'class': 'form-checkbox'
    }))

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'username',
            'blood_group',
            'location',
            'date_of_birth',
            'profile_picture',
            'register_as_donor',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Choose a Username'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not validate_phone_number(phone):
            raise ValidationError("Please enter a valid mobile number (e.g., 01XXXXXXXXX or international format).")
        return phone


class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email__iexact=email).exists():
            raise ValidationError("This email is already in use by another account.")
        return email


class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = [
            'blood_group',
            'phone',
            'location',
            'address',
            'date_of_birth',
            'profile_picture',
            'last_donation_date',
            'is_available',
            'description',
        ]
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '01XXXXXXXXX'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City / Area (e.g. Dhaka, Tangail, Chittagong)'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Street / Area / Landmarks'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-input-file'}),
            'last_donation_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Tell us about your donation experience or availability constraints...'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not validate_phone_number(phone):
            raise ValidationError("Please enter a valid contact phone number.")
        return phone

    def clean_last_donation_date(self):
        last_date = self.cleaned_data.get('last_donation_date')
        if last_date and last_date > date.today():
            raise ValidationError("Last donation date cannot be in the future.")
        return last_date


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = [
            'patient_name',
            'blood_group',
            'hospital_name',
            'location',
            'hospital_address',
            'required_date',
            'bags_required',
            'contact_number',
            'urgency',
            'status',
            'reason',
        ]
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Patient Full Name'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'hospital_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. XYZ Central Hospital'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City / District (e.g. Dhaka, Tangail, Chittagong)'}),
            'hospital_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Hospital Ward / Bed / Street address'}),
            'required_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'bags_required': forms.NumberInput(attrs={'class': 'form-input', 'min': '1', 'max': '50'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Emergency Contact Number'}),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Describe reason (e.g. Surgery, Dengue, Thalassemia, Accident) and specific instructions...'}),
        }

    def __init__(self, *args, **kwargs):
        is_create = kwargs.pop('is_create', False)
        super().__init__(*args, **kwargs)
        if is_create:
            # Hide status on initial create; default is Pending
            self.fields.pop('status', None)

    def clean_bags_required(self):
        bags = self.cleaned_data.get('bags_required')
        if bags is None or bags <= 0:
            raise ValidationError("Number of bags must be at least 1.")
        return bags

    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number')
        if not validate_phone_number(contact):
            raise ValidationError("Please provide a valid contact phone number.")
        return contact

    def clean_required_date(self):
        req_date = self.cleaned_data.get('required_date')
        if req_date and req_date < date.today():
            raise ValidationError("Required date cannot be in the past.")
        return req_date


class BloodRequestStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your registered email',
            'id': 'id_email',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
            'id': 'id_password',
        })
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise ValidationError("Invalid email address or password.")
            elif not self.user_cache.is_active:
                raise ValidationError("This account is inactive.")
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

