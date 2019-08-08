from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    GENDER_CHOICES = [('M', "Male"), ('F', "Female"), ('O', "Other")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    bitsId = models.CharField(max_length=16)
    hostelId = models.CharField(max_length=4, null=True)
    roomNo = models.IntegerField(null = True)
    gender = models.CharField(choices=GENDER_CHOICES, null=True, max_length=2)
    dateOfBirth = models.DateField(null = True)
    address = models.CharField(max_length = 255, null = True)
    profilePic = models.ImageField(upload_to='profilePic',  blank=True)
    firstLogin = models.BooleanField(default=True)
    raf = models.BooleanField(default=False)
    swim = models.CharField(max_length=3, default='F')
    health = models.CharField(max_length=7, default='F')

    def __str__(self):
        return self.user.username

class CertificateRequest(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    certId = models.AutoField(primary_key=True)
    certType = models.CharField(max_length=4)
    isPrepared = models.BooleanField(default=False)
    isDelivered = models.BooleanField(default=False)
    isRejected = models.BooleanField(default=False)
    appDate = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.certId

class Vendor(models.Model):
    vendorId = models.AutoField(primary_key=True)
    vendorName = models.CharField(max_length=20)

    def __str__(self):
        return self.vendorName

class Dues(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    vendorId = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    amt = models.IntegerField(default=0)
    date = models.DateField()

    def __str__(self):
        return self.userId.username + " y" + str(self.date.year) + " m" + str(self.date.month) + " v" + self.vendorId.vendorName
