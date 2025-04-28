from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import razorpay
from django.conf import settings

# Create your views here.
class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_instance = serializer.save()
            # Here you can integrate with real SMS API to send OTP
            return Response({
                "message": "OTP sent successfully",
                "otp": otp_instance.code  # ⚡ In real life, don't send OTP in response! (only for testing now)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "OTP verified successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DonationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            donation = serializer.save(user=request.user)

            # Simulate Payment (in real project, call payment gateway here)
            donation.payment_id = f"PAY-{donation.id}"  # fake payment ID
            donation.status = 'success'  # assume success for now
            donation.save()

            return Response({
                "message": "Donation successful",
                "donation_id": donation.id,
                "payment_id": donation.payment_id,
                "amount": str(donation.amount),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        donations = Donation.objects.filter(user=request.user).order_by('-created_at')
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MonthlyDonationSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            return Response(
                {"error": "Please provide both 'month' and 'year' as query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        donations = Donation.objects.filter(
            user=request.user,
            created_at__year=year,
            created_at__month=month
        ).order_by('-created_at')

        total_amount = donations.aggregate(total=models.Sum('amount'))['total'] or 0

        serializer = DonationSerializer(donations, many=True)

        return Response({
            "month": month,
            "year": year,
            "total_donation_amount": str(total_amount),
            "donations": serializer.data
        }, status=status.HTTP_200_OK

####For razorpay gateway payment(Here i don't get actual id because signup verification takes some time for it so here i add only code and replace the id)
class CreateOrderAPIView(APIView):
    def post(self, request):
        amount = request.data.get('amount')  # Amount in Rupees
        if not amount:
            return Response({"error": "Amount is required"}, status=400)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        data = {
            "amount": int(amount) * 100,  # Razorpay needs paise
            "currency": "INR",
            "payment_capture": 1
        }
        order = client.order.create(data=data)

        return Response({
            "order_id": order['id'],
            "amount": amount,
            "currency": "INR",
            "razorpay_key_id": settings.RAZORPAY_KEY_ID
        })
