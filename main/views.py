from django.shortcuts import render
from main import forms
import smtplib
# Create your views here.

def index(request):
    return render(request, "main/index.html")

def complaints(request):
    form = forms.complaint()

    if request.method == "POST":
        form = forms.complaint(request.POST)

        if form.is_valid():
            s = smtplib.SMTP("smtp.gmail.com", 587)
            s.starttls()

            s.login("amoonshapedpool1999@gmail.com", "HR8938Cephei")
            message = "The following Anti Ragging complaint was filed anonymously.\n\n\"" + form.cleaned_data['complaint'] + "\"\n\nPlease deal with it at the earliest.\n\nAdmin,\nSWD, BITS Pilani\n"
            s.sendmail("amoonshapedpool1999@gmail.com", "guntaas.singh.1999@gmail.com", message)

            s.quit()
    return render(request, "main/complaints.html", {'form': form})

def contactus(request):
    return render(request, "main/contactus.html")
