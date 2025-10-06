from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user():
        def create_user(self,username,email,phone,first_name,last_name,password, **extra_fileds):
            if not email:
                raise ValueError("Email must be provided!")
            if not phone:
                raise ValueError("Phone Number must be provided!")
            if not(first_name or last_name):
                raise ValueError("Name is required!")
            
            email =  self.normalize_email(email)
            user = self.model(
                username=username,
                email = email,
                phone = phone,
                first_name = first_name,
                last_name = last_name,
                **extra_fileds
            )

            user.set_password(password)
            user.save(using=self._db)

            return user
        
        
        def create_superuser(self,username,email,phone,first_name,last_name,password,**extra_fileds):
            extra_fileds.setdefault('is_staff', True)
            extra_fileds.setdefault('is_superuser',True)

            if extra_fileds.get('is_staff') is not True:
                raise ValueError("Superuser must have is_staff=True")
            if extra_fileds.get('is_superuser') is not True:
                raise ValueError("Superuser must have is_superuser=True")
            
            return self.create_user(username,email,phone,password,first_name,last_name,**extra_fileds)