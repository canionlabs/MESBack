from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from apps.processor.models import IceProduction
from apps.api.serializers import IceProductionSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class ProductionView(viewsets.ReadOnlyModelViewSet):
    '''
    List and Retrieve IceProduction objects
    '''
    queryset = IceProduction.objects.all()
    serializer_class = IceProductionSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):

        def filter_queryset(query, parameters):
            dict_items = parameters.items()
            clear_filter = dict()
            for key, value in dict_items:
                if value:
                    clear_filter[key] = value
            return query.filter(**clear_filter).order_by('-hour')

        queryset = IceProduction.objects.all()
        parameters = dict()
        parameters['weight'] = self.request.query_params.get('weight', None)
        parameters['ice_type'] = self.request.query_params.get('type', None)
        parameters['hour__hour'] = self.request.query_params.get('hour', None)
        parameters['date'] = self.request.query_params.get('date', None)
        return filter_queryset(queryset, parameters)
