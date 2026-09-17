from django.db import models
from django.contrib.auth.models import User
from datetime import date
from .utils import (
    BLOOD_GROUP_CHOICES,
    DONATE_COMPATIBILITY,
    RECEIVE_COMPATIBILITY,
    get_donor_eligibility,
)


class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    phone = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    location = models.CharField(max_length=100, help_text="City, District, or Area (e.g., Feni, Dhaka, Chittagong)")
    address = models.CharField(max_length=255, blank=True, help_text="Detailed address or preferred donation zone")
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='donors/', blank=True, null=True)
    last_donation_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True, verbose_name="Available for Donation")
    description = models.TextField(blank=True, help_text="Short bio, experience, or donor notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_available', '-updated_at']
        verbose_name = 'Donor Profile'
        verbose_name_plural = 'Donor Profiles'

    def __str__(self):
        return f"{self.display_name} ({self.blood_group}) - {self.location}"

    @property
    def display_name(self):
        full_name = self.user.get_full_name()
        return full_name if full_name else self.user.username

    @property
    def eligibility(self):
        return get_donor_eligibility(self.last_donation_date)

    @property
    def can_donate_to(self):
        return DONATE_COMPATIBILITY.get(self.blood_group, [])

    @property
    def can_receive_from(self):
        return RECEIVE_COMPATIBILITY.get(self.blood_group, [])

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None


class BloodRequest(models.Model):
    URGENCY_CHOICES = [
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
        ('Critical', 'Critical (Emergency)'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Fulfilled', 'Fulfilled'),
        ('Cancelled', 'Cancelled'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    hospital_name = models.CharField(max_length=150)
    location = models.CharField(max_length=100, help_text="City, District, or Area")
    hospital_address = models.CharField(max_length=255, blank=True)
    required_date = models.DateField()
    bags_required = models.PositiveIntegerField(default=1)
    contact_number = models.CharField(max_length=20)
    reason = models.TextField(help_text="Condition / reason for blood requirement")
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='Normal')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blood Request'
        verbose_name_plural = 'Blood Requests'

    def __str__(self):
        return f"{self.patient_name} - {self.blood_group} ({self.bags_required} bags) at {self.hospital_name}"

    @property
    def compatible_donor_groups(self):
        return RECEIVE_COMPATIBILITY.get(self.blood_group, [])

    def get_matching_donors(self):
        """Returns eligible donors matching compatible blood groups, prioritizing same location and availability."""
        compatible_groups = self.compatible_donor_groups
        return DonorProfile.objects.filter(
            blood_group__in=compatible_groups,
            is_available=True
        ).order_by(
            models.Case(
                models.When(location__iexact=self.location, then=models.Value(0)),
                default=models.Value(1),
                output_field=models.IntegerField(),
            ),
            '-updated_at'
        )


class BloodDonationHistory(models.Model):
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name='donation_records')
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name='fulfilled_donations')
    donation_date = models.DateField(default=date.today)
    bags_donated = models.PositiveIntegerField(default=1)
    hospital = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-donation_date']
        verbose_name = 'Donation History'
        verbose_name_plural = 'Donation Histories'

    def __str__(self):
        return f"{self.donor.display_name} - {self.bags_donated} bag(s) on {self.donation_date}"
