from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('tourist', 'Tourist'),
        ('agent', 'Tour Agent'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='tourist')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    passport_number = models.CharField(max_length=50, blank=True)
    license_number = models.CharField(max_length=50, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Specify a custom related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Specify a custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class BaseProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    DOB = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

class TouristProfile(BaseProfile):
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Tourist: {self.user.username}"

class AgentProfile(BaseProfile):
    company_name = models.CharField(max_length=255, blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Agent: {self.user.username}"

class AdminProfile(BaseProfile):
    role = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Agent: {self.user.username}"