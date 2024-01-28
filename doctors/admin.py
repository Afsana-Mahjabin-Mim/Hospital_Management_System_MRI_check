from django.contrib import admin
from doctors.models import *


# Register your models here.


admin.site.register(DoctorDepartment)
admin.site.register(Doctor)
admin.site.register(Patient)

admin.site.register(Appointment)

admin.site.register(TestType)
admin.site.register(MedicalTest)
admin.site.register(MedicalTestImage)

admin.site.register(Image)
