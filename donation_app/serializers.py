from rest_framework import serializers
from .models import OTP, User, Donation

class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def create(self, validated_data):
        phone = validated_data['phone']
        otp = OTP.objects.create(phone=phone)
        return otp

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        phone = data.get('phone')
        code = data.get('code')

        try:
            otp_record = OTP.objects.filter(phone=phone, is_verified=False).latest('created_at')
        except OTP.DoesNotExist:
            raise serializers.ValidationError("OTP not found or already verified.")

        if otp_record.is_expired():
            raise serializers.ValidationError("OTP has expired. Please request a new one.")

        if otp_record.code != code:
            raise serializers.ValidationError("Incorrect OTP.")

        return data

    def create(self, validated_data):
        phone = validated_data.get('phone')

        # Mark OTP as verified
        otp_record = OTP.objects.filter(phone=phone, is_verified=False).latest('created_at')
        otp_record.is_verified = True
        otp_record.save()

        # Create or get user
        user, created = User.objects.get_or_create(phone=phone)

        return user

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'amount', 'payment_id', 'status', 'created_at']
        read_only_fields = ['id', 'payment_id', 'status', 'created_at']
