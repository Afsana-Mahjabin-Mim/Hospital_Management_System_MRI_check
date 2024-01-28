from django.shortcuts import render
from django.views import View 
from django.contrib.sites.models import Site
from doctors.models import *
from django.shortcuts import render, redirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dashboard.serializers import *
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt



"""
        ------------ Dashboard View ------------
"""

class DashBoardView(View):
    def get(self,request):
        doctor_count = Doctor.objects.count()
        patient_count = Patient.objects.count()
        appointment_count = Appointment.objects.count()
        medical_test_count = MedicalTest.objects.count()
        current_site = Site.objects.get_current()
        
        context = {
            'doctor_count': doctor_count,
            'patient_count': patient_count,
            'appointment_count': appointment_count,
            'medical_test_count': medical_test_count,
        }
        return render(request, "dashboard/dashboard.html", context)


"""
        ------------ Doctor View ------------
"""

class AddDoctorView(View):
    def get(self,request):
        department_list = DoctorDepartment.objects.all()
        context ={
            "department_list":department_list
        }
        return render(request,"hospital/add_doctor.html",context)
    
    def post(self, request):

        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        user_type = request.POST.get('user_type')
        department_id = request.POST.get('department')
        dob = request.POST.get('dob')
        phone_number = request.POST.get('phone_number')
        visit_price = request.POST.get('visit_price')
        address = request.POST.get('address')
        profile_avatar = request.FILES.get('profile_avatar')
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')
        status = request.POST.get('status')

        # Create User instance
        user = User.objects.create(
            email=email,
            full_name=full_name,
            user_type=user_type,
            dob=dob,
            phone_number=phone_number,
            address=address,
            profile_avatar=profile_avatar,
            is_active=(status == 'true'),
        )

        # Create Doctor instance linked to the User
        doctor = Doctor.objects.create(
            user=user,
            name=full_name,
            profile_pic=profile_avatar,
            address=address,
            mobile=phone_number,
            visit_price=visit_price,
            specialization=specialization,
            experience=experience,
            department=DoctorDepartment.objects.get(id=department_id),
            status=(status == 'true'),
        )

        messages.success(request, 'Doctor added successfully!')
        return redirect('dashboard:doctor_list')



class ManageDoctorListView(View):
    def get(self,request):
        doctor_list = Doctor.objects.all()
        context ={
            "doctor_list":doctor_list
        }
        return render(request,"hospital/doctor_list.html",context)



class UpdateDoctorView(View):
    def get(self, request, pk):
        doctor = Doctor.objects.get(id=pk)
        department_list = DoctorDepartment.objects.all()

        context = {
            'doctor': doctor,
            'department_list': department_list,
        }
        return render(request, "hospital/update_doctor.html", context)

    def post(self, request, pk):
        doctor = Doctor.objects.get(id=pk)

        # Extract data from the POST request
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        user_type = request.POST.get('user_type')
        department_id = request.POST.get('department')
        dob = request.POST.get('dob')
        visit_price = request.POST.get('visit_price')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        profile_avatar = request.FILES.get('profile_avatar')
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')
        status = request.POST.get('status')
        delete_profile_avatar = request.POST.get('delete_profile_avatar')

        # Update Doctor and User models directly
        doctor.user.email = email
        doctor.user.full_name = full_name
        doctor.user.user_type = user_type
        doctor.user.dob = dob
        doctor.user.phone_number = phone_number
        doctor.user.address = address
        
        if delete_profile_avatar:
            doctor.user.profile_avatar.delete(save=True)
        elif profile_avatar:
            doctor.user.profile_avatar = profile_avatar

        doctor.user.is_active = (status == 'true')
        doctor.user.save()

        doctor.department = DoctorDepartment.objects.get(id=department_id)
        doctor.specialization = specialization
        doctor.mobile = phone_number
        doctor.visit_price = visit_price
        doctor.name = full_name

        if delete_profile_avatar:
            doctor.profile_pic = None
        elif profile_avatar:
            doctor.profile_pic = profile_avatar

        doctor.experience = experience
        doctor.address = address
        doctor.status = (status == 'true')
        doctor.save()

        messages.success(request, 'Doctor Updated successfully!')
        return redirect('dashboard:doctor_list')



