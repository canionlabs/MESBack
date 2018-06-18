from rest_framework.views import APIView
from django.http import JsonResponse

from apps.devices.models import Device

from pymongo import MongoClient, DESCENDING, ASCENDING
from prettyconf import config

from datetime import datetime


MONGO_URI = config('MONGO_URI', default='mongodb://localhost:27017/')

client = MongoClient(MONGO_URI)
packages = client.mes.packages
packages.create_index([
    ('device_id', DESCENDING),
    ('time', ASCENDING),
    ('type', DESCENDING)
])

PACKAGE_TYPES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


class ReceiverView(APIView):
    """
    Receive gateway data and save.
    """
    def get(self, request):

        rsp = {}
        data = self.request.data
        device_id = data['device_id']
        registered_device = Device.objects.filter(device_id=device_id).exists()

        if registered_device:
            packages.insert_one({
                'type': data['package_type'],
                'device_id': data['device_id'],
                'time': datetime.strptime(
                    data['created'], '%d/%m/%Y %H:%M:%S'
                ),
            })

        return JsonResponse(rsp)
