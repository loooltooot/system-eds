from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phone, surname, name, password=None, **extra_fields):
        pass

    def create_superuser(self, phone, surname, name, password=None, **extra_fields):
        pass

class User(AbstractBaseUser, PermissionsMixin):
    surname = models.CharField('фамилия', max_length=128)
    name = models.CharField('имя', max_length=128)
    patronymic = models.CharField('отчество', max_length=128, blank=True)
    phone = models.CharField('номер телефона', max_length=128, unique=True)
    email = models.EmailField('электронная почта', max_length=128, blank=True)
    photo = models.ImageField('фото профиля', max_length=128, blank=True)
    is_staff = models.BooleanField('имеет доступ к панели', default=False)
    is_active = models.BooleanField('активная учетная запись', default=True)

    USERNAME_FIELD = 'phone'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['surname', 'name']

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return f'{self.surname} {self.name} {self.patronymic}'.strip()

    def get_short_name(self):
        return self.name