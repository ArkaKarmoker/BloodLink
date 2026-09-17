import re
from datetime import date

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

# Compatibility Maps
# Key: Donor blood group -> Value: List of recipient blood groups donor CAN donate to
DONATE_COMPATIBILITY = {
    'O-': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],  # Universal Donor
    'O+': ['O+', 'A+', 'B+', 'AB+'],
    'A-': ['A-', 'A+', 'AB-', 'AB+'],
    'A+': ['A+', 'AB+'],
    'B-': ['B-', 'B+', 'AB-', 'AB+'],
    'B+': ['B+', 'AB+'],
    'AB-': ['AB-', 'AB+'],
    'AB+': ['AB+'],
}

# Key: Recipient blood group -> Value: List of donor blood groups recipient CAN receive from
RECEIVE_COMPATIBILITY = {
    'O-': ['O-'],
    'O+': ['O-', 'O+'],
    'A-': ['O-', 'A-'],
    'A+': ['O-', 'O+', 'A-', 'A+'],
    'B-': ['O-', 'B-'],
    'B+': ['O-', 'O+', 'B-', 'B+'],
    'AB-': ['O-', 'A-', 'B-', 'AB-'],
    'AB+': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],  # Universal Recipient
}

PHONE_REGEX = re.compile(r'^(\+?880|0)?1[3-9]\d{8}$')

def validate_phone_number(phone: str) -> bool:
    """Validates Bangladesh and standard phone formats."""
    cleaned = re.sub(r'[\s\-()]', '', phone)
    if PHONE_REGEX.match(cleaned):
        return True
    # Fallback to international general length check: 10 to 15 digits
    digits = re.sub(r'\D', '', phone)
    return 10 <= len(digits) <= 15

def get_donor_eligibility(last_donation_date: date | None) -> dict:
    """
    Returns eligibility info based on last donation date (standard 90-day cooldown).
    """
    if not last_donation_date:
        return {
            'is_eligible': True,
            'days_since': None,
            'days_remaining': 0,
            'status_text': 'Eligible to Donate (No prior donation on record)',
        }
    
    today = date.today()
    days_since = (today - last_donation_date).days
    cooldown_days = 90

    if days_since < 0:
        return {
            'is_eligible': False,
            'days_since': 0,
            'days_remaining': cooldown_days,
            'status_text': 'Invalid future date recorded',
        }

    if days_since >= cooldown_days:
        return {
            'is_eligible': True,
            'days_since': days_since,
            'days_remaining': 0,
            'status_text': f'Eligible to Donate ({days_since} days since last donation)',
        }
    else:
        days_remaining = cooldown_days - days_since
        return {
            'is_eligible': False,
            'days_since': days_since,
            'days_remaining': days_remaining,
            'status_text': f'Cooldown period ({days_remaining} days remaining)',
        }
