from django.shortcuts import render
from django.views.generic import TemplateView


class ForgotPassword(TemplateView):
    template_name = 'auth/forgot-password.html'