class DeleteDoctorView(View):
    def get(self, request, pk):
        doctor = get_object_or_404(Doctor, id=pk)
        user = doctor.user

        doctor.delete()
        user.delete()

        messages.success(request, 'Doctor deleted successfully!')
        return redirect('dashboard:doctor_list')


"""
        ------------ Patient View ------------
"""

class AddPatientView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "hospital/add_patient.html")

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        user_type = request.POST.get('user_type')
        dob = request.POST.get('dob')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        profile_avatar = request.FILES.get('profile_avatar')
        gender = request.POST.get('gender')
        marital_status = request.POST.get('marital_status')
        blood_type = request.POST.get('blood_type')
        emergency_contact_number = request.POST.get('emergency_contact_number')
        status = request.POST.get('status')

        # Create a new user
        user = User.objects.create(
            email=email,
            full_name=full_name,
            dob=dob,
            phone_number=phone_number,
            address=address,
            profile_avatar=profile_avatar,
            user_type=user_type,
            is_active=(status == 'true'),
        )

        # Create a new patient
        patient = Patient.objects.create(
            user=user,
            profile_pic=profile_avatar,
            name=full_name,
            date_of_birth=dob,
            gender=gender,
            marital_status=marital_status,
            address=address,
            phone_number=phone_number,
            blood_type=blood_type,
            emergency_contact_number=emergency_contact_number,
            status=(status == 'true')
        )

        messages.success(request, 'Patient Added successfully!')
        return redirect('dashboard:patient_list')



class ManagePatientListView(View):
    def get(self,request):
        patient_list = Patient.objects.all()
        context ={
            "patient_list":patient_list
        }
        return render(request,"hospital/patient_list.html",context)



class UpdatePatientView(View):
    def get(self, request, pk, *args, **kwargs):
        patient = get_object_or_404(Patient, id=pk)
        return render(request, "hospital/update_patient.html", {'patient': patient})

    def post(self, request, pk, *args, **kwargs):
        patient = get_object_or_404(Patient, id=pk)

        # Update User model
        patient.user.email = request.POST.get('email')
        patient.user.full_name = request.POST.get('full_name')
        patient.user.user_type = request.POST.get('user_type')
        patient.user.dob = request.POST.get('dob')
        patient.user.phone_number = request.POST.get('phone_number')
        patient.user.address = request.POST.get('address')
        patient.user.is_active = (request.POST.get('status') == 'true')

        # Check if the user wants to delete the profile picture
        delete_profile_avatar = request.POST.get('delete_profile_avatar')
        if delete_profile_avatar == 'true':
            patient.user.profile_avatar.delete()  # Delete the existing profile avatar
            patient.user.profile_avatar = None

        # Check if the user wants to delete the profile picture
        delete_profile_pic = request.POST.get('delete_profile_avatar')
        if delete_profile_pic == 'true':
            patient.profile_pic.delete()  # Delete the existing profile picture
            patient.profile_pic = None

        # Update Patient model
        patient.name = request.POST.get('full_name')
        patient.date_of_birth = request.POST.get('dob')
        patient.phone_number = request.POST.get('phone_number')
        patient.address = request.POST.get('address')
        patient.gender = request.POST.get('gender')
        patient.marital_status = request.POST.get('marital_status')
        patient.blood_type = request.POST.get('blood_type')
        patient.emergency_contact_number = request.POST.get('emergency_contact_number')
        patient.status = request.POST.get('status') == 'true'

        # Check if a new profile avatar is provided
        new_profile_avatar = request.FILES.get('profile_avatar')
        if new_profile_avatar:
            if patient.user.profile_avatar:
                patient.user.profile_avatar.delete()
            patient.user.profile_avatar = new_profile_avatar

        # Check if a new profile picture is provided
        new_profile_pic = request.FILES.get('profile_avatar')
        if new_profile_pic:
            if patient.profile_pic:
                patient.profile_pic.delete()
            patient.profile_pic = new_profile_pic

        # Save changes to both models
        patient.user.save()
        patient.save()

        messages.success(request, 'Patient Updated successfully!')
        return redirect('dashboard:patient_list')




