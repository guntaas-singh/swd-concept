from django import forms
from django.contrib.auth.models import User
from userDash.models import UserProfile, CertificateRequest, Vendor, Dues

GENDER_CHOICES = [('M', "Male"), ('F', "Female"), ('O', "Other")]
CERT_CHOICES = [('A', 'Alphabet')]

class LoginForm(forms.ModelForm):

    class Meta():
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'})
        }
        labels = {
            'username' : '',
            'password' : '',
        }

class PassGenForm(forms.Form):
    bitsId = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'201xxxxx####P'}))

class ProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        exclude = ['user', 'bitsId', 'firstLogin', ]
        widgets = {
            'hostelId':forms.TextInput(attrs={'class':'form-control'}),
            'roomNo':forms.NumberInput(attrs={'class':'form-control'}),
            'gender':forms.Select(choices = GENDER_CHOICES, attrs={'class':'form-control'}),
            'dateOfBirth':forms.DateInput(),
            'address':forms.Textarea(),
            'profilePic':forms.ClearableFileInput(attrs={'class':'form-control-file'}),
        }
        labels = {
            'hostelId': "Hostel",
            'roomNo': "Room",
            'gender': "Gender",
            'dateOfBirth': "Date of birth",
            'address': "Address",
            'profilePic': "Profile Photo",

        }

class CertForm(forms.ModelForm):
    class Meta():
        model = CertificateRequest
        fields = ("certType", )
        widgets = {
            'certType':forms.Select(choices = CERT_CHOICES, attrs={'class':'form-control','placeholder':"Select Certificate Type"})
        }
        labels = {
            'certType':''
        }

class VendorForm(forms.ModelForm):
    class Meta():
        model = Vendor
        fields = ('vendorName', )
        labels = {
            'vendorName':''
        }
        widgets = {
            'vendorName': forms.TextInput(attrs={'class':'form-control'}),

        }

class DuesForm(forms.ModelForm):
    userId = forms.ModelChoiceField(label="Username", queryset=User.objects.all(), to_field_name="username", widget=forms.Select(attrs={'class':'form-control'}))
    vendorId = forms.ModelChoiceField(label="Vendor Name", queryset=Vendor.objects.all(), to_field_name="vendorName", widget=forms.Select(attrs={'class':'form-control'}))
    class Meta():
        model = Dues
        fields = ('userId', 'vendorId', 'date', 'amt',  )
        labels = {
            'amt':"Amount",
            'date':"Date"
        }
        widgets = {
            'amt':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Negative value means the student shall pay to clear'}),
            'date':forms.DateInput(attrs={'class':'form-control', 'placeholder':'DD-MM-YYYY'}),
        }
