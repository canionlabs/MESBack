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
        UserAdmin.list_display = list(UserAdmin.list_display)

    inlines = [
        ClientInline
    ]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