class DeletePatientView(View):
    def get(self, request, pk):
        patient = get_object_or_404(Patient, id=pk)
        user = patient.user

        patient.delete()
        user.delete()

        messages.success(request, 'Patient deleted successfully!')
        return redirect('dashboard:patient_list')


"""
        ----------- Appoinment ------------
"""

class AddAppointmentView(View):

    def get(self, request, *args, **kwargs):
        patient_list = Patient.objects.all()
        department_list = DoctorDepartment.objects.all()
        doctor_list = Doctor.objects.all()

        context = {
            'patient_list': patient_list,
            'department_list': department_list,
            'doctor_list': doctor_list,
        }
        return render(request, "hospital/appoinment.html", context)

    def post(self, request, *args, **kwargs):
        patient_id = request.POST.get('patient')
        department_id = request.POST.get('department')
        doctor_id = request.POST.get('doctor')

        patient = get_object_or_404(Patient, id=patient_id)
        department = get_object_or_404(DoctorDepartment, id=department_id)
        doctor = get_object_or_404(Doctor, id=doctor_id)

        visit_price = request.POST.get('visit_price')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        details = request.POST.get('details')
        age = request.POST.get('age')
        allergies = request.POST.get('allergies')
        medications = request.POST.get('medications')
        confirmation = request.POST.get('confirmation')

        appointment = Appointment(
            patient=patient,
            department=department,
            doctor=doctor,
            visit_price=visit_price,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            details=details,
            age=age,
            allergies=allergies,
            medications=medications,
            confirmation=confirmation
        )

        appointment.save()
        messages.success(request, 'Appointment added successfully!')
        return redirect('dashboard:appoinment_list')


def get_doctors_by_department(request, department_id):
    doctors = Doctor.objects.filter(department_id=department_id).values('id', 'name')
    return JsonResponse(list(doctors), safe=False)


class GetDoctorVisitPriceView(View):
    def get(self, request, doctor_id):
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            visit_price = doctor.visit_price
            return JsonResponse({'visit_price': visit_price})
        except Doctor.DoesNotExist:
            return JsonResponse({'error': 'Doctor not found'}, status=404)



class ManageAppointmentListView(View):
    def get(self,request):
        appointment_list = Appointment.objects.all()
        context ={
            "appointment_list":appointment_list
        }
        return render(request,"hospital/appoinment_list.html",context)



class UpdateAppointmentView(View):
    def get(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, id=pk)
        patient_list = Patient.objects.all()
        department_list = DoctorDepartment.objects.all()
        doctor_list = Doctor.objects.all()

        context = {
            'selected_appointment': appointment,
            'patient_list': patient_list,
            'department_list': department_list,
            'doctor_list': doctor_list,
        }
        return render(request, "hospital/update_appointment.html", context)

    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, id=pk)

        # Update appointment fields based on the data
        appointment.patient = Patient.objects.get(id=request.POST['patient'])
        appointment.doctor = Doctor.objects.get(id=request.POST['doctor'])
        appointment.department = DoctorDepartment.objects.get(id=request.POST['department'])
        appointment.visit_price = request.POST.get('visit_price', 0)
        appointment.appointment_date = request.POST.get('appointment_date')
        appointment.appointment_time = request.POST.get('appointment_time')
        appointment.details = request.POST.get('details')
        appointment.age = request.POST.get('age')
        appointment.allergies = request.POST.get('allergies')
        appointment.medications = request.POST.get('medications')
        appointment.confirmation = request.POST.get('confirmation')

        appointment.save()
        messages.success(request, 'Appointment Updated successfully!')
        return redirect('dashboard:appoinment_list')



class DeleteAppointmentView(View):
    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, id=pk)
        appointment.delete()
        messages.success(request, 'Appointment Deleted successfully!')
        return redirect('dashboard:appoinment_list')



"""
        ----------- Test Type ------------
"""

