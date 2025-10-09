from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, CarrinhoViewSet, PedidoItemViewSet, EntregaViewSet

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet)
router.register(r'itens', PedidoItemViewSet)
router.register(r'entregas', EntregaViewSet)
router.register(r'carrinho', CarrinhoViewSet, basename="carrinho")

urlpatterns = router.urls
