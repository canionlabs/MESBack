from django.conf.urls import url

from apps.dashboard.views import HomeView


app_name = 'dashboard'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home')
    # url(r'', include('apps.dashboard.urls', namespace='dashboard')),
    # url(r'^api/', include('apps.api.urls')),
]
