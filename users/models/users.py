from django.contrib.auth.models import AbstractUser, Group
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from users.managers import CustomUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models.profile import Profile


class Group(Group):
    code = models.CharField('Code', max_length=32, null=True, unique=True,)


class User(AbstractUser):
    username = models.CharField(
        'Никнейм', max_length=65, unique=True, null=True, blank=True,
    )
    email = models.EmailField('Почта', unique=True, null=True)
    phone_number = PhoneNumberField('Телефон', unique=True, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    is_corporate_account = models.BooleanField('Корпоротивный аккаунт', default=False,)

    objects = CustomUserManager()
    groups = models.ManyToManyField(Group, related_name='groups', verbose_name='Группы', blank=True,)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name} ({self.pk})'


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
