from django.conf.urls import url

from apps.dashboard.views import DashboardCuboView, DashboardBarraView

app_name = 'dashboard'

urlpatterns = [
    url(r'^$', DashboardCuboView.as_view(), name='cubo'),
    url(r'^barra/$', DashboardBarraView.as_view(), name='barra'),
]
