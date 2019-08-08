from django.contrib import admin
from userDash.models import UserProfile, CertificateRequest, Vendor, Dues

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CertificateRequest)
admin.site.register(Vendor)
admin.site.register(Dues)
