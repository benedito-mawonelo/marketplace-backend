# apps/users/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, telefone, nome, password=None, role="CLIENTE"):
        if not email:
            raise ValueError("Email obrigatório")
        user = self.model(
            email=self.normalize_email(email),
            telefone=telefone,
            nome=nome,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, telefone, nome, password):
        user = self.create_user(email, telefone, nome, password, role="ADMIN")
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("CLIENTE", "Cliente"),
        ("SOCIO", "Sócio"),
        ("ADMIN", "Admin"),
        ("EMPRESA", "Empresa"),
    ]
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="CLIENTE")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['telefone', 'nome']

    objects = UserManager()

    def __str__(self):
        return self.nome

    @property
    def is_staff(self):
        return self.is_admin


class ClienteEmpresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_empresa = models.CharField(max_length=255)
    nuit = models.CharField(max_length=50)
    endereco = models.TextField()


class Socio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    endereco = models.TextField()
    foto_perfil = models.URLField(blank=True, null=True)
    codigo_socio = models.CharField(max_length=50, unique=True)
    dados_pagamento = models.TextField()
