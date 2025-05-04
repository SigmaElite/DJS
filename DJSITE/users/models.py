from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields): #регистр для юзеров для супер ниже будет, e_f для возможности созд доп полей
        if not email:
            raise ValueError('The field must be set.')
        email = self.normalize_email(email)#инициализ
        user = self.model(email=email, **extra_fields)#s.model ссылается на модель(UsMa)
        user.set_password(password)
        user.save(using=self._db)#сохр в бд
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)#созд доп поле
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40, blank=True)# b=T поле может быть пустым(необязат для заполн)
    last_name = models.CharField(max_length=40, blank=True)
    middle_name = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=40, blank=True)
    house_number = models.CharField(max_length=10, blank=True)
    apartment_number = models.CharField(max_length=10, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email