from django.db import models

from apps.core.models import DefaultModel

from datetime import datetime
import json


TYPE_CHOICES = (('tubo', 'Tubo'), ('escama', 'Escama'), ('barra', 'Barra'))


class IceProduction(DefaultModel):

    ice_type = models.CharField('Tipo', max_length=75, choices=TYPE_CHOICES)
    topic = models.CharField('Tópico MQTT', max_length=175)
    weight = models.CharField('Peso', max_length=75)
    date = models.DateField('Data')
    hour = models.TimeField('Horário')

    class Meta:
        verbose_name = 'Produção de Gelo'
        verbose_name_plural = 'Produção de Gelo'

    def __str__(self):
        return self.ice_type

    def simple_save(data):
        def json_decode(json_str):
            try:
                data_json = json.loads(json_str)
                get_weigth = data_json['msg']['button']
                return get_weigth
            except KeyError:
                pass

        def type_detect(topic):
            for ice_type in TYPE_CHOICES:
                if ice_type[0] in topic:
                    return ice_type[0]

        new_register = IceProduction(
            ice_type=type_detect(data['topic']),
            topic=data['topic'], weight=json_decode(data['weight']),
            date=datetime.strptime(data['created'], '%d/%m/%Y %H:%M:%S'),
            hour=datetime.strptime(data['created'], '%d/%m/%Y %H:%M:%S'),

        )
        return new_register.save()
