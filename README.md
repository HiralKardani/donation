Project Overview
This project is a Donation System built with Django REST Framework.
It allows users to:
- Authenticate using phone number and OTP
- online using a payment locally
- View their donation/payment history
- See monthly donation reports
- The project is containerized using Docker.

Features
-User Authentication with Phone and OTP
-Donation locally (Not apply the payment gateway because signup verification takes time)
-Payment History Management
-Monthly Donation Dashboard 
-Dockerized Deployment

Setup Instructions
1. Clone the Repository
-git clone <your-repo-link>

2. Set up Environment (Without Docker)
python -m venv myenv
- myenv\Scripts\activate   

3. Install Requirements
- pip install -r requirements.txt

5. Run Migrations
- python manage.py migrate
- 
5. Create a Superuser
-python manage.py createsuperuser

6. Run the Server
-python manage.py runserver

Notes
Database used: SQLite (default Django)
myenv/ (virtual environment) is not pushed to GitHub (ignored in .gitignore)
OTP sending is simulated in local development.
Razorpay gateway payment is implemented but i don't get the actual is because of account takes time so here i only add code. For check the working you need to replace your configuration for payment.

API endpoints:
Login with phone number (POST) - /api/login/
Verify OTP (POST) - api/verify-otp/
Make Donation (POST) - /api/donate/
View Payment History (GET) - /api/payment-history/


Time Spent
Time spent: 6-7 hours
