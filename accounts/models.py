from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, is_admin=False, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name, 
            is_admin=is_admin           
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, is_admin=True, password=None):
        """
        Creates and saves a Superuser with the given email, name and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            full_name=full_name,   
            is_admin=is_admin         
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User Model.
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['full_name', 'is_admin']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

# CreditAccount Model
class CreditAccount(models.Model):
    account_number = models.CharField(max_length=255, unique=True)
    account_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_accounts')

    def __str__(self):
        return f"{self.account_name} ({self.account_number})"

# Service Model
class Service(models.Model):
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.description} - ${self.price}"

# Tier Model
class Tier(models.Model):
    current_tier = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tiers')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='tiers')
    start_day = models.DateField()
    end_day = models.DateField()

    def __str__(self):
        return f"{self.current_tier} for {self.user.email}"