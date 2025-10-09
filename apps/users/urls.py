from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import UserViewSet, ClienteEmpresaViewSet, SocioViewSet, CustomLoginView, RegisterView, MeView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clientes-empresa', ClienteEmpresaViewSet)
router.register(r'socios', SocioViewSet)

urlpatterns = router.urls  + [
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', MeView.as_view(), name='me'),

]
