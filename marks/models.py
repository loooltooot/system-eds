from django.db import models
from django.conf import settings

# Create your models here.

class StudentsUnit(models.Model):
    name = models.CharField('номер', max_length=128)
    description = models.TextField('описание', blank=True)

    class Meta:
        verbose_name = 'группа/класс'
        verbose_name_plural = 'группы/классы'

class Subject(models.Model):
    name = models.CharField('название', max_length=128)
    description = models.TextField('описание', blank=True)

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'предметы'

class Appointment(models.Model):
    students_unit = models.ForeignKey(StudentsUnit, on_delete=models.PROTECT, verbose_name='группа/класс')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name='предмет')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='преподаватель')
    pub_date = models.DateTimeField('дата назначения', auto_now_add=True)
    
    class Meta:
        verbose_name = 'назначение преподавателя'
        verbose_name_plural = 'назначения преподавателей'

class Mark(models.Model):
    value = models.PositiveSmallIntegerField('оценка')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name='предмет')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='set_marks', verbose_name='выставленные оценки')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='received_marks', verbose_name='полученные оценки')
    pub_date = models.DateTimeField('дата оценивания', auto_now_add=True)

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'

    def __str__(self):
        return self.value