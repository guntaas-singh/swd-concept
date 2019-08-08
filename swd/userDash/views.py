from django.shortcuts import render
from userDash import forms
from userDash.models import UserProfile, CertificateRequest, Vendor, Dues
from django.contrib.auth.models import User
import secrets  # For password generation
import string   #
import smtplib      # For email management
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict

# Create your views here.

def user_login(request):
    LoginForm = forms.LoginForm()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                if user.is_staff:
                    return HttpResponseRedirect(reverse('staff'))
                if user.userprofile.firstLogin:
                    return HttpResponseRedirect(reverse('editprofile'))
                else:
                    return HttpResponseRedirect(reverse('dashboard'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Login failed")
            print(f"Username: {username}\nPassword: {password}")
            return HttpResponse("Invalid credentials supplied.")
    else:
        return render(request, "userDash/login.html", {"login_form": LoginForm})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def dashboard(request):
    return render(request, "userDash/dashboard.html")

@login_required
def editprofile(request):

    if request.method == "POST":
        ProfileForm = forms.ProfileForm(request.POST, request.FILES)

        if ProfileForm.is_valid():
            thisuserprofile = request.user.userprofile

            thisuserprofile.hostelId = ProfileForm.cleaned_data['hostelId']
            thisuserprofile.roomNo = ProfileForm.cleaned_data['roomNo']
            thisuserprofile.gender = ProfileForm.cleaned_data['gender']
            thisuserprofile.dateOfBirth = ProfileForm.cleaned_data['dateOfBirth']
            thisuserprofile.address = ProfileForm.cleaned_data['address']

            if 'profilePic' in request.FILES:
                imagefile = request.FILES['profilePic']
                imagefile.name = str(request.user.username)+'.jpg'
                thisuserprofile.profilePic = imagefile
            thisuserprofile.firstLogin = False
            thisuserprofile.save()
        else:
            print(ProfileForm.errors)
            return HttpResponse("ERROR. Invalid form.")
    else:
        if request.user.userprofile.firstLogin:
            ProfileForm = forms.ProfileForm()
        else:
            userprofile = request.user.userprofile
            profiledict = model_to_dict(userprofile)
            ProfileForm = forms.ProfileForm(profiledict)

    return render(request, "userDash/editprofile.html", {'form':ProfileForm})

@login_required
def clubs(request):
    thisuserprofile = request.user.userprofile
    if request.method == "POST":
        if 'raf' in request.POST:
            thisuserprofile.raf = True
            thisuserprofile.save()
        elif 'swim-slot' in request.POST:
            thisuserprofile.swim = request.POST['swim-slot'][7:9]
            thisuserprofile.save()
        elif 'health-slot' in request.POST:
            thisuserprofile.health = request.POST['health-slot'][7:13]
            thisuserprofile.save()

    rafsign = thisuserprofile.raf
    swimsign = False if (thisuserprofile.swim == 'F') else True
    healthsign = False if (thisuserprofile.health == 'F') else True
    return render(request, "userDash/clubs.html", {'rafsign':rafsign, 'swimsign':swimsign, 'healthsign':healthsign, 'swimslot':thisuserprofile.swim, 'healthslot':thisuserprofile.health})

@login_required
def certificates(request):
    CertForm = forms.CertForm()
    list1 = CertificateRequest.objects.filter(userId = request.user)
    if request.method == "POST":
        CertForm = forms.CertForm(request.POST)

        if CertForm.is_valid():
            CertRequest = CertificateRequest.objects.create(certType=CertForm.cleaned_data['certType'], userId = request.user)
            CertRequest.save()

    return render(request, "userDash/certificates.html", {'form':CertForm, "list": list1})

@login_required
def myDues(request):
    list1 = Dues.objects.filter(userId=request.user).order_by('date')
    duesDict = {}
    month_list = []
    for entry in list1:
        if not str(entry.date.month)+"/"+str(entry.date.year) in month_list:
            month_list.append(str(entry.date.month)+"/"+str(entry.date.year))
        if not entry.vendorId in duesDict:
            duesDict[entry.vendorId] = []
    for vendor in duesDict:
        for month in month_list:
            try:
                dues = Dues.objects.get(vendorId__vendorName = vendor, date__month=month[:-5])
                duesDict[vendor].append(dues.amt)
            except Dues.DoesNotExist:
                duesDict[vendor].append(0)
    print(duesDict)
    return render(request, "userDash/myDues.html", {'dict':duesDict, 'months':month_list})

def passgen(request):
    PassGenForm = forms.PassGenForm()

    submitted = False

    if request.method == "POST":
        PassGenForm = forms.PassGenForm(request.POST)

        if PassGenForm.is_valid():
            bitsId = PassGenForm.cleaned_data['bitsId']

            thisUserProfile, created = UserProfile.objects.get_or_create(bitsId=bitsId)
            if created == True:

                # Convert ID to username
                username = "f" + bitsId[:4] + bitsId[8:12]


                # Generate Password
                alphabet = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(alphabet) for i in range(8))

                # Create new User
                thisUser = User.objects.create(username=username, password=password)
                thisUser.set_password(thisUser.password)
                thisUser.save()

                # Link to new thisUserProfile
                thisUserProfile.user = thisUser
                thisUserProfile.firstLogin = True
                thisUserProfile.save()
            else:
                # Generate Password
                alphabet = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(alphabet) for i in range(8))
                thisUser = thisUserProfile.user
                thisUser.password = password
                thisUser.set_password(thisUser.password)
                thisUser.save()

            # Email the new password
            username = "f" + bitsId[:4] + bitsId[8:12]
            email = username + "@pilani.bits-pilani.ac.in"
            s = smtplib.SMTP("smtp.gmail.com", 587)
            s.starttls()

            s.login("amoonshapedpool1999@gmail.com", "HR8938Cephei")
            message = "Dear " + username + ",\n\nThe new password for your SWD account is '" + password + "'.\n\nRegards,\nSWD Admin\n"
            s.sendmail("amoonshapedpool1999@gmail.com", email, message)

            s.quit()
            sumbitted = True

    return render(request, "userDash/passgen.html", {"pass_gen_form": PassGenForm, "submitted":submitted})

