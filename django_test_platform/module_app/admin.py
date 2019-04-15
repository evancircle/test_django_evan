from django.contrib import admin
from module_app.models import Module

# Register your models here.


class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name','describe','project','create_time']
    search_fields = ['name']
    list_filter = ['project']

admin.site.register(Module,ModuleAdmin)