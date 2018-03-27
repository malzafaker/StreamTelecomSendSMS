from django.contrib import admin
from apps.sms.models import SMS


@admin.register(SMS)
class SMSAdmin(admin.ModelAdmin):
    list_display = ('phone', 'sms_id', 'status', 'created')

    readonly_fields = ('phone', 'sms_id', 'status', 'created')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(SMSAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
