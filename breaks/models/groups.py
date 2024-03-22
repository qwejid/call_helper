from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Group(models.Model):
    organisation = models.ForeignKey(
        'breaks.Organisation', models.CASCADE, related_name='groups',
        verbose_name='Организация',
    )
    name = models.CharField('Название', max_length=255)
    manager = models.ForeignKey(
        User, models.RESTRICT, 'group_managers', 
        verbose_name='Мэнаджер',
    )
    employees = models.ManyToManyField(
        User, 'groups_employees', verbose_name='Сотрудники',
        blank=True,
    )
    min_active = models.PositiveSmallIntegerField(
        'Минимальное количество активных сотрудников',
        null=True, blank=True,
    )
    break_start = models.TimeField('Начало обеда', null=True, blank=True)
    break_end = models.TimeField('Конец обеда', null=True, blank=True)
    break_max_duration = models.PositiveSmallIntegerField(
        'Максимальная длительность обеда', null=True, blank=True,
    )
    
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.pk})'
    