# Generated by Django 4.1.5 on 2023-02-12 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('full_name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('profile_avatar', models.ImageField(default='media/default/profile_avatar.png', upload_to='media/profile')),
                ('otp', models.CharField(blank=True, max_length=5, null=True)),
                ('user_type', models.CharField(choices=[('1', 'Administrator'), ('2', 'Vendor'), ('3', 'Customer')], default='3', max_length=1)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
