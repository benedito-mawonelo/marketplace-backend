from rest_framework.routers import DefaultRouter
from .views import (
    ProdutoViewSet, ProdutoAtributoViewSet, ProdutoImagemViewSet,
    ProdutoVideoViewSet, CategoriaViewSet
)

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'atributos', ProdutoAtributoViewSet)
router.register(r'imagens', ProdutoImagemViewSet)
router.register(r'videos', ProdutoVideoViewSet)
router.register(r'categorias', CategoriaViewSet)

urlpatterns = router.urls
