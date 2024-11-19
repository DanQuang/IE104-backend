
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        """
        Creates and saves a User with the given email and full name.
        """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        """
        Creates and saves a Superuser with the given email and full name.
        """
        user = self.create_user(
            email=email,
            full_name=full_name,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
    
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        return True

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        All admins are staff members.
        """
        return self.is_admin