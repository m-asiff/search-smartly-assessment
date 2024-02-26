from django.contrib import admin
from .models import Poi, Category


admin.site.register(Category)


@admin.register(Poi)
class POITable(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "external_id",
        "category",
        "avg_rating",
    )
    search_fields = ("id", "external_id")
    list_filter = ("category",)
