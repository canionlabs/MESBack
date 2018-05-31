from rest_framework.views import APIView
from rest_framework import permissions
from django.http import JsonResponse

from . import mongo_db

from datetime import datetime, timedelta

from mongoengine import connect

connect('mes', alias='default')


def fill_query(query, device):
    default_types = ['a', 'b', 'c', 'd']
    for pkg_type in default_types:
        if not getattr(device, f'type_{pkg_type}'):
            query = query.filter(package_type__ne=pkg_type)
    return query


class CardsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def device_info(self, device):
        now = datetime.now()
        start_day = now.replace(
            hour=0, minute=0, second=0
        )
        final_day = now.replace(
            hour=23, minute=59, second=59
        )
        device_id = device.device_id

        def daily_prod():
            query = mongo_db.PackageModel.objects(
                time__gte=start_day, time__lte=final_day, 
                device_id=device_id
            ).all()
            filter_query = fill_query(query, device)
            return filter_query.count()

        def daily_init():
            query = mongo_db.PackageModel.objects(
                time__gte=start_day, time__lte=final_day,
                device_id=device_id
            ).all()
            filter_query = fill_query(query, device)
            init_pkg = filter_query.limit(1)[0]
            if init_pkg:
                return init_pkg.time.strftime('%H:%M:%S')
            else:
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
            for t in ['a', 'b', 'c', 'd']:
                query = mongo_db.PackageModel.objects(
                    time__gte=weekly_start_date, time__lte=final_day,
                    device_id=device_id, package_type=t
                ).all()
                filter_query = fill_query(query, device)
                count = filter_query.count()
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
            query = mongo_db.PackageModel.objects(
                time__gte=weekly_start_date, time__lte=final_day,
                device_id=device_id
            ).all()
            filter_query = fill_query(query, device) 
            return filter_query.count()

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
        def get_name(pkg_type):
            try:
                return getattr(device, f'type_{pkg_type}')
            except Exception as e:
                pass

        monthly_rsp = {}
        now = datetime.now()
        device_id = device.device_id
        start_month = now.replace(
            day=1, hour=0, minute=0, second=0
        )
        final_month = now
        types = ['a', 'b', 'c', 'd']
        for pkg_type in types:
            type_name = get_name(pkg_type)
            if type_name:
                type_count = mongo_db.PackageModel.objects(
                    package_type=pkg_type,
                    device_id=device_id,
                    time__gte=start_month, time__lte=final_month).count()
                monthly_rsp[type_name] = type_count
        return monthly_rsp

    def get(self, request):
        rsp = {}
        client = self.request.user.client
        devices = client.get_devices()
        for device in devices:
            rsp.update(self.montly_prod(device))
        # rsp = {self.montly_prod(device) for device in devices}
        print(type(rsp))
        print(rsp)
        return JsonResponse(rsp)


class InfoWeeklyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def weekly_prod(self, device):
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
        types = ['a', 'b', 'c', 'd']
        while start_week.weekday() <= final_week.weekday():
            weekly_rsp[start_week.weekday()] = {}

            for pkg_type in types:
                type_name = get_name(pkg_type)
                final_day = start_week.replace(hour=23, minute=59, second=59)
                if type_name:
                    type_count = mongo_db.PackageModel.objects(
                        package_type=pkg_type, device_id=device_id,
                        time__gte=start_week, time__lte=final_day
                    ).count()
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
            # rsp.update(self.weekly_prod(device))
            print(rsp)
            # rsp[device.name] = self.weekly_prod(device)
        return JsonResponse(rsp)
