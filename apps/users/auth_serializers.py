from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Permite login tanto com email quanto com telefone
    """
    def validate(self, attrs):
        email_or_phone = attrs.get("email") or attrs.get("telefone")
        password = attrs.get("password")

        # Buscar usuário pelo email ou telefone
        try:
            user = User.objects.get(email=email_or_phone)
        except User.DoesNotExist:
            try:
                user = User.objects.get(telefone=email_or_phone)
            except User.DoesNotExist:
                raise serializers.ValidationError(_("Usuário não encontrado"))

        # Verificar senha
        if not user.check_password(password):
            raise serializers.ValidationError(_("Credenciais inválidas"))

        # **Proteção: verificar se a conta está ativa**
        if not user.is_active:
            raise serializers.ValidationError(_("Conta desativada. Entre em contato para reativar."))
        
        #TODO: Escrever logica para reactivar a conta por email enviando um link.

        # Gerar tokens
        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                "id": user.id,
                "nome": user.nome,
                "email": user.email,
                "telefone": user.telefone,
                "role": user.role
            }
        }
