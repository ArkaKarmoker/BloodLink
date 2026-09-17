from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta
from blood_app.forms import BloodRequestForm, DonorProfileForm, UserRegisterForm


class FormTests(TestCase):
    def test_blood_request_form_valid(self):
        data = {
            'patient_name': 'Test Patient',
            'blood_group': 'B+',
            'hospital_name': 'Central Clinic',
            'location': 'Dhaka',
            'hospital_address': 'Dhanmondi',
            'required_date': date.today() + timedelta(days=3),
            'bags_required': 2,
            'contact_number': '01711223344',
            'urgency': 'Urgent',
            'reason': 'Emergency platelet need for dengue patient.',
        }
        form = BloodRequestForm(data=data, is_create=True)
        self.assertTrue(form.is_valid(), form.errors)

    def test_blood_request_form_invalid_bags(self):
        data = {
            'patient_name': 'Test Patient',
            'blood_group': 'B+',
            'hospital_name': 'Central Clinic',
            'location': 'Dhaka',
            'required_date': date.today() + timedelta(days=3),
            'bags_required': 0,  # Invalid
            'contact_number': '01711223344',
            'urgency': 'Normal',
            'reason': 'Reason here',
        }
        form = BloodRequestForm(data=data, is_create=True)
        self.assertFalse(form.is_valid())
        self.assertIn('bags_required', form.errors)

    def test_blood_request_form_past_date(self):
        data = {
            'patient_name': 'Test Patient',
            'blood_group': 'B+',
            'hospital_name': 'Central Clinic',
            'location': 'Dhaka',
            'required_date': date.today() - timedelta(days=5),  # Past date
            'bags_required': 1,
            'contact_number': '01711223344',
            'urgency': 'Normal',
            'reason': 'Reason here',
        }
        form = BloodRequestForm(data=data, is_create=True)
        self.assertFalse(form.is_valid())
        self.assertIn('required_date', form.errors)

    def test_donor_profile_form_invalid_phone(self):
        data = {
            'blood_group': 'A+',
            'phone': 'not-a-number',
            'location': 'Feni',
            'is_available': True,
        }
        form = DonorProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_donor_profile_form_future_donation_date(self):
        data = {
            'blood_group': 'A+',
            'phone': '01711223344',
            'location': 'Feni',
            'last_donation_date': date.today() + timedelta(days=10),  # Future date
            'is_available': True,
        }
        form = DonorProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_donation_date', form.errors)

    def test_user_registration_duplicate_email(self):
        User.objects.create_user(username='existing', email='unique@example.com', password='pwd')
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'unique@example.com',  # Duplicate email
            'phone': '01711223344',
            'blood_group': 'O+',
            'location': 'Feni',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
