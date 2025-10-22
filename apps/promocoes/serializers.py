from rest_framework import serializers
from .models import CarouselBanner

class CarouselBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselBanner
        fields = ['id', 'image', 'promotion', 'ordem', 'created_at']