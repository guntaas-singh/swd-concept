from django.urls import path
from userDash import views

urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('passgen/', views.passgen, name="passgen"),
    path('editprofile/', views.editprofile, name="editprofile"),
    path("clubs/", views.clubs, name="clubs"),
    path('certificates/', views.certificates, name="certificates"),
    path('dues/', views.myDues, name="myDues"),
    path('logout/', views.user_logout, name="logout"),
    path('staff/', views.staff, name="staff"),
    path('staff/vendors', views.vendors, name="vendors"),
    path('staff/clubs/', views.staffClubs, name="staffClubs"),
    path('staff/clubs/raflist', views.rafList),
    path('staff/clubs/swimlist/<str:batch>', views.swimList),
    path('staff/clubs/healthlist', views.healthList),
    path('staff/certificates', views.staffCertificates, name="staffCertificates"),
    path('staff/dues', views.staffDues, name="staffDues"),


]
