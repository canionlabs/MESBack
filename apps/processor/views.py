from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import IceProduction

import json


class ReceiverView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ReceiverView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        # Log register
        new_register = IceProduction.simple_save(data)
        return HttpResponse('ok')
