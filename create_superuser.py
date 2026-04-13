import os

import django
from django.contrib.auth import get_user_model

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "app.settings",
)  # Confirme se 'app' é o nome da sua pasta de settings
django.setup()

User = get_user_model()
username = 'admin'
password = 'admin'  # noqa: S105

if User.objects.filter(username=username).exists():
    print("Superusuário já existe.")
elif username and password:
    User.objects.create_superuser(username=username, password=password) # type: ignore  # noqa: PGH003
    print("Superusuário criado com sucesso!")
else:
    print("Variáveis de ambiente do superusuário não configuradas.")
