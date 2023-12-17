from django.contrib import admin
from . import models


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(CustomModelAdmin, self).__init__(model, admin_site)


@admin.register(models.Client)
class ClientAdmin(CustomModelAdmin):
    search_fields = ("id", "phone_number")
    list_filter = ("tag", "operator_code", "time_zone")
    list_display = ("id", "phone_number", "operator_code", "tag", "time_zone")

    fieldsets = (
        (None, {
            'fields': ('phone_number', 'operator_code', 'tag', 'time_zone')
        }),
    )


@admin.register(models.Mailing)
class MailingAdmin(CustomModelAdmin):
    search_fields = ("id", "text")
    list_filter = ("launch_date_time", "client_filter", "end_date_time")
    list_display = ("id", "launch_date_time", "text", "end_date_time")

    fieldsets = (
        (None, {
            'fields': ('launch_date_time', 'text', 'client_filter', 'end_date_time')
        }),
    )


@admin.register(models.Message)
class MessageAdmin(CustomModelAdmin):
    search_fields = ("id",)
    list_filter = ("create_date_time", "status")
    list_display = ("id", "create_date_time", "status", "mailing_id", "client_id")

    fieldsets = (
        (None, {
            'fields': ('create_date_time', 'status', 'mailing_id', 'client_id')
        }),
    )
