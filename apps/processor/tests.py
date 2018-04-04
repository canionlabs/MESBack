from django.test import TestCase
from django.urls import reverse

from datetime import datetime
import requests
import json


class ProcessorTest(TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/receiver/v1/tubo/'
        self.gateway_data = {
            'topic': 'canionlabs/tubo/',
            'weight': '2',
            'created': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        }

    def test_save_request(self):
        response = requests.post(self.url, data=json.dumps(self.gateway_data))
        self.assertEqual(response.status_code, 200)
