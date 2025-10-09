from rest_framework.routers import DefaultRouter
from .views import ComissaoViewSet

router = DefaultRouter()
router.register(r'comissoes', ComissaoViewSet)

urlpatterns = router.urls
