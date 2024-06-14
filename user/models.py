from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser, PermissionsMixin
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.
class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail")
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', email)


        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser, PermissionsMixin):
    ROLES = (
        ("customer", "Customer"),
        ("company", "Company"),
        ("admin", "Admin")
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLES, default="customer")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class UserProfile(models.Model):
    REGION = (

    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    region = models.CharField(max_length=25, choices=REGION, default='Tbilisi')
    location = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.email
    