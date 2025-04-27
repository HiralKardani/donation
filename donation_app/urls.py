from django.urls import path
from .views import *

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('donate/', DonationView.as_view(), name='donate'),
    path('payment-history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('monthly-summary/', MonthlyDonationSummaryView.as_view(), name='monthly-summary'),
]