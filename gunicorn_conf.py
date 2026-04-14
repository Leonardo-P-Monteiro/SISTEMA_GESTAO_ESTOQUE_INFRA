import multiprocessing

# 1️⃣ CONFIGURAÇÕES DE REDE
# Ponha no Nginx esse "proxy_pass http://unix:/run/gunicorn.sock;" e aqui
# esse trecho ==> bind = "unix:/run/gunicorn.sock"
# Isso vai implementar o uso de socket UNIX ao invés da conexão TCP/IP
bind = "0.0.0.0:8000"

# 2️⃣ GERENCIAMENTO DE PROCESSOS E WORKERS
cores = multiprocessing.cpu_count()
workers = (2 * cores) + 1

# 3️⃣ TIPO DE WORKER E CONCORRÊNCIA
worker_class = "sync"
threads = 2

# 4️⃣ Timeout e Ciclo de Vida
timeout = 120
max_requests = 1000
max_requests_jitter = 50

# 6️⃣ Logs
accesslog = "-"
errorlog = "-"
loglevel = "info"