class AddTestTypeView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "hospital/add_test_type.html")

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        short_name = request.POST.get('short_name')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        preparation_instructions = request.POST.get('preparation_instructions')

        test_type = TestType(
            name=name,
            short_name=short_name,
            amount=amount,
            description=description,
            preparation_instructions=preparation_instructions,
        )

        test_type.save()
        messages.success(request, 'Test Type added successfully!')
        return redirect('dashboard:test_type_list')



class TestTypeListView(View):
    def get(self,request):
        test_type_list = TestType.objects.all()
        context ={
            "test_type_list":test_type_list
        }
        return render(request,"hospital/test_type_list.html",context)



class UpdateTestTypeView(View):
    
    def get(self, request, pk, *args, **kwargs):
        test_type = TestType.objects.get(pk=pk)
        context = {'test_type': test_type}
        return render(request, "hospital/update_test_type.html", context)

    def post(self, request, pk, *args, **kwargs):
        test_type = TestType.objects.get(pk=pk)
        test_type.name = request.POST.get('name')
        test_type.short_name = request.POST.get('short_name')
        test_type.amount = request.POST.get('amount')
        test_type.description = request.POST.get('description')
        test_type.preparation_instructions = request.POST.get('preparation_instructions')

        test_type.save()
        messages.success(request, 'Test Type updated successfully!')
        return redirect('dashboard:test_type_list')



class DeleteTestTypeView(View):
    def get(self, request, pk):
        test_type = get_object_or_404(TestType, id=pk)
        test_type.delete()
        messages.success(request, 'Test Type Deleted successfully!')
        return redirect('dashboard:test_type_list')


"""
        ---------- Add Medical Test ------------
"""

class AddMedicalTestView(View):
    
    def get(self, request, *args, **kwargs):
        context = {
            'patient_list': Patient.objects.all(),
            'doctor_list': Doctor.objects.all(),
            'test_type_list': TestType.objects.all(),
        }
        return render(request, "hospital/add_medical_test.html", context)

    def post(self, request, *args, **kwargs):
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        test_type_id = request.POST.get('test_type')
        amount = request.POST.get('amount')
        test_date = request.POST.get('test_date')
        details = request.POST.get('details')

        try:
            patient = Patient.objects.get(id=patient_id)
            doctor = Doctor.objects.get(id=doctor_id)
            test_type = TestType.objects.get(id=test_type_id)

            medical_test = MedicalTest(
                patient=patient,
                doctor=doctor,
                test_type=test_type,
                amount=amount,
                test_date=test_date,
                details=details,
            )

            medical_test.save()
            messages.success(request, 'Medical test added successfully!')
            return redirect('dashboard:medical_test_list')

        except (Patient.DoesNotExist, Doctor.DoesNotExist, TestType.DoesNotExist) as e:
            messages.error(request, 'Error adding medical test. Please check the form.')
        
        context = {
            'patient_list': Patient.objects.all(),
            'doctor_list': Doctor.objects.all(),
            'test_type_list': TestType.objects.all(),
        }
        return render(request, "hospital/add_medical_test.html", context)



class GetTestVisitPriceView(View):
    def get(self, request, test_type_id, *args, **kwargs):
        test_type = get_object_or_404(TestType, id=test_type_id)
        visit_price = test_type.amount
        return JsonResponse({'visit_price': visit_price})



class MedicalTestListView(View):
    def get(self,request):
        medical_test_type_list = MedicalTest.objects.all()
        context ={
            "medical_test_type_list":medical_test_type_list
        }
        return render(request,"hospital/medical_test_list.html",context)



