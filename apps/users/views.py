from rest_framework import viewsets, generics, status
from .models import User, ClienteEmpresa, Socio
from .serializers import UserSerializer, ClienteEmpresaSerializer, SocioSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .auth_serializers import CustomTokenObtainPairSerializer

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def deactivate_account(self, request):
        """
        Desativa a conta do usuário logado
        """
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "Conta desativada com sucesso."}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def activate_account(self, request):
        """
        Reativa a conta do usuário logado
        """
        user = request.user
        user.is_active = True
        user.save()
        return Response({"message": "Conta reativada com sucesso."}, status=status.HTTP_200_OK)



class MeView(APIView):
    permission_classes = [IsAuthenticated]  # garante que só usuários logados acessam

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "nome": user.nome,
            "email": user.email,
            "telefone": user.telefone,
            "role": user.role
        }
        return Response(data)
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ClienteEmpresaViewSet(viewsets.ModelViewSet):
    queryset = ClienteEmpresa.objects.all()
    serializer_class = ClienteEmpresaSerializer

class SocioViewSet(viewsets.ModelViewSet):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
