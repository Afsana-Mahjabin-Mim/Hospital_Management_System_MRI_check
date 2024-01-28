# Generated by Django 4.1.5 on 2024-01-25 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0010_remove_medicaltestimage_images_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="medicaltestimage",
            name="image",
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="medical_tests_image/")),
                (
                    "medical_test_image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="medical_test_image",
                        to="doctors.medicaltestimage",
                    ),
                ),
            ],
        ),
    ]
