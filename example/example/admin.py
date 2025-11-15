from __future__ import annotations

from django.contrib import admin

from .models import ExampleModel


@admin.register(ExampleModel)
class ExampleAdmin(admin.ModelAdmin):
    pass
