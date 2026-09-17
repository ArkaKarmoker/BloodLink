from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Count
from datetime import date

from .models import DonorProfile, BloodRequest, BloodDonationHistory
from .forms import (
    UserRegisterForm,
    UserProfileUpdateForm,
    DonorProfileForm,
    BloodRequestForm,
    BloodRequestStatusUpdateForm,
    EmailLoginForm,
)
from .utils import (
    BLOOD_GROUP_CHOICES,
    DONATE_COMPATIBILITY,
    RECEIVE_COMPATIBILITY,
)


def home_view(request):
    total_donors = DonorProfile.objects.count()
    available_donors = DonorProfile.objects.filter(is_available=True).count()
    total_requests = BloodRequest.objects.count()
    fulfilled_requests = BloodRequest.objects.filter(status='Fulfilled').count()
    pending_requests_count = BloodRequest.objects.filter(status='Pending').count()

    # Urgent & Recent Requests
    urgent_requests = BloodRequest.objects.filter(status='Pending').order_by(
        models_order_urgency(), 'required_date'
    )[:4]

    # Recent Available Donors
    featured_donors = DonorProfile.objects.filter(is_available=True).select_related('user')[:4]

    context = {
        'total_donors': total_donors,
        'available_donors': available_donors,
        'total_requests': total_requests,
        'fulfilled_requests': fulfilled_requests,
        'pending_requests_count': pending_requests_count,
        'urgent_requests': urgent_requests,
        'featured_donors': featured_donors,
        'blood_groups': [bg[0] for bg in BLOOD_GROUP_CHOICES],
        'compatibility_donate': DONATE_COMPATIBILITY,
        'compatibility_receive': RECEIVE_COMPATIBILITY,
    }
    return render(request, 'blood_app/home.html', context)


