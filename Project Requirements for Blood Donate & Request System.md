# Final Django Assignment

## Project Name
**Blood Donate & Request System**

## Project Overview
The **Blood Donate & Request System** is a Django-based web application where users can register as blood donors, create blood requests, and find suitable donors based on blood group and location.

The main goal of this project is to build a practical CRUD-based Django application that solves a real-world problem while applying the concepts learned throughout the course.

Students are expected to use:
* Django Models
* Views
* Templates
* Forms
* CRUD Operations
* Django ORM
* User Authentication
* Template Inheritance
* Basic Validation
* Search and Filtering

---

## 1. Main Features

### A. User Registration & Login
Users should be able to:
* Create an account
* Login
* Logout
* View their profile
* Update their profile

Each user can provide information such as:
* Full Name
* Email
* Phone Number
* Blood Group
* Location
* Date of Birth or Age
* Profile Picture (Optional)

Django's built-in authentication system can be used.

---

## 2. Donor Profile
A logged-in user can create/update their donor information.

**Donor Information**
* Name
* Blood Group
* Phone Number
* Location
* Last Donation Date
* Availability Status
* Short Description

**Availability Status**
For example:
* Available
* Not Available

Users should be able to update their availability whenever necessary.

---

## 3. Blood Request
A user can create a blood request when blood is needed.

**Blood Request Fields**
* Patient Name
* Blood Group Required
* Hospital Name
* Hospital Location
* Required Date
* Number of Bags
* Contact Number
* Reason/Description
* Request Status

**Request Status**
For example:
* Pending
* Fulfilled
* Cancelled

Users should be able to:
* Create a request
* View their requests
* Edit their requests
* Delete their requests
* Update request status

---

## 4. Donor Search
The system should provide a page where users can search for suitable donors.

Users should be able to filter donors by:
* Blood Group
* Location
* Availability

Example:
A user searches:
**Blood Group:** O+
**Location:** Feni
**Availability:** Available

The system should display matching donors.

---

## 5. Blood Request Listing
Create a page where users can see active blood requests.

Each request should display important information such as:
* Patient Name
* Blood Group
* Hospital
* Location
* Required Date
* Number of Bags
* Contact Information
* Request Status

Users should be able to filter requests by:
* Blood Group
* Location
* Status

---

## 6. Request Details Page
When a user clicks on a blood request, they should be taken to a details page.

The page should display complete information about the request.

Example:

**Patient:** Rahim Ahmed  
**Blood Group:** A+  
**Hospital:** XYZ Hospital  
**Location:** Feni  
**Required Date:** 20 September 2026  
**Bags Required:** 2  
**Contact:** 01XXXXXXXXX  
**Status:** Pending

---

## 7. Donor Details Page
Users should also be able to view a donor's profile.

The donor details page can show:
* Name
* Blood Group
* Location
* Last Donation Date
* Availability
* Contact Number
* Description

---

## 8. CRUD Requirements
Students must implement CRUD operations for at least the following:

**Blood Request**
* Create
* Read
* Update
* Delete

**Donor Profile**
* Create
* Read
* Update
* Delete

Students should properly restrict users so that they can modify/delete **their own records**.

---

## 9. Suggested Database Models
Students are free to design their own database structure.

However, a possible structure could be:

**User**
Use Django's built-in User model.

**DonorProfile**
Possible fields:
* `user`
* `blood_group`
* `phone`
* `location`
* `last_donation_date`
* `availability`
* `description`

**BloodRequest**
Possible fields:
* `requester`
* `patient_name`
* `blood_group`
* `hospital_name`
* `location`
* `required_date`
* `bags_required`
* `contact_number`
* `description`
* `status`
* `created_at`

Students may add additional fields if necessary.

---

## 10. Home Page
The home page should provide a clear introduction to the platform.

It may contain:

**Welcome Section**  
**Blood Donate & Request**  
"Find a donor. Save a life."

**Quick Actions**
* Find Blood Donor
* Request Blood
* Become a Donor
* View Blood Requests

Students are encouraged to create a clean and user-friendly interface.

---

## 11. Navigation Bar
The website should have a navigation bar containing relevant links.

Example:
* Home
* Find Donors
* Blood Requests
* Create Request
* My Requests
* My Profile
* Login / Logout

Students can modify the navigation based on their implementation.

---

## 12. Form Validation
Students should implement basic validation.

Examples:
* Required fields cannot be empty.
* Phone number should follow a reasonable format.
* Number of bags should be a positive number.
* Required date should be valid.
* Blood group should be selected from predefined choices.

---

## 13. Django Requirements
The project must be developed using **Django**.

Students should demonstrate proper use of:
* Models
* Views
* Templates
* Forms
* URL Routing
* Django ORM
* CRUD
* Authentication
* Template Inheritance
* Static Files
* Media Files (if profile pictures are implemented)

---

## 14. Bonus Features
The following features are **optional** and can be implemented for additional quality:

* Donor search by multiple filters
* Pagination
* Profile picture
* Blood group compatibility information
* Success/error messages using Django Messages
* Email notification
* Donor request/response system
* Admin dashboard customization
* Responsive design
* Bootstrap/Tailwind CSS
* AJAX-based search
* Blood request priority
* Dashboard showing statistics

Students do **not** need to implement all bonus features.

---

## 15. Suggested Pages
The project should contain appropriate pages such as:

1. Home Page
2. Registration Page
3. Login Page
4. User Profile
5. Donor List
6. Donor Details
7. Create Donor Profile
8. Edit Donor Profile
9. Blood Request List
10. Blood Request Details
11. Create Blood Request
12. Edit Blood Request
13. My Requests
14. About/Contact Page (Optional)

Students may add or remove pages depending on their implementation.

---

## 16. Submission Guidelines
Students must submit the following:

### 1. GitHub Repository — REQUIRED
Create a GitHub repository containing the complete project.

The repository must include:
* Complete Django source code
* `requirements.txt`
* Proper project structure
* Project description

**GitHub Repository Link is mandatory.**

### 2. Project Video — OPTIONAL
Students may include a short video demonstrating the project.

The video can show:
* Registration/Login
* Creating donor profile
* Searching donors
* Creating blood request
* Editing/deleting records
* Filtering/searching
* Overall website functionality

### 3. Screenshots — OPTIONAL
Students may include screenshots of important pages in the GitHub repository.

Suggested screenshots:
* Home Page
* Login/Register
* Donor List
* Donor Details
* Blood Request List
* Blood Request Details
* User Dashboard/Profile
