from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, CarrinhoViewSet, PedidoItemViewSet, EntregaViewSet, PedidoReciboView
from django.urls import path

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet)
router.register(r'itens', PedidoItemViewSet)
router.register(r'entregas', EntregaViewSet)
router.register(r'carrinho', CarrinhoViewSet, basename="carrinho")

urlpatterns = router.urls
urlpatterns += [
    path('carrinho/checkout/', CarrinhoViewSet.as_view({'post': 'checkout'}), name='carrinho-checkout'),
    path('pedidos/<int:pk>/recibo/', PedidoReciboView.as_view(), name='pedido-recibo'),
]