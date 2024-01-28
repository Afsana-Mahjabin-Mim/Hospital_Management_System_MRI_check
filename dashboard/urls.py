from django.urls import path 

from .views import *

app_name="dashboard"

urlpatterns=[
    path("",DashBoardView.as_view(),name="dashboard"),
    
    path('add_doctor/', AddDoctorView.as_view(), name='add_doctor'),
    path('doctor_list/', ManageDoctorListView.as_view(), name='doctor_list'),
    path('update_doctor/<int:pk>/', UpdateDoctorView.as_view(), name='update_doctor'),
    path('delete_doctor/<int:pk>/', DeleteDoctorView.as_view(), name='delete_doctor'),
    
    path('add_patient/', AddPatientView.as_view(), name='add_patient'),
    path('patient_list/', ManagePatientListView.as_view(), name='patient_list'),
    path('update_patient/<int:pk>/', UpdatePatientView.as_view(), name='update_patient'),
    path('delete_patient/<int:pk>/', DeletePatientView.as_view(), name='delete_patient'),
    
    path('appoinment/', AddAppointmentView.as_view(), name='appoinment'),
    path('appoinment_list/', ManageAppointmentListView.as_view(), name='appoinment_list'),
    path('get-doctors-by-department/<int:department_id>/', get_doctors_by_department, name='get_doctors_by_department'),
    path('get-doctor-visit-price/<int:doctor_id>/', GetDoctorVisitPriceView.as_view(), name='get_doctor_visit_price'),
    path('update_appointment/<int:pk>/', UpdateAppointmentView.as_view(), name='update_appointment'),
    path('delete_appointment/<int:pk>/', DeleteAppointmentView.as_view(), name='delete_appointment'),

    path('add_test_type/', AddTestTypeView.as_view(), name='add_test_type'),
    path('test_type_list/', TestTypeListView.as_view(), name='test_type_list'),
    path('update_test_type/<int:pk>/', UpdateTestTypeView.as_view(), name='update_test_type'),
    path('delete_test_type/<int:pk>/', DeleteTestTypeView.as_view(), name='delete_test_type'),
    
    path('add_medical_test/', AddMedicalTestView.as_view(), name='add_medical_test'),
    path('medical_test_list/', MedicalTestListView.as_view(), name='medical_test_list'),
    path('get-test-visit-price/<int:test_type_id>/', GetTestVisitPriceView.as_view(), name='get_test_visit_price'),
    path('medical_test/update/<int:pk>/', UpdateMedicalTestView.as_view(), name='update_medical_test'),
    path('delete_medical_test/<int:pk>/', DeleteMedicalTestView.as_view(), name='delete_medical_test'),
    
    
    path('add_test_image_report/', AddTestImageReportView.as_view(), name='add_test_image_report'),
    path('test_image_report_all/', MedicalTestImageListView.as_view(), name='test_image_report_all'),
    path('report_image/<int:pk>/', MedicalReportImageListView.as_view(), name='report_image'),

    path('api/test-image-report/', TestImageReportAPIView.as_view(), name='test_image_report_api')


]
