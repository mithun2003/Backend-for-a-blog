from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password, name, is_staff=False, is_active=True, is_superuser=False, **extra_fields):
        if not email:
            raise ValueError('Users must have an valid email address')
        if self.model.objects.filter(email=email).exists():
            raise ValueError(f'Email: {email} Already exists.')
        if not password:
            raise ValueError('Users must have an valid password')
        if not name:
            raise ValueError('Users must have an valid name')
        user = self.model(
            email=self.normalize_email(email),
            name=name,

            is_staff=False,
            is_active=True,
            is_superuser=False,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name, **extra_fields):
        if not email:
            raise ValueError('Users must have an valid email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email