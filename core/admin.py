from django.contrib import admin
from core.models import Tenant, Hospital, Branch, Department, AuditEvent

admin.site.register(Tenant)
admin.site.register(Hospital)
admin.site.register(Branch)
admin.site.register(Department)
admin.site.register(AuditEvent)
