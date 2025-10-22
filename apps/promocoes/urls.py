from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarouselAdminViewSet, CarouselPublicViewSet

router_admin = DefaultRouter()
router_admin.register(r'carousel', CarouselAdminViewSet, basename='carousel-admin')

router_public = DefaultRouter()
router_public.register(r'carousel', CarouselPublicViewSet, basename='carousel-public')

urlpatterns = [
    path('promocoes/', include(router_admin.urls)),      # /api/promocoes/carousel/ (admin)
    path('public/', include(router_public.urls)),        # /api/public/carousel/ (public)
]