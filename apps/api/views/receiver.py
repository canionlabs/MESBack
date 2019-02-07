from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

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

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['type', 'device_id', 'time'],
            properties={
                'type': openapi.Schema(type=openapi.TYPE_STRING),
                'device_id': openapi.Schema(type=openapi.TYPE_STRING),
                'time': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        security=[],
        responses={200: '{}'}
    )
    def post(self, request):

        rsp = {}
        data = self.request.data
        device_id = data.get('device_id')
        registered_device = Device.objects.filter(device_id=device_id).exists()

        if registered_device:
            status_code = status.HTTP_201_CREATED
            packages.insert_one({
                'type': PACKAGE_TYPES[int(data['package_type']) - 1],
                'device_id': device_id,
                'time': datetime.strptime(
                    data['created'], '%d/%m/%Y %H:%M:%S'
                ),
            })
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(status=status_code)
