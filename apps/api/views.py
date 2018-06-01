from rest_framework.views import APIView
from rest_framework import permissions
from django.http import JsonResponse

from datetime import datetime, timedelta

from mongoengine import connect
from pymongo import MongoClient, DESCENDING


client = MongoClient()
packages = client.mes.packages
packages.create_index([
    ('device_id', DESCENDING),
    ('time', DESCENDING),
    ('type', DESCENDING)
])


class CardsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def device_info(self, device):

        def get_active_types():
            active_types = ['a', 'b', 'c', 'd']
            for pkg_type in active_types:
                if not getattr(device, f'type_{pkg_type}'):
                    active_types.remove(pkg_type)
            return active_types

        def create_filter():
            type_filter = {'$or': []}
            for act_type in get_active_types():
                type_filter['$or'].append({'type': act_type})
            return type_filter

        now = datetime.now()
        start_day = now.replace(hour=0, minute=0, second=0)
        final_day = now.replace(hour=23, minute=59, second=59)
        device_id = device.device_id
        or_filter = create_filter()

        def daily_prod():
            return packages.find({
                'device_id': device_id,
                'time': {'$gte': start_day, '$lte': final_day},
                **or_filter
            }).count()

        def daily_init():
            daily_query = packages.find({
                'device_id': device_id,
                'time': {'$gte': start_day, '$lte': final_day},
                **or_filter
            }).limit(1)

            try:
                return list(daily_query)[0]['time'].strftime('%H:%M:%S')
            except IndexError:
                return '--:--:--'

        def weekly_type():
            def get_name(pkg_type):
                try:
                    return getattr(device, f'type_{pkg_type}')
                except Exception as e:
                    pass

            def get_start_week(now):
                start_week = now.replace(hour=0, minute=0, second=0)
                one_day = timedelta(days=1)
                while start_week.weekday() != 1:
                    start_week = start_week - one_day
                return start_week

            weekly_start_date = get_start_week(now)
            value = 0
            pkg_type = ''
            for t in get_active_types():
                count = packages.find({
                    'device_id': device_id,
                    'time': {'$gte': weekly_start_date, '$lte': final_day},
                    'type': t
                }).count()
                if count > value:
                    value = count
                    pkg_type = t
            return get_name(pkg_type)

        def weekly_prod():
            def get_start_week(now):
                start_week = now.replace(hour=0, minute=0, second=0)
                one_day = timedelta(days=1)
                while start_week.weekday() != 0:
                    start_week = start_week - one_day
                return start_week

            weekly_start_date = get_start_week(now)
            return packages.find({
                'device_id': device_id,
                'time': {'$gte': weekly_start_date, '$lte': final_day},
                **or_filter
            }).count()

        return {
            'device_id': f'{device_id}',
            'daily_prod': daily_prod(),
            'daily_init': daily_init(),
            'weekly_type': weekly_type(),
            'weekly_prod': weekly_prod()
        }

    def get(self, request):
        client = self.request.user.client
        devices = client.get_devices()
        rsp = {d.name: self.device_info(d) for d in devices}

        return JsonResponse(rsp)


class InfoMonthlyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def montly_prod(self, device):
        def get_active_types():
            active_types = ['a', 'b', 'c', 'd']
            for pkg_type in active_types:
                if not getattr(device, f'type_{pkg_type}'):
                    active_types.remove(pkg_type)
            return active_types

        def get_name(pkg_type):
            try:
                return getattr(device, f'type_{pkg_type}')
            except Exception as e:
                pass

        def get_last_day(now):
            last_day = 31
            while True:
                try:
                    return now.replace(day=last_day).day
                except ValueError:
                    last_day -= 1

        monthly_rsp = {}
        now = datetime.now()
        device_id = device.device_id
        start_month = now.replace(day=1, hour=0, minute=0, second=0)
        final_month = now.replace(day=get_last_day(now))
        for pkg_type in get_active_types():
            type_name = get_name(pkg_type)
            if type_name:
                type_count = packages.find({
                    'device_id': device_id,
                    'time': {'$gte': start_month, '$lte': final_month},
                    'type': pkg_type
                }).count()
                monthly_rsp[type_name] = type_count
        return monthly_rsp

    def get(self, request):
        rsp = {}
        client = self.request.user.client
        devices = client.get_devices()
        for device in devices:
            rsp.update(self.montly_prod(device))
        return JsonResponse(rsp)


class InfoWeeklyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def weekly_prod(self, device):
        def get_active_types():
            active_types = ['a', 'b', 'c', 'd']
            for pkg_type in active_types:
                if not getattr(device, f'type_{pkg_type}'):
                    active_types.remove(pkg_type)
            return active_types

        def get_start_week(now):
            start_week = now.replace(hour=0, minute=0, second=0)
            one_day = timedelta(days=1)
            while start_week.weekday() != 0:
                start_week = start_week - one_day
            return start_week

        def get_name(pkg_type):
            try:
                return getattr(device, f'type_{pkg_type}')
            except Exception as e:
                pass

        weekly_rsp = {}
        now = datetime.now()
        device_id = device.device_id
        start_week = get_start_week(now)
        final_week = now
        one_day = timedelta(days=1)
        types = get_active_types()
        while start_week.weekday() <= final_week.weekday():
            weekly_rsp[start_week.weekday()] = {}

            for pkg_type in types:
                type_name = get_name(pkg_type)
                final_day = start_week.replace(hour=23, minute=59, second=59)
                if type_name:
                    type_count = packages.find({
                        'device_id': device_id,
                        'time': {'$gte': start_week, '$lte': final_day},
                        'type': pkg_type
                    }).count()
                    weekly_rsp[start_week.weekday()][type_name] = type_count

            start_week = start_week + one_day
        return weekly_rsp

    def get(self, request):
        rsp = {}
        client = self.request.user.client
        devices = client.get_devices()
        for device in devices:
            for k, v in (self.weekly_prod(device)).items():
                if rsp.get(k):
                    rsp[k].update(v)
                else:
                    rsp[k] = v
        return JsonResponse(rsp)


class InfoDailyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_daily_prod(self, device):
        def get_active_types():
            active_types = ['a', 'b', 'c', 'd']
            for pkg_type in active_types:
                if not getattr(device, f'type_{pkg_type}'):
                    active_types.remove(pkg_type)
            print(active_types)
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
        init_day = today.replace(hour=0, minute=0, second=0)
        final_day = today.replace(hour=23, minute=59, second=59)
        rsp_daily = {}
        print(get_active_types())
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
                for hour in range(0, 23):
                    final_hour = init_day.replace(minute=59, second=59)
                    iso_final = final_hour.isoformat()
                    iso_init = init_day.isoformat()
                    js_filter = f'''
                        function () {{
                            return (
                                this.time >= ISODate("{iso_init}") &&
                                this.time <= ISODate("{iso_final}") &&
                                this.type == "{pkg_type}"
                            )
                        }}
                    '''
                    query_hour = main_query.where(js_filter)
                    count = query_hour.count()
                    rsp_daily[pkg_name].append(count)
                    print(rsp_daily)
                    init_day = init_day + timedelta(hours=1)
        return rsp_daily

    def get(self, request):
        rsp = {}
        client = self.request.user.client
        devices = client.get_devices()
        for device in devices:
            rsp.update(self.get_daily_prod(device))
        return JsonResponse(rsp)
