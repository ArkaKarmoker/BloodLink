from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django import forms
from .models import DonorProfile, BloodRequest, BloodDonationHistory


class EmailAdminAuthenticationForm(AdminAuthenticationForm):
    username = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'autofocus': True, 'placeholder': 'Enter admin email'})
    )


admin.site.login_form = EmailAdminAuthenticationForm
admin.site.site_header = "BloodLink Administration"
admin.site.site_title = "BloodLink Admin Portal"
admin.site.index_title = "Welcome to BloodLink Management Portal"



@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'blood_group', 'phone', 'location', 'is_available', 'last_donation_date', 'created_at')
    list_filter = ('blood_group', 'is_available', 'location')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone', 'location')
    list_editable = ('is_available',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'blood_group', 'bags_required', 'hospital_name', 'location', 'required_date', 'urgency', 'status', 'created_at')
    list_filter = ('status', 'urgency', 'blood_group', 'location')
    search_fields = ('patient_name', 'hospital_name', 'location', 'contact_number', 'requester__username')
    list_editable = ('status', 'urgency')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BloodDonationHistory)
class BloodDonationHistoryAdmin(admin.ModelAdmin):
    list_display = ('donor', 'donation_date', 'bags_donated', 'hospital')
    list_filter = ('donation_date',)
    search_fields = ('donor__user__username', 'hospital')
