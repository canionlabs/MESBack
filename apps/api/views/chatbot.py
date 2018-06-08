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

    def get_daily_prod(self, device, req_date=None):
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

        now = datetime.now()
        today = datetime.strptime(req_date, '%d/%m/%Y') if req_date else now
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
        req_date = self.request.data.get('date')
        query_org = Organization.objects.filter(chatbot_token=chat_token)
        if query_org.exists():
            org = query_org.first()
            devices = org.get_devices()
            for device in devices:
                rsp.update(self.get_daily_prod(device, req_date))
        return JsonResponse(rsp)


class WeeklyView(APIView):

    def get_weekly_prod(self, device):
        def get_active_types():
            active_types = []
            for pkg_tp in ['a', 'b', 'c', 'd']:
                if getattr(device, f'type_{pkg_tp}'):
                    active_types.append(pkg_tp)
            return active_types

        def get_start_week(now):
            start_week = now.replace(hour=0, minute=0, second=0)
            one_day = timedelta(days=1)
            while start_week.weekday() != 0:
                start_week = start_week - one_day
            return start_week
        
        def get_final_week(now):
            start_day = now.replace(hour=0, minute=0, second=0)
            one_day = timedelta(days=1)
            while start_day.weekday() != 6:
                start_day = start_day + one_day
            return start_day

        def get_name(pkg_type):
            try:
                return getattr(device, f'type_{pkg_type}')
            except Exception as e:
                pass

        weekly_rsp = {}
        now = datetime.now()
        device_id = device.device_id
        start_week = get_start_week(now)
        final_week = get_final_week(now)
        types = get_active_types()

        for pkg_type in types:
            if get_name(pkg_type):
                pkg_name = get_name(pkg_type)
                type_count = packages.find({
                    'device_id': device_id,
                    'time': {'$gte': start_week, '$lte': final_week},
                    'type': pkg_type
                }).count()

                weekly_rsp[pkg_name] = type_count

        return weekly_rsp

    def post(self, request):
        rsp = {}
        chat_token = self.request.data.get('org_token')
        query_org = Organization.objects.filter(chatbot_token=chat_token)
        if query_org.exists():
            org = query_org.first()
            devices = org.get_devices()
            for device in devices:
                rsp.update(self.get_weekly_prod(device))

        return JsonResponse(rsp)
