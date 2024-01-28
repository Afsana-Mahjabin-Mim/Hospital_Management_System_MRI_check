from django.db import models 
from .manager import UserManager
from django.contrib.auth.models import (
    AbstractBaseUser
)
from django.utils.html import format_html


class User(AbstractBaseUser):
    full_name=models.CharField(max_length=100)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    ) 
    dob=models.DateField(blank=True,null=True)
    phone_number=models.CharField(max_length=20)
    address=models.TextField(blank=True,null=True)
    profile_avatar=models.ImageField(default="media/default/profile_avatar.png",upload_to="media/profiles")
    otp=models.CharField(max_length=5,blank=True,null=True)
    user_type=models.CharField(max_length=1,choices=(("1","Administrator"),("2","Doctor"),("3","Patient")),default="3")
    is_active = models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','phone_number','dob', 'address']
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin 

    def profile_avatar_circle(self):
        if self.profile_avatar:
            return format_html(f"<img src='{self.profile_avatar.url}' style='width:25px;border-radius:50%'>")
        else:
            return ""





