from django.contrib import admin

# Register your models here.
from .models import *

# Register your model
admin.site.register(User)
admin.site.register(OTP)
admin.site.register(Donation)
