from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta
from blood_app.models import DonorProfile, BloodRequest


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            first_name='Rahim',
            last_name='Ahmed',
            email='rahim@example.com',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            first_name='Karim',
            last_name='Uddin',
            email='karim@example.com',
            password='password123'
        )

        self.donor1 = DonorProfile.objects.create(
            user=self.user1,
            blood_group='O+',
            phone='01711223344',
            location='Feni',
            is_available=True
        )

        self.request1 = BloodRequest.objects.create(
            requester=self.user1,
            patient_name='Patient Rahim',
            blood_group='O+',
            hospital_name='Feni Hospital',
            location='Feni',
            required_date=date.today() + timedelta(days=2),
            bags_required=2,
            contact_number='01711223344',
            urgency='Urgent',
            status='Pending',
            reason='Accident surgery'
        )

    def test_home_view(self):
        response = self.client.get(reverse('blood_app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Find a Donor")
        self.assertEqual(response.context['total_donors'], 1)
        self.assertEqual(response.context['total_requests'], 1)

    def test_donor_list_and_filters(self):
        # Unfiltered
        response = self.client.get(reverse('blood_app:donor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rahim Ahmed")

        # Filter matching
        res_match = self.client.get(reverse('blood_app:donor_list'), {'blood_group': 'O+', 'location': 'Feni'})
        self.assertEqual(res_match.status_code, 200)
        self.assertEqual(len(res_match.context['page_obj']), 1)

        # Filter non-matching
        res_none = self.client.get(reverse('blood_app:donor_list'), {'blood_group': 'AB-'})
        self.assertEqual(res_none.status_code, 200)
        self.assertEqual(len(res_none.context['page_obj']), 0)

    def test_donor_detail_view(self):
        response = self.client.get(reverse('blood_app:donor_detail', kwargs={'pk': self.donor1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rahim Ahmed")
        self.assertContains(response, "O+")

    def test_donor_toggle_availability(self):
        self.client.login(username='user1', password='password123')
        self.assertTrue(self.donor1.is_available)
        response = self.client.post(reverse('blood_app:donor_toggle_availability'))
        self.assertEqual(response.status_code, 302)
        self.donor1.refresh_from_db()
        self.assertFalse(self.donor1.is_available)

    def test_donor_crud_permission(self):
        # Anonymous cannot access create
        res_anon = self.client.get(reverse('blood_app:donor_create'))
        self.assertEqual(res_anon.status_code, 302)

        # user2 has no donor profile, can create
        self.client.login(username='user2', password='password123')
        res_create = self.client.post(reverse('blood_app:donor_create'), {
            'blood_group': 'B+',
            'phone': '01811223344',
            'location': 'Dhaka',
            'is_available': True,
        })
        self.assertEqual(res_create.status_code, 302)
        self.assertTrue(DonorProfile.objects.filter(user=self.user2).exists())

    def test_blood_request_list_and_filters(self):
        response = self.client.get(reverse('blood_app:request_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Patient Rahim")

        res_status = self.client.get(reverse('blood_app:request_list'), {'status': 'Fulfilled'})
        self.assertEqual(len(res_status.context['page_obj']), 0)

    def test_blood_request_detail_view(self):
        response = self.client.get(reverse('blood_app:request_detail', kwargs={'pk': self.request1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Patient Rahim")

    def test_blood_request_create_authenticated(self):
        self.client.login(username='user2', password='password123')
        res = self.client.post(reverse('blood_app:request_create'), {
            'patient_name': 'New Patient',
            'blood_group': 'AB+',
            'hospital_name': 'Dhaka Medical',
            'location': 'Dhaka',
            'required_date': date.today() + timedelta(days=1),
            'bags_required': 1,
            'contact_number': '01911223344',
            'urgency': 'Critical',
            'reason': 'Emergency platelet transfusion',
        })
        self.assertEqual(res.status_code, 302)
        new_req = BloodRequest.objects.filter(patient_name='New Patient').first()
        self.assertIsNotNone(new_req)
        self.assertEqual(new_req.requester, self.user2)

    def test_blood_request_edit_permissions(self):
        # User2 tries to edit User1's request -> Should raise 403 PermissionDenied
        self.client.login(username='user2', password='password123')
        res = self.client.get(reverse('blood_app:request_edit', kwargs={'pk': self.request1.pk}))
        self.assertEqual(res.status_code, 403)

        # User1 (Owner) can edit
        self.client.login(username='user1', password='password123')
        res_owner = self.client.get(reverse('blood_app:request_edit', kwargs={'pk': self.request1.pk}))
        self.assertEqual(res_owner.status_code, 200)

    def test_blood_request_delete_permissions(self):
        # User2 tries to delete User1's request -> 403
        self.client.login(username='user2', password='password123')
        res = self.client.post(reverse('blood_app:request_delete', kwargs={'pk': self.request1.pk}))
        self.assertEqual(res.status_code, 403)

        # User1 deletes own request
        self.client.login(username='user1', password='password123')
        res_delete = self.client.post(reverse('blood_app:request_delete', kwargs={'pk': self.request1.pk}))
        self.assertEqual(res_delete.status_code, 302)
        self.assertFalse(BloodRequest.objects.filter(pk=self.request1.pk).exists())

    def test_user_authentication_flow(self):
        # Register new user
        res_reg = self.client.post(reverse('blood_app:register'), {
            'username': 'fresh_user',
            'first_name': 'Fresh',
            'last_name': 'User',
            'email': 'fresh@example.com',
            'phone': '01799887766',
            'blood_group': 'O-',
            'location': 'Feni',
            'password1': 'FreshPass123!',
            'password2': 'FreshPass123!',
            'register_as_donor': True,
        })
        self.assertEqual(res_reg.status_code, 302)
        self.assertTrue(User.objects.filter(username='fresh_user').exists())
        self.assertTrue(DonorProfile.objects.filter(user__username='fresh_user').exists())

        # Logout
        res_logout = self.client.get(reverse('blood_app:logout'))
        self.assertEqual(res_logout.status_code, 302)

        # Login with email
        res_login = self.client.post(reverse('blood_app:login'), {
            'email': 'fresh@example.com',
            'password': 'FreshPass123!',
        })
        self.assertEqual(res_login.status_code, 302)

    def test_admin_login_with_email(self):
        admin = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@bloodlink.com',
            password='adminpassword123'
        )
        res_admin = self.client.post(reverse('admin:login'), {
            'username': 'superadmin@bloodlink.com',
            'password': 'adminpassword123',
        })
        # Admin login redirects to /admin/ upon success
        self.assertEqual(res_admin.status_code, 302)

