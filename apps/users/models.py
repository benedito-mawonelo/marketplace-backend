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
        user.is_superuser = True
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


def gerar_novo_codigo_socio():
    """
    Gera um novo código de sócio no formato 'M' + 4 dígitos (ex: M0001).
    """
    ultimo_socio = Socio.objects.all().order_by('id').last()
    
    if not ultimo_socio or not ultimo_socio.codigo_socio or not ultimo_socio.codigo_socio.startswith('M'):
        # Se não houver sócios ou o último código não estiver no formato esperado, começa do 1.
        novo_numero = 1
    else:
        try:
            # Extrai a parte numérica do código do último sócio e incrementa.
            ultimo_numero = int(ultimo_socio.codigo_socio[1:])
            novo_numero = ultimo_numero + 1
        except (ValueError, IndexError):
            # Fallback caso o código existente seja inválido.
            novo_numero = Socio.objects.count() + 1

    # Formata o novo código com 4 dígitos, preenchendo com zeros à esquerda.
    return f"M{novo_numero:04d}"


class Socio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    endereco = models.TextField()
    # Use TextField to allow storing base64 captured images if needed
    foto_perfil = models.TextField(blank=True, null=True)
    bi_frente = models.TextField(blank=True, null=True)
    bi_verso = models.TextField(blank=True, null=True)
    codigo_socio = models.CharField(max_length=5, unique=True, blank=True)
    dados_pagamento = models.TextField()

    def save(self, *args, **kwargs):
        if not self.codigo_socio:
            self.codigo_socio = gerar_novo_codigo_socio()
        super().save(*args, **kwargs)
