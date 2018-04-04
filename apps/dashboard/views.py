from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.processor.models import IceProduction

from prettyconf import config
import requests

from datetime import datetime, timedelta
import json

import locale


@method_decorator(login_required(login_url="/login"), name='dispatch')
class DashboardCuboView(TemplateView):
    template_name = "dashboard-cubo.html"

    def get_week_production(self, week_2={}, week_4={}):
        one_day = timedelta(days=1)
        datetime_object = datetime.now()

        def start_week(select_date=datetime_object):
            while select_date.strftime("%a") != 'Sun':
                select_date = select_date - one_day
            return select_date

        def final_week(select_date=datetime_object):
            one_day = timedelta(days=1)
            while select_date.strftime("%a") != 'Sat':
                select_date = select_date + one_day
            return select_date

        start_week = start_week()
        final_week = final_week()
        key = 0
        while start_week.strftime("%a") != 'Sat':
            fmt_date = start_week.strftime('%Y-%m-%d')
            week_2[key] = IceProduction.objects.filter(
                date=fmt_date, weight='2'
            )
            week_4[key] = IceProduction.objects.filter(
                date=fmt_date, weight='4'
            )
            start_week = start_week + one_day
            key += 1
        fmt_date = final_week.strftime('%Y-%m-%d')
        week_2[6] = IceProduction.objects.filter(
            date=fmt_date, weight='2'
        )
        week_4[6] = IceProduction.objects.filter(
            date=fmt_date, weight='4'
        )
        return week_2, week_4

    def get_diary_production(self, data_diary_2={}, data_diary_4={}):
        date = datetime.now().strftime('%Y-%m-%d')
        production_list = IceProduction.objects.filter(date=date)
        for hour in range(0, 23):
            data_diary_2[hour] = production_list.filter(
                hour__hour=hour, weight='2'
            )
            data_diary_4[hour] = production_list.filter(
                hour__hour=hour, weight='4'
            )
        return data_diary_2, data_diary_4

    def get_total_week_production(self, week_2, week_4):
        total = 0
        for day_week in range(0, 6):
            total_day = (len(week_2[day_week]) + len(week_4[day_week]))
            total += total_day
        return total

    def get_start_production(self):
        date = datetime.now().strftime('%Y-%m-%d')
        today_list = IceProduction.objects.filter(date=date).order_by('hour')
        if today_list.exists():
            return today_list.first().hour
        return '- - : - - : - -'

    def get_most_productive_day(self, week_2, week_4):
        total = 0
        day = 0
        days = [
            "Domingo", "Segunda", "Terça",
            "Quarta", "Quinta", "Sexta", "Sábado"
        ]
        for day_week in range(0, 6):
            total_day = (len(week_2[day_week]) + len(week_4[day_week]))
            if total < total_day:
                total = total_day
                day = day_week
        return days[day]

    def get_context_data(self, **kwargs):
        def sum_dict(dictionary):
            total = 0
            for k, i in dictionary.items():
                total += len(i)
            return total

        context = super().get_context_data(**kwargs)
        data_diary_2, data_diary_4 = self.get_diary_production()
        week_2, week_4 = self.get_week_production()
        context.update(dict(
            data_diary_2=data_diary_2,
            data_diary_4=data_diary_4,
            week_2=week_2,
            week_4=week_4,
            data_diary_sum=(sum_dict(data_diary_2) + sum_dict(data_diary_4)),
            most_productive_day=self.get_most_productive_day(week_2, week_4),
            total_week=self.get_total_week_production(week_2, week_4),
            start_diary_production=self.get_start_production(),
            range=range(0, 23), range_day=range(0, 7)
        ))
        return context


@method_decorator(login_required(login_url="/login"), name='dispatch')
class DashboardBarraView(TemplateView):
    template_name = "dashboard-barra.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
