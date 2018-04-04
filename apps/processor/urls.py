from django.conf.urls import url

from apps.processor.views import ReceiverView

app_name = 'receiver'

urlpatterns = [
    url(r'^v1/tubo/$', ReceiverView.as_view(), name='receiver'),
]
