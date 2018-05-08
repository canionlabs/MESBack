from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.models import DefaultModel


class Organization(DefaultModel):
    name = models.CharField('Nome', max_length=75)
    active = models.BooleanField('Ativo', default=True)
    phone = models.CharField('Telefone', max_length=75, null=True, blank=True)
    chatbot_token = models.CharField(
        'Token do ChatBot', max_length=75, null=True, blank=True
    )

    class Meta:
        verbose_name = 'Organização'
        verbose_name_plural = 'Organizações'

    def __str__(self):
        return f'{self.name}'


class Client(DefaultModel):

    ROLES = (
        ('administrador', 'Administrador'),
        ('gerente', 'Gerente'),
        ('funcionario', 'Funcionário'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(
        'customers.Organization',
        related_name='client', on_delete=models.CASCADE, null=True, blank=True
    )
    role = models.CharField('Cargo', max_length=175, choices=ROLES)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.user.username}'

    def get_devices(self):
        return self.organization.org_device.all()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.client.save()
