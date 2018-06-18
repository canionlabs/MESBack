from django.conf.urls import url
from rest_framework_jwt import views as jwt_views
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_swagger.views import get_swagger_view

from apps.api.views import dashboard as dash_views
from apps.api.views import chatbot as chat_views
from apps.api.views import receiver as rec_views


schema_view = get_swagger_view(title='API Documentation')

app_name = 'api'

urlpatterns = [

    # Swagger
    url(r'^docs/$', schema_view),

    # JWT Auth
    url(r'^auth/token/$', jwt_views.obtain_jwt_token),
    url(r'^auth/token-refresh/$', jwt_views.refresh_jwt_token),
    url(r'^auth/token-verify/$', jwt_views.verify_jwt_token),

    # Dashboard Endpoints
    url(r'^info/cards/$', dash_views.CardsView.as_view(
        authentication_classes=[JSONWebTokenAuthentication])),
    url(r'^info/monthly/$', dash_views.InfoMonthlyView.as_view(
        authentication_classes=[JSONWebTokenAuthentication])),
    url(r'^info/weekly/$', dash_views.InfoWeeklyView.as_view(
        authentication_classes=[JSONWebTokenAuthentication])),
    url(r'^info/daily/$', dash_views.InfoDailyView.as_view(
        authentication_classes=[JSONWebTokenAuthentication])),

    # ChatBot Endpoints
    url(r'^chatbot/check/$', chat_views.CheckView.as_view()),
    url(r'^chatbot/daily/$', chat_views.DailyView.as_view()),
    url(r'^chatbot/weekly/$', chat_views.WeeklyView.as_view()),

    # Receiver Endpoints
    url(r'^receiver/$', rec_views.ReceiverView.as_view()),
]
