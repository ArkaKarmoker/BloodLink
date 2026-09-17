from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta
from blood_app.models import DonorProfile, BloodRequest, BloodDonationHistory
from blood_app.utils import get_donor_eligibility, validate_phone_number


class ModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='testpassword123'
        )
        self.donor1 = DonorProfile.objects.create(
            user=self.user1,
            phone='01711223344',
            blood_group='O+',
            location='Feni',
            date_of_birth=date(1995, 5, 15),
            last_donation_date=date.today() - timedelta(days=100),
            is_available=True,
            description='Test donor profile bio'
        )

    def test_donor_profile_creation_and_str(self):
        self.assertEqual(str(self.donor1), "John Doe (O+) - Feni")
        self.assertEqual(self.donor1.display_name, "John Doe")
        self.assertTrue(self.donor1.is_available)
        self.assertGreater(self.donor1.age, 20)

    def test_donor_eligibility_calculator(self):
        # 100 days ago should be eligible (> 90 days cooldown)
        eligibility = self.donor1.eligibility
        self.assertTrue(eligibility['is_eligible'])
        self.assertEqual(eligibility['days_remaining'], 0)

        # Recent donation (20 days ago) should be in cooldown
        self.donor1.last_donation_date = date.today() - timedelta(days=20)
        self.donor1.save()
        eligibility_recent = self.donor1.eligibility
        self.assertFalse(eligibility_recent['is_eligible'])
        self.assertEqual(eligibility_recent['days_remaining'], 70)

        # None last donation should be eligible
        self.donor1.last_donation_date = None
        self.donor1.save()
        self.assertTrue(self.donor1.eligibility['is_eligible'])

    def test_donor_compatibility(self):
        # O+ can donate to O+, A+, B+, AB+
        self.assertIn('O+', self.donor1.can_donate_to)
        self.assertIn('AB+', self.donor1.can_donate_to)
        # O+ can receive from O+, O-
        self.assertEqual(self.donor1.can_receive_from, ['O-', 'O+'])

    def test_blood_request_creation_and_matching_donors(self):
        req = BloodRequest.objects.create(
            requester=self.user1,
            patient_name='Jane Smith',
            blood_group='A+',
            hospital_name='Feni Hospital',
            location='Feni',
            required_date=date.today() + timedelta(days=2),
            bags_required=2,
            contact_number='01811223344',
            urgency='Urgent',
            status='Pending',
            reason='Surgery required'
        )
        self.assertEqual(str(req), "Jane Smith - A+ (2 bags) at Feni Hospital")
        self.assertIn('O+', req.compatible_donor_groups)  # A+ can receive O+
        matching = req.get_matching_donors()
        self.assertIn(self.donor1, matching)

    def test_phone_validation_utility(self):
        self.assertTrue(validate_phone_number('01711223344'))
        self.assertTrue(validate_phone_number('+8801812345678'))
        self.assertFalse(validate_phone_number('12345'))
        self.assertFalse(validate_phone_number('abcdefghijk'))
