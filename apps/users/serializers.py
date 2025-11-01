from rest_framework import serializers
from .models import User, ClienteEmpresa, Socio


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # Do not allow client to choose role during registration; server enforces default CLIENTE
        fields = ['id', 'nome', 'email', 'telefone', 'password', 'role']
        read_only_fields = ['role']

    def create(self, validated_data):
        password = validated_data.pop("password")
        # Force default role CLIENTE regardless of input
        validated_data['role'] = 'CLIENTE'
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class ClienteEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteEmpresa
        fields = '__all__'

class SocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socio
        fields = '__all__'
