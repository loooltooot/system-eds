# Generated by Django 4.1.13 on 2024-06-03 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='дата назначения')),
                ('course', models.PositiveSmallIntegerField(verbose_name='курс')),
                ('is_first_term', models.BooleanField(verbose_name='первое полугодие?')),
            ],
            options={
                'verbose_name': 'назначение преподавателя',
                'verbose_name_plural': 'назначения преподавателей',
            },
        ),
        migrations.CreateModel(
            name='StudentsUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='номер')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'группа/класс',
                'verbose_name_plural': 'группы/классы',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='название')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'предмет',
                'verbose_name_plural': 'предметы',
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('H', 'H'), ('/', '/'), ('+', '+'), ('.', '.')], max_length=2, verbose_name='оценка')),
                ('feedback', models.TextField(blank=True, verbose_name='обратная связь')),
                ('is_final', models.BooleanField(verbose_name='итоговая оценка?')),
                ('pub_date', models.DateField(verbose_name='дата оценивания')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='marks.appointment', verbose_name='предмет')),
                ('student', models.ForeignKey(limit_choices_to={'groups__name': 'Студенты'}, on_delete=django.db.models.deletion.PROTECT, related_name='received_marks', to=settings.AUTH_USER_MODEL, verbose_name='студент')),
            ],
            options={
                'verbose_name': 'оценка',
                'verbose_name_plural': 'оценки',
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='students_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='marks.studentsunit', verbose_name='группа/класс'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='marks.subject', verbose_name='предмет'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='teacher',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'Преподаватели'}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='преподаватель'),
        ),
    ]
