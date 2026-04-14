import os

import django
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

# Configuração do ambiente Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "app.settings",
)  # Confirme se 'app' é o nome da sua pasta de settings
django.setup()

User = get_user_model()
username = "admin"
password = "admin"  # noqa: S105

# 1. Validação inicial das variáveis
if not username or not password:
    print("🛑 ERRO: Variáveis de ambiente do superusuário não configuradas.")
else:
    # 2. Início do bloco atômico
    try:
        with transaction.atomic():
            # Verifica se o usuário já existe
            if User.objects.filter(username=username).exists():
                print("ℹ️ INFO: Superusuário já existe. Nenhuma ação necessária.")  # noqa: RUF001
            else:
                # Cria o superusuário caso não exista
                User.objects.create_superuser(username=username, password=password)  # type: ignore  # noqa: PGH003
                print("✅ SUCESSO: Superusuário criado com sucesso!")

    # 3. Tratamento de concorrência (Race Condition)
    except IntegrityError:
        print("⚠️ AVISO: O superusuário já foi criado por outro processo simultâneo.")
    except Exception as e:  # noqa: BLE001
        print(f"💥 ERRO CRÍTICO: Erro inesperado ao tentar criar o superusuário: {e}")
