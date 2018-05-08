from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from apps.customers.models import Organization, Client


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


class ClientInline(admin.StackedInline):
    model = Client


class CustomUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        UserAdmin.list_display = list(UserAdmin.list_display) + ['get_org']

    inlines = [
        ClientInline
    ]

    def get_org(self, obj):
        return obj.client.organization

    get_org.admin_order_field = 'organization'
    get_org.short_description = 'Organização'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
