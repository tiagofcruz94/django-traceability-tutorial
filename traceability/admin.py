from django.contrib import admin
from django.utils.formats import number_format

from .models import Animal, Carcass, DeboningLot


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = [
        "identification_number",
        "breed",
        "sex",
        "live_weight",
        "received_at",
    ]
    list_filter = ["sex", "breed"]
    search_fields = ["identification_number"]


@admin.register(Carcass)
class CarcassAdmin(admin.ModelAdmin):
    list_display = [
        "slaughter_number",
        "animal",
        "slaughtered_at",
        "hot_weight",
        "yield_display",
        "lot",
    ]
    list_filter = ["lot"]

    @admin.display(description="rendimento (%)")
    def yield_display(self, obj):
        """Yield with one decimal; the raw method would show every decimal place."""
        value = obj.carcass_yield()
        if value is None:
            return "-"
        return number_format(value, 1)


@admin.register(DeboningLot)
class DeboningLotAdmin(admin.ModelAdmin):
    list_display = ["lot_number", "created_at", "carcass_count"]

    @admin.display(description="n.º de carcaças")
    def carcass_count(self, obj):
        return obj.carcasses.count()
