from rest_framework.views import APIView
from rest_framework import permissions
from django.http import JsonResponse


class CardsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        rsp = {'key': 'value'}
        return JsonResponse(rsp)
