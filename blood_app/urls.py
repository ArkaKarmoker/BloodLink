from django.urls import path
from . import views

app_name = 'blood_app'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Donors
    path('donors/', views.donor_list_view, name='donor_list'),
    path('donors/<int:pk>/', views.donor_detail_view, name='donor_detail'),
    path('donor/create/', views.donor_create_view, name='donor_create'),
    path('donor/edit/', views.donor_edit_view, name='donor_edit'),
    path('donor/delete/', views.donor_delete_view, name='donor_delete'),
    path('donor/toggle-availability/', views.donor_toggle_availability, name='donor_toggle_availability'),
    
    # Blood Requests
    path('requests/', views.blood_request_list_view, name='request_list'),
    path('requests/<int:pk>/', views.blood_request_detail_view, name='request_detail'),
    path('requests/create/', views.blood_request_create_view, name='request_create'),
    path('requests/<int:pk>/edit/', views.blood_request_edit_view, name='request_edit'),
    path('requests/<int:pk>/delete/', views.blood_request_delete_view, name='request_delete'),
    path('requests/<int:pk>/status/', views.blood_request_update_status, name='request_update_status'),
    path('my-requests/', views.my_requests_view, name='my_requests'),
    
    # Information
    path('about/', views.about_view, name='about'),
]
