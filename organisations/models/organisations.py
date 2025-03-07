from auditlog.registry import auditlog
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from common.models.mixins import InfoMixin
from organisations.constants import DIRECTOR_POSITION, MANAGER_POSITION, \
    OPERATOR_POSITION

User = get_user_model()


class Organisation(InfoMixin):
    name = models.CharField('Название', max_length=255)
    director = models.ForeignKey(
        User, models.RESTRICT, 'organisations_directors',
        verbose_name='Директор',
    )
    employees = models.ManyToManyField(
        User, 'organisations_employees', verbose_name='Сотрудники',
        blank=True, through='Employee'
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ('name', 'id',)

    def __str__(self):
        return f'{self.name} ({self.pk})'

    @property
    def director_employee(self):
        obj, create = self.employees_info.get_or_create(
            position_id=DIRECTOR_POSITION, defaults={'user': self.director, }
        )
        return obj


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
    date_joined = models.DateField('Date joined', default=timezone.now)

    class Meta:
        verbose_name = 'Сотрудник организации'
        verbose_name_plural = 'Сотрудники организаций'
        ordering = ('-date_joined',)
        unique_together = (('organisation', 'user'),)

    def __str__(self):
        return f'Employee #{self.pk} {self.user}'

    @property
    def is_director(self):
        if self.position_id == DIRECTOR_POSITION:
            return True
        return False

    @property
    def is_manager(self):
        if self.position_id == MANAGER_POSITION:
            return True
        return False

    @property
    def is_operator(self):
        if self.position_id == OPERATOR_POSITION:
            return True
        return False


auditlog.register(Organisation)