@login_required
def staff(request):
    if not request.user.is_staff:
        logout(request)
        return HttpResponseRedirect(reverse('login'))
    return render(request, "userDash/staff.html")

@login_required
def staffClubs(request):
    return render(request, "userDash/staff_clubs.html")

@login_required
def rafList(request):
    list1 = UserProfile.objects.filter(raf=True)
    return render(request, "userDash/rafList.html", {'list':list1})

@login_required
def swimList(request, batch):
    list1 = UserProfile.objects.filter(swim=batch)
    batches = ['A1', 'A2', 'A4', 'A5', 'B1', 'B2', 'B4', 'B5']
    print(list1)
    return render(request, "userDash/swimlist.html", {'batches':batches, 'chosenBatch':batch, 'list':list1})

@login_required
def healthList(request):
    list1 = UserProfile.objects.exclude(health = 'F').order_by('health', 'bitsId')
    return render(request, "userDash/healthList.html", {'list':list1})

@login_required
def staffCertificates(request):
    if request.method == "POST":
        cert = CertificateRequest.objects.get(certId=request.POST['certId'])
        action = request.POST['control']
        if action == "Prepared":
            cert.isPrepared = True
        elif action == "Delivered":
            cert.isDelivered = True
        elif action == "Rejected":
            cert.isRejected = True
        cert.save()
    list1 = CertificateRequest.objects.all()
    return render(request, "userDash/staff_certificates.html", {'list':list1})

@login_required
def vendors(request):
    vendorForm = forms.VendorForm()
    list1 = Vendor.objects.all()
    if request.method == "POST":
        newVendor = Vendor.objects.create(vendorName = request.POST['vendorName'])
        newVendor.save()
    return render(request, 'userDash/vendors.html', {"form":vendorForm, 'list':list1})

@login_required
def staffDues(request):
    duesForm = forms.DuesForm()
    if request.method == "POST":
        duesForm = forms.DuesForm(request.POST)
        if duesForm.is_valid():
            dues = duesForm.save()
    return render(request, 'userDash/staff_dues.html', {'form':duesForm})
