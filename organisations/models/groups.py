from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from common.models.mixins import InfoMixin


User = get_user_model()

class Group(InfoMixin):
    organisation = models.ForeignKey(
        'Organisation', models.CASCADE, related_name='groups',
        verbose_name='Организация',
    )
    name = models.CharField('Название', max_length=255)
    manager = models.ForeignKey(
        User, models.RESTRICT, 'groups_managers', 
        verbose_name='Мэнаджер',
    )    
    members = models.ManyToManyField(
        User, 'groups_members', verbose_name='Участники группы',
        blank=True, through='Member'
    )   
    
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.pk})'
    

class Member(models.Model):
    group = models.ForeignKey(
        'Group', models.CASCADE, related_name='members_info'
    )
    user = models.ForeignKey(
        User, models.CASCADE, 'groups_info', 
    )    
    date_joined = models.DateField('Date joined', default=timezone.now())

    class Meta:
        verbose_name = 'Участник группы'
        verbose_name_plural = 'Участники групп'
        ordering = ('-date_joined',)
        unique_together = (('group', 'user'),)

    def __str__(self):
        return f' Member {self.user}'
    