from django.db import models
from django.conf import settings

# Create your models here.

class StudentsUnit(models.Model):
    name = models.CharField('номер', max_length=128)
    description = models.TextField('описание', blank=True)

    class Meta:
        verbose_name = 'группа/класс'
        verbose_name_plural = 'группы/классы'

    def __str__(self) -> str:
        return self.name

class Subject(models.Model):
    name = models.CharField('название', max_length=128)
    description = models.TextField('описание', blank=True)

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'предметы'

    def __str__(self) -> str:
        return self.name

class Appointment(models.Model):
    students_unit = models.ForeignKey(StudentsUnit, on_delete=models.PROTECT, verbose_name='группа/класс')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name='предмет')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
        verbose_name='преподаватель', limit_choices_to={'groups__name': 'Преподаватели'}
    )
    pub_date = models.DateTimeField('дата назначения', auto_now_add=True)
    
    class Meta:
        verbose_name = 'назначение преподавателя'
        verbose_name_plural = 'назначения преподавателей'

    def __str__(self) -> str:
        return f'{self.students_unit} {self.subject} {self.teacher}'.strip()

class Mark(models.Model):
    VALUES_CHOICES = [
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('H', 'H'),
        ('/', '/'),
        ('+', '+'),
        ('.', '.'),
    ]

    value = models.CharField('оценка', max_length=2, choices=VALUES_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name='предмет')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
        related_name='set_marks', verbose_name='учитель', limit_choices_to={'groups__name': 'Преподаватели'}
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
        related_name='received_marks', verbose_name='студент', limit_choices_to={'groups__name': 'Студенты'}
    )
    feedback = models.TextField('обратная связь', blank=True)
    pub_date = models.DateField('дата оценивания')

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'

    def __str__(self):
        return f'{self.value} ({self.subject}) {self.student}'.strip()