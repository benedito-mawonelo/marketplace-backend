from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import CarouselBanner
from .serializers import CarouselBannerSerializer
from .permissions import IsAdminOrReadOnly

class CarouselAdminViewSet(viewsets.ModelViewSet):
    queryset = CarouselBanner.objects.all()
    serializer_class = CarouselBannerSerializer
    permission_classes = [IsAdminOrReadOnly]

class CarouselPublicViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CarouselBanner.objects.all()
    serializer_class = CarouselBannerSerializer
    permission_classes = [AllowAny]