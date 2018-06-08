from rest_framework.views import APIView
from django.http import JsonResponse

from apps.customers.models import Organization

from pymongo import MongoClient, DESCENDING, ASCENDING

from datetime import datetime, timedelta

client = MongoClient()
packages = client.mes.packages
packages.create_index([
    ('device_id', DESCENDING),
    ('time', ASCENDING),
    ('type', DESCENDING)
])


class CheckView(APIView):

    def post(self, request):
        rsp = {}

        chat_token = self.request.data.get('org_token')
        query_org = Organization.objects.filter(chatbot_token=chat_token)
        print(query_org)
        if query_org.exists():
            organization = query_org.last()
            rsp['data'] = {'org_name': organization.name}
            return JsonResponse(rsp)
        return JsonResponse(rsp, status=401)


class DailyView(APIView):

    def get_daily_prod(self, device):
        def get_active_types():
            active_types = []
            for pkg_tp in ['a', 'b', 'c', 'd']:
                if getattr(device, f'type_{pkg_tp}'):
                    active_types.append(pkg_tp)
            return active_types

        def create_filter():
            type_filter = {'$or': []}
            for act_type in get_active_types():
                type_filter['$or'].append({'type': act_type})
            return type_filter

        def get_name(pkg_type):
            try:
                return getattr(device, f'type_{pkg_type}')
            except Exception as e:
                pass

        today = datetime.now()
        init_day = today.replace(
            hour=0, minute=0, second=0, microsecond=000000)
        final_day = today.replace(
            hour=23, minute=59, second=59, microsecond=999999)

        rsp_daily = {}
        or_filter = create_filter()
        main_query = packages.find({
            'device_id': device.device_id,
            'time': {'$gte': init_day, '$lte': final_day},
            **or_filter
        })
        for pkg_type in get_active_types():
            if get_name(pkg_type):
                pkg_name = get_name(pkg_type)
                rsp_daily[pkg_name] = []
                init_day = today.replace(
                    hour=0, minute=0, second=0, microsecond=000000)
                final_day = today.replace(
                    hour=23, minute=59, second=59, microsecond=999999)

                js_filter = f'''
                    function () {{
                        return (
                            this.type == "{pkg_type}"
                        )
                    }}
                '''

                query_hour = main_query.where(js_filter)
                rsp_daily[pkg_name] = query_hour.count()

        return rsp_daily

    def post(self, request):
        rsp = {}
        chat_token = self.request.data.get('org_token')
        query_org = Organization.objects.filter(chatbot_token=chat_token)
        if query_org.exists():
            org = query_org.first()
            devices = org.get_devices()
            for device in devices:
                rsp.update(self.get_daily_prod(device))
        return JsonResponse(rsp)
