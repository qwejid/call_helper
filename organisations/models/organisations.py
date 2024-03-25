from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Organisation(models.Model):
    name = models.CharField('Название', max_length=255)
    director = models.ForeignKey(
        User, models.RESTRICT, 'organisations_director', 
        verbose_name='Директор',
    )
    employees = models.ManyToManyField(
        User, 'organisations_employees', verbose_name='Сотрудники',
        blank=True, through='Employee'
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.pk})'

class Employee(models.Model):
    organisation = models.ForeignKey(
        'Organisation', models.CASCADE, related_name='employees_info'
    )
    user = models.ForeignKey(
        User, models.CASCADE, 'organisations_info', 
    )
    position = models.ForeignKey(
        'Position', models.RESTRICT, 'employees',
    )
    date_joined = models.DateField('Date joined', default=timezone.now())

    class Meta:
        verbose_name = 'Сотрудник организации'
        verbose_name_plural = 'Сотрудники организаций'
        ordering = ('-date_joined',)
        unique_together = (('organisation', 'user'),)

    def __str__(self):
        return f' Employee {self.user}'