class UpdateMedicalTestView(View):
    
    def get(self, request, pk, *args, **kwargs):
        medical_test = get_object_or_404(MedicalTest, id=pk)
        context = {
            'patient_list': Patient.objects.all(),
            'doctor_list': Doctor.objects.all(),
            'test_type_list': TestType.objects.all(),
            'medical_test': medical_test,
        }
        return render(request, "hospital/update_medical_test.html", context)

    def post(self, request, pk, *args, **kwargs):
        medical_test = get_object_or_404(MedicalTest, id=pk)
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        test_type_id = request.POST.get('test_type')
        amount = request.POST.get('amount')
        test_date = request.POST.get('test_date')
        details = request.POST.get('details')

        try:
            patient = Patient.objects.get(id=patient_id)
            doctor = Doctor.objects.get(id=doctor_id)
            test_type = TestType.objects.get(id=test_type_id)

            medical_test.patient = patient
            medical_test.doctor = doctor
            medical_test.test_type = test_type
            medical_test.amount = amount
            medical_test.test_date = test_date
            medical_test.details = details

            medical_test.save()
            messages.success(request, 'Medical test updated successfully!')
            return redirect('dashboard:medical_test_list')

        except (Patient.DoesNotExist, Doctor.DoesNotExist, TestType.DoesNotExist) as e:
            messages.error(request, 'Error updating medical test. Please check the form.')
        
        context = {
            'patient_list': Patient.objects.all(),
            'doctor_list': Doctor.objects.all(),
            'test_type_list': TestType.objects.all(),
            'medical_test': medical_test,
        }
        return render(request, "hospital/update_medical_test.html", context)



class DeleteMedicalTestView(View):
    def get(self, request, pk):
        medical_test = get_object_or_404(MedicalTest, id=pk)
        medical_test.delete()
        messages.success(request, 'Medical Test Deleted successfully!')
        return redirect('dashboard:medical_test_list')



"""
        -------------- Medical Test Report ------------
"""

class AddTestImageReportView(View):

    def get(self, request, *args, **kwargs):
        medical_test_list = MedicalTest.objects.all()
        context = {'medical_test_list': medical_test_list}
        return render(request, "hospital/add_test_image_report.html", context)

    def post(self, request, *args, **kwargs):
        medical_test_id = request.POST.get('medical_test')
        qr_code = request.POST.get('qr_code')
        description = request.POST.get('description')
        images = request.FILES.getlist('image')

        medical_test = MedicalTest.objects.get(id=medical_test_id)

        try:
            medical_test_image = MedicalTestImage.objects.get(qr_code=qr_code)
            
            # Update the existing instance
            medical_test_image.medical_test = medical_test
            medical_test_image.description = description

        except MedicalTestImage.DoesNotExist:
            # If not found, create a new instance
            medical_test_image = MedicalTestImage(
                medical_test=medical_test,
                qr_code=qr_code,
                description=description
            )
            medical_test_image.save()

        # Save images to Image
        for image in images:
            new_image = Image(medical_test_image=medical_test_image, image=image)
            new_image.save()

        return redirect('dashboard:test_image_report_all')



class MedicalTestImageListView(View):
    def get(self,request):
        medial_test_list = MedicalTestImage.objects.all()
        context ={
            "medial_test_list":medial_test_list
        }
        return render(request,"hospital/test_image_report_all.html",context)
    


class MedicalReportImageListView(View):
    def get(self, request, pk):
        medical_test_image = get_object_or_404(MedicalTestImage, id=pk)
        medical_test_images = Image.objects.filter(medical_test_image=medical_test_image)
        context = {
            "medical_test_images": medical_test_images
        }
        return render(request, "hospital/report_image.html", context)




"""
||||||||| ***********Image Post API *********** ||||||||||| 
"""


class TestImageReportAPIView(APIView):
    def get(self, request):
        medical_tests = MedicalTest.objects.all()
        serializer = MedicalTestSerializer(medical_tests, many=True)
        return Response(serializer.data)

    def post(self, request):
        medical_test_id = request.data.get('medical_test')
        qr_code = request.data.get('qr_code')
        description = request.data.get('description')
        images = request.FILES.getlist('image')

        medical_test = MedicalTest.objects.get(id=medical_test_id)

        try:
            medical_test_image = MedicalTestImage.objects.get(qr_code=qr_code)
            medical_test_image.medical_test = medical_test
            medical_test_image.description = description
            medical_test_image.save()

        except MedicalTestImage.DoesNotExist:
            medical_test_image = MedicalTestImage(
                medical_test=medical_test,
                qr_code=qr_code,
                description=description
            )
            medical_test_image.save()

        for image in images:
            new_image = Image(medical_test_image=medical_test_image, image=image)
            new_image.save()

        return Response(status=status.HTTP_201_CREATED)

