from django import template
from apps.devices.models import Device


register = template.Library()


@register.simple_tag
def weekly_production_by_type(value_list):
    value = 0
    for k, v in value_list.items():
        if (k.startswith('weekly_type_') and v > value):
            most_produced = k
            v = value

    device = Device.objects.get(device_id=value_list['device_id'])
    return getattr(device, ('type_' + most_produced[-1]))
