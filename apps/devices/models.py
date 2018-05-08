from django.db import models
from apps.core.models import DefaultModel

import requests


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

    @property
    def total_production(self):
        r = requests.post(
            f'http://127.0.0.1:8000/packages:list?device_id={self.device_id}'
        )
        return r.json()['count']

    @property
    def most_produced(self):
        types = ['a', 'b', 'c', 'd']
        count = {}
        for t in types:
            r = requests.post(
                f'http://127.0.0.1:8000/packages:list?' +
                'device_id={self.device_id}&type={t}'
            )
            count[t] = r.json()['count']

        value = 0
        for k, v in count.items():
            if v > value:
                most_produced = k
                v = value

        return getattr(self, ('type_' + most_produced))
