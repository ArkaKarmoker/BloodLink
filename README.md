# BloodLink — Blood Donate & Request System

[![Django](https://img.shields.io/badge/Django-6.1.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-22%20Passed-10B981?style=for-the-badge&logo=pytest&logoColor=white)](#automated-testing)

> **"Find a donor. Save a life."**  
> BloodLink is a comprehensive, production-grade Django web application connecting volunteer blood donors with patients and healthcare facilities in urgent need across Bangladesh.

---

## 🌟 Key Features

### 1. User Authentication & Profile
- **Account Registration & Login**: Multi-step user onboarding with phone validation and optional direct donor registration.
- **Account Settings**: Update personal details, contact info, and profile credentials.
- **User Dashboard**: Centralized hub showcasing donation stats, quick availability toggles, and user-posted blood requests.

### 2. Donor Profile (Full CRUD)
- **Create Profile**: Logged-in users can volunteer as donors with blood group, city/location, contact phone, last donation date, bio, and profile photo.
- **Read & Directory**: Public searchable directory with responsive donor cards.
- **Update Profile**: Owner-exclusive profile editing with phone and date validation.
- **Delete Profile**: Safe removal with confirmation modal.
- **Availability Toggle**: One-click quick toggle (`Available` / `Unavailable`).
- **Donation Cooldown & Eligibility**: Dynamic calculation of 90-day cooldown period and real-time eligibility status.

### 3. Blood Requests (Full CRUD)
- **Create Request**: Submit urgent blood requests with patient name, required blood group, bags needed, hospital name & location, required date, and reason.
- **Read & Feed**: Browse all active requests with urgency badges (`Critical`, `Urgent`, `Normal`).
- **Detail View**: Full patient and hospital breakdown, direct phone call triggers, and **intelligent compatible donor matching**.
- **Update & Status Management**: Requesters can edit request details or transition status between `Pending`, `Fulfilled`, and `Cancelled`.
- **Delete Request**: Requesters can remove obsolete requests with confirmation.
- **My Requests Page**: Filterable table tracking all requests initiated by the user.

### 4. Search & Multi-Parameter Filtering
- Filter **Donors** by Blood Group, City/Location (`icontains`), and Availability status.
- Filter **Blood Requests** by Blood Group, Hospital/City, Status, and Urgency.
- Pagination across all listings for smooth performance.

### 5. Blood Group Compatibility Guide
- Educational and emergency guide displaying exact compatible donor and recipient groups for A+, A-, B+, B-, AB+, AB-, O+, and O-.
- Automatic discovery of compatible donors on every blood request detail page.

### 6. Modern & Mobile-Responsive UI
- Bespoke modern design system built with clean Vanilla CSS (no framework bloat).
- Rich color palette: Deep Crimson (`#E11D48`), Slate Navy (`#0F172A`), and Emerald Green (`#10B981`).
- Interactive mobile hamburger navigation drawer.
- Floating dismissible toast alerts integrated with Django Messages framework.

---

## 📁 Project Architecture

```
BloodLink/
├── core/                       # Django project configuration
│   ├── __init__.py
│   ├── settings.py             # Configured apps, static, media, auth redirects
│   ├── urls.py                 # Root URL router
│   ├── wsgi.py
│   └── asgi.py
├── blood_app/                  # Main application
│   ├── models.py               # DonorProfile, BloodRequest, BloodDonationHistory
│   ├── forms.py                # Validation-backed forms
│   ├── views.py                # CRUD views, auth, filters, dashboard
│   ├── urls.py                 # App URL patterns
│   ├── utils.py                # Compatibility matrices & phone validators
│   ├── admin.py                # Customized Django admin
│   ├── management/commands/    # Data seeding scripts (seed_data.py)
│   └── tests/                  # 22 automated tests
│       ├── test_models.py
│       ├── test_forms.py
│       └── test_views.py
├── templates/
│   ├── base.html               # Base layout, fonts, toasts, semantic HTML
│   ├── navbar.html             # Responsive navbar with drawer
│   ├── footer.html             # Footer with emergency hotline (999)
│   └── blood_app/              # 14 distinct feature templates
├── static/
│   ├── css/main.css            # Complete design system & responsive styling
│   └── js/main.js              # Mobile menu, toasts, confirmations
├── requirements.txt            # Top-level dependencies with pinned versions
├── manage.py
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.12+ installed on your system.

### 2. Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/ArkaKarmoker/BloodLink.git
cd BloodLink

# Create virtual environment named venv
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1
# (Or on Command Prompt):
# .\venv\Scripts\activate.bat
# (Or on Linux/macOS):
# source venv/bin/activate
```

### 3. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 4. Run Migrations & Seed Sample Data
```bash
# Apply database migrations
python manage.py migrate

# Seed sample donors and emergency blood requests
python manage.py seed_data
```

### 5. Start the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🧪 Automated Testing

BloodLink includes a comprehensive test suite covering models, form validations, view permissions, CRUD security, and search filters.

Run tests using Django's test runner:
```bash
python manage.py test blood_app
```

**Result:**
```
Ran 22 tests in ~13s
OK (All 22 passed)
```

---

## 🔒 Security & Permissions

- **Authorization Guards**: Users can only edit or delete records they personally created. Non-owners attempting modifications receive an HTTP `403 Forbidden` (`PermissionDenied`).
- **Input Sanitization**: Phone numbers are validated against standard formats; negative bag counts and past dates are strictly rejected.
- **CSRF Protection**: All forms include Django's `{% csrf_token %}` tokens.
- **Passwords**: Secure hashed storage using Django's PBKDF2 algorithm.

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
