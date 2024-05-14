from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from marks.models import StudentsUnit

# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, phone, surname, name, password=None, **extra_fields):
        if not phone:
            raise ValueError('Введите корректный номер телефона')

        extra_fields['email'] = self.normalize_email(extra_fields.get('email'))
        user = self.model(phone=phone, surname=surname, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, phone, surname, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, surname, name, password, **extra_fields)

    def create_superuser(self, phone, surname, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(phone, surname, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    surname = models.CharField('фамилия', max_length=128)
    name = models.CharField('имя', max_length=128)
    patronymic = models.CharField('отчество', max_length=128, blank=True)
    phone = models.CharField('номер телефона', max_length=128, unique=True)
    email = models.EmailField('электронная почта', max_length=128, blank=True)
    photo = models.ImageField('фото профиля', max_length=128, blank=True)
    is_staff = models.BooleanField('имеет доступ к панели', default=False)
    is_active = models.BooleanField('активная учетная запись', default=True)
    date_joined = models.DateTimeField('дата регистрации', default=timezone.now)
    students_unit = models.ForeignKey(StudentsUnit, on_delete=models.PROTECT, verbose_name='группа/класс', null=True, blank=True, help_text='только для студентов')

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
        return f'{self.surname} {self.name}'.strip()
    
    def __str__(self) -> str:
        return self.get_full_name()