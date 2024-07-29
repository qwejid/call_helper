from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Break(models.Model):
    replacement = models.ForeignKey(
        'breaks.Replacement', models.CASCADE, related_name='breaks', verbose_name='Смена',
    )
    member = models.ForeignKey(
        'breaks.ReplacementMember', models.CASCADE, 'breaks',
        verbose_name='Участник смены',
    )
    break_start = models.TimeField('Начало обеда', null=True, blank=True)
    break_end = models.TimeField('Конец обеда', null=True, blank=True)

    class Meta:
        verbose_name = 'Обеденный перерыв'
        verbose_name_plural = 'Обеденные перерывы'
        ordering = ('-replacement__date', 'break_start')

    def __str__(self):
        return f'Обед пользователя {self.member} ({self.pk})'
