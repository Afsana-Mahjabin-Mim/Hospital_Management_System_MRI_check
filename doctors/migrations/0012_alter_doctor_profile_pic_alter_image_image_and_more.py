# Generated by Django 4.1.5 on 2024-02-20 09:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("doctors", "0011_remove_medicaltestimage_image_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="profile_pic",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/profile_pic/DoctorProfilePic/"
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="image",
            field=models.ImageField(upload_to="media/medical_tests_image/"),
        ),
        migrations.AlterField(
            model_name="patient",
            name="profile_pic",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/profile_pic/PatientProfilePic/"
            ),
        ),
    ]