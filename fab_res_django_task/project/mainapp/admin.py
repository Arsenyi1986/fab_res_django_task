from django.contrib import admin
from . import models


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(CustomModelAdmin, self).__init__(model, admin_site)


@admin.register(models.Client)
class ClientAdmin(CustomModelAdmin):
    search_fields = "unique_id", "phone_number"
    list_filter = "tag", "operator_code", "time_zone"


@admin.register(models.Mailing)
class MailingAdmin(CustomModelAdmin):
    search_fields = "unique_id", "text"
    list_filter = "launch_date_time", "client_filter", "end_date_time"


@admin.register(models.Message)
class MessageAdmin(CustomModelAdmin):
    search_fields = ("unique_id",)
    list_filter = "create_date_time", "status"
