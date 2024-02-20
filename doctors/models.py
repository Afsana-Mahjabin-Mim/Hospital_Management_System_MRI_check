from django.db import models
from datetime import date
from users.models import *
import uuid

# Create your models here.


class DoctorDepartment(models.Model):
    department_name = models.CharField(max_length=255)
    department_shortname = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Department: {self.department_name} (- {self.department_shortname})"



class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    profile_pic= models.ImageField(upload_to='media/profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40, null=True, blank=True)
    mobile = models.CharField(max_length=20,null=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    visit_price = models.IntegerField(null=True, blank=True)
    department = models.ForeignKey(DoctorDepartment, on_delete=models.CASCADE, related_name='doctors')
    status  =models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.full_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} ({})".format(self.user.full_name,self.department.department_name)



class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('W', 'Widowed'),
        ('D', 'Divorced'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('NA', 'Not Available'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_user")
    profile_pic = models.ImageField(upload_to='media/profile_pic/PatientProfilePic/',null=True,blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank =True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, default='NA')
    emergency_contact_number = models.CharField(max_length=15, blank=True, null=True)

    status=models.BooleanField(default=True)
    
    @property
    def get_name(self):
        return self.user.full_name
    
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return self.user.full_name



class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Canceled', 'Canceled'),
        ('Completed', 'Completed'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')

    department = models.ForeignKey(DoctorDepartment, on_delete=models.DO_NOTHING, related_name="doc_department", null=True, blank=True)
    visit_price = models.IntegerField(null=True, blank=True)
    appointment_date = models.DateField(blank=True, null=True)
    appointment_time = models.TimeField(blank=True, null=True)

    details = models.TextField(blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)

    allergies = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)

    status = models.BooleanField(default=True)
    confirmation = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Confirmed', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.patient.name} with {self.doctor.name} on {self.appointment_date}"




class TestType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    short_name = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    preparation_instructions = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return self.short_name



class MedicalTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_medical_tests')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_medical_tests')
    test_type = models.ForeignKey(TestType, on_delete=models.DO_NOTHING, related_name='medical_test_type')

    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    test_date = models.DateField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    qr_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.test_type} for {self.patient.name} QR {self.qr_code}"

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code = uuid.uuid4()
        super().save(*args, **kwargs)



class MedicalTestImage(models.Model):
    medical_test = models.ForeignKey(MedicalTest, on_delete=models.CASCADE, related_name='test_images')
    qr_code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Images for {self.medical_test.test_type} test on QR {self.qr_code}"


class Image(models.Model):
    medical_test_image = models.ForeignKey(MedicalTestImage, on_delete=models.CASCADE, related_name='medical_test_image')
    image = models.ImageField(upload_to='media/medical_tests_image/')

    def __str__(self):
        return f"Image {self.id} for {self.medical_test_image.qr_code}"
