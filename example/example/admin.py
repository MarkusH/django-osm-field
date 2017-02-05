from django.contrib import admin

from .models import ExampleModel


class ExampleAdmin(admin.ModelAdmin):
    pass


admin.site.register(ExampleModel, ExampleAdmin)
