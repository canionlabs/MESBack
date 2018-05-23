from django.conf.urls import url
from rest_framework_jwt import views as jwt_views
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.api.views import CardsView


app_name = 'api'

urlpatterns = [
    url(r'^auth/token/$', jwt_views.obtain_jwt_token),
    url(r'^auth/token-refresh/$', jwt_views.refresh_jwt_token),
    url(r'^auth/token-verify/$', jwt_views.verify_jwt_token),

    url(r'^cards/$', CardsView.as_view(
        authentication_classes=[JSONWebTokenAuthentication])),
]
