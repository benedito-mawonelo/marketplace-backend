from rest_framework import serializers
from .models import User, ClienteEmpresa, Socio


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'nome', 'email', 'telefone', 'role', 'password']

    def create(self, validated_data):
        password = validated_data.pop("password")
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
        fields = ['id','user','endereco','foto_perfil','bi_frente','bi_verso','dados_pagamento','status','codigo_socio']
        read_only_fields = ['status','codigo_socio','user']

class SocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socio
        fields = '__all__'
