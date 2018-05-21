from django.db import models
from apps.core.models import DefaultModel


class Device(DefaultModel):

    organization = models.ForeignKey(
        'customers.Organization',
        related_name='org_device', on_delete=models.CASCADE
    )
    name = models.CharField('Nome', max_length=175, null=True, blank=True)
    device_id = models.CharField('Device ID', max_length=275)
    type_a = models.CharField('Tipo A', max_length=75, null=True, blank=True)
    type_b = models.CharField('Tipo B', max_length=75, null=True, blank=True)
    type_c = models.CharField('Tipo C', max_length=75, null=True, blank=True)
    type_d = models.CharField('Tipo D', max_length=75, null=True, blank=True)

    def __str__(self):
        return self.name or self.device_id

    class Meta:
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'