def models_order_urgency():
    from django.db.models import Case, When, Value, IntegerField
    return Case(
        When(urgency='Critical', then=Value(1)),
        When(urgency='Urgent', then=Value(2)),
        When(urgency='Normal', then=Value(3)),
        default=Value(4),
        output_field=IntegerField(),
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect('blood_app:dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # If registered with donor profile info
            register_donor = form.cleaned_data.get('register_as_donor', False)
            phone = form.cleaned_data.get('phone')
            blood_group = form.cleaned_data.get('blood_group')
            location = form.cleaned_data.get('location')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            profile_pic = form.cleaned_data.get('profile_picture')

            if register_donor and blood_group and location:
                DonorProfile.objects.create(
                    user=user,
                    phone=phone,
                    blood_group=blood_group,
                    location=location,
                    date_of_birth=date_of_birth,
                    profile_picture=profile_pic,
                    is_available=True,
                )
                messages.success(request, f"Welcome {user.first_name}! Your account and donor profile have been created.")
            else:
                messages.success(request, f"Welcome {user.first_name}! Your account has been created.")

            login(request, user, backend='blood_app.backends.EmailBackend')
            return redirect('blood_app:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'blood_app/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('blood_app:dashboard')

    if request.method == 'POST':
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('blood_app:dashboard')
        else:
            messages.error(request, "Invalid email address or password.")
    else:
        form = EmailLoginForm(request)

    return render(request, 'blood_app/login.html', {'form': form})



def logout_view(request):
    if request.method in ['POST', 'GET']:
        logout(request)
        messages.info(request, "You have been logged out successfully.")
    return redirect('blood_app:home')


@login_required
def profile_view(request):
    user = request.user
    donor_profile = getattr(user, 'donor_profile', None)

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile information updated successfully.")
            return redirect('blood_app:profile')
    else:
        form = UserProfileUpdateForm(instance=user)

    context = {
        'form': form,
        'user': user,
        'donor_profile': donor_profile,
    }
    return render(request, 'blood_app/profile.html', context)


@login_required
def dashboard_view(request):
    user = request.user
    donor_profile = getattr(user, 'donor_profile', None)
    my_requests = BloodRequest.objects.filter(requester=user).order_by('-created_at')
    
    # User's stats
    requests_count = my_requests.count()
    pending_count = my_requests.filter(status='Pending').count()
    fulfilled_count = my_requests.filter(status='Fulfilled').count()

    context = {
        'user': user,
        'donor_profile': donor_profile,
        'my_requests': my_requests[:5],
        'total_my_requests': requests_count,
        'pending_count': pending_count,
        'fulfilled_count': fulfilled_count,
    }
    return render(request, 'blood_app/dashboard.html', context)


# --- Donor CRUD & Discovery ---

def donor_list_view(request):
    blood_group = request.GET.get('blood_group', '').strip()
    location = request.GET.get('location', '').strip()
    availability = request.GET.get('availability', 'all').strip()

    donors = DonorProfile.objects.select_related('user').all()

    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    if location:
        donors = donors.filter(
            Q(location__icontains=location) | Q(address__icontains=location)
        )

    if availability == 'available':
        donors = donors.filter(is_available=True)
    elif availability == 'unavailable':
        donors = donors.filter(is_available=False)

    paginator = Paginator(donors, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'blood_groups': BLOOD_GROUP_CHOICES,
        'selected_blood_group': blood_group,
        'selected_location': location,
        'selected_availability': availability,
        'total_results': donors.count(),
    }
    return render(request, 'blood_app/donor_list.html', context)


def donor_detail_view(request, pk):
    donor = get_object_or_404(DonorProfile.objects.select_related('user'), pk=pk)
    context = {
        'donor': donor,
        'can_donate_to': donor.can_donate_to,
        'can_receive_from': donor.can_receive_from,
        'eligibility': donor.eligibility,
        'is_owner': request.user.is_authenticated and request.user == donor.user,
    }
    return render(request, 'blood_app/donor_detail.html', context)


@login_required
def donor_create_view(request):
    if hasattr(request.user, 'donor_profile'):
        messages.info(request, "You already have a donor profile. You can update it here.")
        return redirect('blood_app:donor_edit')

    if request.method == 'POST':
        form = DonorProfileForm(request.POST, request.FILES)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.save()
            messages.success(request, "Your donor profile has been created successfully! Thank you for being a lifesaver.")
            return redirect('blood_app:donor_detail', pk=donor.pk)
    else:
        form = DonorProfileForm()

    return render(request, 'blood_app/donor_form.html', {
        'form': form,
        'title': 'Create Donor Profile',
        'button_text': 'Save Donor Profile',
        'is_create': True,
    })


@login_required
def donor_edit_view(request):
    try:
        donor = request.user.donor_profile
    except DonorProfile.DoesNotExist:
        messages.warning(request, "You don't have a donor profile yet. Create one now!")
        return redirect('blood_app:donor_create')

    if request.method == 'POST':
        form = DonorProfileForm(request.POST, request.FILES, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, "Donor profile updated successfully.")
            return redirect('blood_app:donor_detail', pk=donor.pk)
    else:
        form = DonorProfileForm(instance=donor)

    return render(request, 'blood_app/donor_form.html', {
        'form': form,
        'title': 'Edit Donor Profile',
        'button_text': 'Update Profile',
        'is_create': False,
        'donor': donor,
    })


@login_required
def donor_delete_view(request):
    try:
        donor = request.user.donor_profile
    except DonorProfile.DoesNotExist:
        messages.warning(request, "No donor profile found to delete.")
        return redirect('blood_app:dashboard')

    if request.method == 'POST':
        donor.delete()
        messages.success(request, "Your donor profile has been removed.")
        return redirect('blood_app:dashboard')

    return render(request, 'blood_app/donor_confirm_delete.html', {'donor': donor})


@login_required
def donor_toggle_availability(request):
    if request.method == 'POST':
        try:
            donor = request.user.donor_profile
            donor.is_available = not donor.is_available
            donor.save()
            status_str = "Available" if donor.is_available else "Not Available"
            messages.success(request, f"Your donation status changed to: {status_str}.")
        except DonorProfile.DoesNotExist:
            messages.error(request, "You do not have a donor profile yet.")
    return redirect(request.META.get('HTTP_REFERER', 'blood_app:dashboard'))


# --- Blood Request CRUD ---

def blood_request_list_view(request):
    blood_group = request.GET.get('blood_group', '').strip()
    location = request.GET.get('location', '').strip()
    status = request.GET.get('status', '').strip()
    urgency = request.GET.get('urgency', '').strip()

    requests_qs = BloodRequest.objects.select_related('requester').all()

    if blood_group:
        requests_qs = requests_qs.filter(blood_group=blood_group)

    if location:
        requests_qs = requests_qs.filter(
            Q(location__icontains=location) | Q(hospital_name__icontains=location)
        )

    if status:
        requests_qs = requests_qs.filter(status=status)
    else:
        # Default prioritize Pending
        pass

    if urgency:
        requests_qs = requests_qs.filter(urgency=urgency)

    # Order by urgency and date
    requests_qs = requests_qs.order_by(
        models_order_urgency(),
        '-created_at'
    )

    paginator = Paginator(requests_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'blood_groups': BLOOD_GROUP_CHOICES,
        'status_choices': BloodRequest.STATUS_CHOICES,
        'urgency_choices': BloodRequest.URGENCY_CHOICES,
        'selected_blood_group': blood_group,
        'selected_location': location,
        'selected_status': status,
        'selected_urgency': urgency,
        'total_results': requests_qs.count(),
    }
    return render(request, 'blood_app/request_list.html', context)


def blood_request_detail_view(request, pk):
    blood_request = get_object_or_404(BloodRequest.objects.select_related('requester'), pk=pk)
    matching_donors = blood_request.get_matching_donors()[:6]
    is_owner = request.user.is_authenticated and request.user == blood_request.requester

    context = {
        'request_obj': blood_request,
        'matching_donors': matching_donors,
        'is_owner': is_owner,
        'status_form': BloodRequestStatusUpdateForm(instance=blood_request) if is_owner else None,
    }
    return render(request, 'blood_app/request_detail.html', context)


@login_required
def blood_request_create_view(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST, is_create=True)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.status = 'Pending'
            blood_request.save()
            messages.success(request, f"Blood request for {blood_request.patient_name} created successfully!")
            return redirect('blood_app:request_detail', pk=blood_request.pk)
    else:
        form = BloodRequestForm(is_create=True)

    return render(request, 'blood_app/request_form.html', {
        'form': form,
        'title': 'Post a Blood Request',
        'button_text': 'Submit Blood Request',
        'is_create': True,
    })


@login_required
def blood_request_edit_view(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)

    if blood_request.requester != request.user:
        raise PermissionDenied("You are not authorized to edit this blood request.")

    if request.method == 'POST':
        form = BloodRequestForm(request.POST, instance=blood_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Blood request updated successfully.")
            return redirect('blood_app:request_detail', pk=blood_request.pk)
    else:
        form = BloodRequestForm(instance=blood_request)

    return render(request, 'blood_app/request_form.html', {
        'form': form,
        'title': 'Edit Blood Request',
        'button_text': 'Update Blood Request',
        'is_create': False,
        'blood_request': blood_request,
    })


@login_required
def blood_request_delete_view(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)

    if blood_request.requester != request.user:
        raise PermissionDenied("You are not authorized to delete this blood request.")

    if request.method == 'POST':
        patient_name = blood_request.patient_name
        blood_request.delete()
        messages.success(request, f"Blood request for {patient_name} has been deleted.")
        return redirect('blood_app:my_requests')

    return render(request, 'blood_app/request_confirm_delete.html', {'blood_request': blood_request})


@login_required
def blood_request_update_status(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)

    if blood_request.requester != request.user:
        raise PermissionDenied("You are not authorized to update the status of this blood request.")

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Fulfilled', 'Cancelled']:
            blood_request.status = new_status
            blood_request.save()
            messages.success(request, f"Request status updated to: {new_status}")
    
    return redirect('blood_app:request_detail', pk=blood_request.pk)


@login_required
def my_requests_view(request):
    requests_list = BloodRequest.objects.filter(requester=request.user).order_by('-created_at')
    
    paginator = Paginator(requests_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_requests': requests_list.count(),
    }
    return render(request, 'blood_app/my_requests.html', context)


def about_view(request):
    return render(request, 'blood_app/about.html', {
        'compatibility_donate': DONATE_COMPATIBILITY,
        'compatibility_receive': RECEIVE_COMPATIBILITY,
    })
