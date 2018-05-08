from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

import requests


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        client = self.request.user.client
        context['devices'] = client.get_devices()
        # import pdb; pdb.set_trace()
        context['total_production'] = sum(
            [total.total_production for total in client.get_devices()]
        )
        # import pdb; pdb.set_trace()
        return self.render_to_response(context)
