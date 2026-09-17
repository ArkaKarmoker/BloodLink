from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta
from blood_app.models import DonorProfile, BloodRequest


class Command(BaseCommand):
    help = 'Seeds database with realistic sample donors and emergency blood requests.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding initial data for BloodLink...')

        # Sample Donors
        sample_donors = [
            {
                'username': 'rahim_donor',
                'first_name': 'Rahim',
                'last_name': 'Ahmed',
                'email': 'rahim.ahmed@example.com',
                'blood_group': 'O+',
                'phone': '01711223344',
                'location': 'Feni',
                'address': 'Trunk Road, Feni Sadar',
                'last_donation_date': date.today() - timedelta(days=110),
                'is_available': True,
                'description': 'Regular voluntary donor. Happy to help anytime in Feni and nearby areas.',
            },
            {
                'username': 'karim_donor',
                'first_name': 'Karim',
                'last_name': 'Uddin',
                'email': 'karim.u@example.com',
                'blood_group': 'A+',
                'phone': '01812345678',
                'location': 'Feni',
                'address': 'SSK Road, Feni',
                'last_donation_date': date.today() - timedelta(days=45),
                'is_available': False,
                'description': 'Recently donated blood for a surgery patient.',
            },
            {
                'username': 'tanjila_donor',
                'first_name': 'Tanjila',
                'last_name': 'Akter',
                'email': 'tanjila.a@example.com',
                'blood_group': 'B+',
                'phone': '01998765432',
                'location': 'Dhaka',
                'address': 'Dhanmondi, Dhaka',
                'last_donation_date': date.today() - timedelta(days=120),
                'is_available': True,
                'description': 'University student and voluntary donor.',
            },
            {
                'username': 'sakib_donor',
                'first_name': 'Sakib',
                'last_name': 'Hasan',
                'email': 'sakib.h@example.com',
                'blood_group': 'O-',
                'phone': '01755667788',
                'location': 'Chittagong',
                'address': 'Agrabad, Chittagong',
                'last_donation_date': date.today() - timedelta(days=150),
                'is_available': True,
                'description': 'Universal donor (O-). Available for emergency calls.',
            },
            {
                'username': 'sumon_donor',
                'first_name': 'Sumon',
                'last_name': 'Paul',
                'email': 'sumon.p@example.com',
                'blood_group': 'AB+',
                'phone': '01611223399',
                'location': 'Sylhet',
                'address': 'Zindabazar, Sylhet',
                'last_donation_date': None,
                'is_available': True,
                'description': 'Ready for first-time donation.',
            },
            {
                'username': 'fatima_donor',
                'first_name': 'Fatima',
                'last_name': 'Begum',
                'email': 'fatima.b@example.com',
                'blood_group': 'A-',
                'phone': '01822334455',
                'location': 'Feni',
                'address': 'Hospital Road, Feni',
                'last_donation_date': date.today() - timedelta(days=100),
                'is_available': True,
                'description': 'A- rare blood donor in Feni district.',
            }
        ]

        # Create or update Administrator
        admin_user, admin_created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Admin',
                'last_name': 'BloodLink',
                'email': 'admin@bloodlink.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if admin_created:
            admin_user.set_password('admin12345')
            admin_user.save()
        else:
            admin_user.email = 'admin@bloodlink.com'
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.set_password('admin12345')
            admin_user.save()

        created_users = []
        for donor_data in sample_donors:
            username = donor_data['username']
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': donor_data['first_name'],
                    'last_name': donor_data['last_name'],
                    'email': donor_data['email'],
                }
            )
            if created:
                user.set_password('donor12345')
                user.save()

            created_users.append(user)

            DonorProfile.objects.update_or_create(
                user=user,
                defaults={
                    'phone': donor_data['phone'],
                    'blood_group': donor_data['blood_group'],
                    'location': donor_data['location'],
                    'address': donor_data['address'],
                    'last_donation_date': donor_data['last_donation_date'],
                    'is_available': donor_data['is_available'],
                    'description': donor_data['description'],
                }
            )

        # Sample Blood Requests
        requester = created_users[0]
        sample_requests = [
            {
                'patient_name': 'Mohammad Rafiq',
                'blood_group': 'O+',
                'hospital_name': 'Feni Modern Sadar Hospital',
                'location': 'Feni',
                'hospital_address': 'Hospital Road, Feni Sadar',
                'required_date': date.today() + timedelta(days=2),
                'bags_required': 2,
                'contact_number': '01711223344',
                'urgency': 'Critical',
                'status': 'Pending',
                'reason': 'Patient undergoing emergency orthopedic surgery following a road accident. Immediate whole blood transfusion required.',
            },
            {
                'patient_name': 'Nusrat Jahan',
                'blood_group': 'A+',
                'hospital_name': 'Square Hospital',
                'location': 'Dhaka',
                'hospital_address': 'Panthapath, Dhaka',
                'required_date': date.today() + timedelta(days=1),
                'bags_required': 3,
                'contact_number': '01812345678',
                'urgency': 'Urgent',
                'status': 'Pending',
                'reason': 'Dengue complications with dropping platelet count. A+ donors requested for direct cross-matching.',
            },
            {
                'patient_name': 'Tanvir Alam',
                'blood_group': 'B+',
                'hospital_name': 'Chittagong Medical College Hospital',
                'location': 'Chittagong',
                'hospital_address': 'KB Fazlul Kader Road, CMCH Ward 4',
                'required_date': date.today() + timedelta(days=4),
                'bags_required': 1,
                'contact_number': '01998765432',
                'urgency': 'Normal',
                'status': 'Fulfilled',
                'reason': 'Scheduled thalassemic regular blood transfusion.',
            },
            {
                'patient_name': 'Rehana Parveen',
                'blood_group': 'O-',
                'hospital_name': 'Z.H. Sikder Women\'s Medical College',
                'location': 'Dhaka',
                'hospital_address': 'Rayerbazar, Dhaka',
                'required_date': date.today() + timedelta(days=3),
                'bags_required': 2,
                'contact_number': '01755667788',
                'urgency': 'Critical',
                'status': 'Pending',
                'reason': 'Rare negative blood group required for cesarean delivery.',
            },
        ]

        for req_data in sample_requests:
            BloodRequest.objects.get_or_create(
                requester=requester,
                patient_name=req_data['patient_name'],
                defaults=req_data,
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded sample donors and blood requests!'))
