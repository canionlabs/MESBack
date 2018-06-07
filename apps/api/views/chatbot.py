from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

from apps.customers.models import Organization


class CheckView(APIView):

    def post(self, request):
        rsp = {}
        chat_token = self.request.POST.get('org_code')
        query_org = Organization.objects.filter(chatbot_token=chat_token)
        if query_org.exists():
            organization = query_org.last()
            rsp['data'] = {'org_name': organization.name}
            return JsonResponse(rsp)
        return JsonResponse(rsp, status.HTTP_401_UNAUTHORIZED)
