from django.contrib import admin
from .models import CarouselBanner

@admin.register(CarouselBanner)
class CarouselBannerAdmin(admin.ModelAdmin):
    list_display = ('promotion', 'ordem', 'created_at')  # campos existentes
    list_filter = ('ordem', 'created_at')                # campos existentes
    search_fields = ('promotion',)
