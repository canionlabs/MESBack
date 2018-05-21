from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.core.api_gateway import mount_query


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        client = self.request.user.client
        devices = client.get_devices()
        cards = {}
        for d in devices:
            cards[d.name] = mount_query(d.device_id)
            cards[d.name]['device_id'] = d.device_id
        # cards = {d.name: mount_query(d.device_id) for d in devices}
        context['cards'] = cards
        context['devices'] = devices
        return self.render_to_response(context)
