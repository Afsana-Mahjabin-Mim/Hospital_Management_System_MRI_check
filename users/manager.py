from django.contrib.auth.models import BaseUserManager
import random 
class UserManager(BaseUserManager):
    def create_user(self,email,full_name,dob,phone_number,address,user_type="3",otp=None, password=None,**kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            user_type=user_type,
            full_name=full_name,
            dob=dob,
            phone_number=phone_number,
            address=address,
            otp=otp
           
        )
       
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,full_name,dob,phone_number,address, password=None,**kwargs):
        """
        Creates and saves a superuser with the given email,
        and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            dob=dob,
            phone_number=phone_number,
            address=address,
            
        )
    
        user.is_admin = True
        user.is_superuser=True 
        user.user_type="1"
        user.otp=random.randint(11111,99999)
        user.save(using=self._db)
        return user 


