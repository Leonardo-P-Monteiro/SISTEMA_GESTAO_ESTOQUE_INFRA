# ==============================================================================
# 🚀 CONFIGURAÇÃO DO GUNICORN (SGE)
# Este arquivo dita como o Gunicorn vai executar a sua aplicação Django.
# Ele controla quantos processos serão abertos, como eles lidam com a rede e
# como gerenciam a memória e os tempos de resposta.
# ==============================================================================

# O módulo "multiprocessing" é nativo do Python e serve para obtermos
# informações sobre o hardware do servidor/container onde o código está rodando.
import multiprocessing

# ==============================================================================
# 🌐 1. CONFIGURAÇÕES DE REDE
# ==============================================================================
# A variável "bind" define a interface de rede e a porta onde o Gunicorn vai
# "escutar" as requisições que chegam (normalmente repassadas pelo Nginx).
#
# NOTA SOBRE DOCKER VS MÁQUINA VIRTUAL CLÁSSICA:
# - Se o Nginx e o Gunicorn estivessem rodando no MESMO sistema operacional
#   diretamente, usaríamos um Unix Socket (ex: bind = "unix:/run/gunicorn.sock")
#   porque é ligeiramente mais rápido, pois pula a camada de rede do SO.
# - Como estamos usando DOCKER, o Nginx e o Gunicorn estão em containers
#   (máquinas) separados. Portanto, eles SÓ conseguem se comunicar via rede TCP/IP.
# O IP "0.0.0.0" manda o Gunicorn escutar em TODAS as interfaces de rede do container.
bind = "0.0.0.0:8000"

# ==============================================================================
# ⚙️ 2. GERENCIAMENTO DE PROCESSOS E WORKERS
# ==============================================================================
# A variável "cores" usa o módulo importado acima para descobrir quantos núcleos
# de CPU estão disponíveis no hardware hospedeiro do Docker.
cores = multiprocessing.cpu_count()

# A variável "workers" define a quantidade de processos (cópias da sua aplicação)
# que rodarão em paralelo para atender múltiplos usuários ao mesmo tempo.
#
# A FÓRMULA DE OURO DA DOCUMENTAÇÃO OFICIAL: (2 x Número de Núcleos) + 1.
# - Se o servidor tiver 2 núcleos, o cálculo é (2 * 2) + 1 = 5 workers.
# Isso garante que a CPU não fique ociosa enquanto um worker aguarda o banco de dados.
workers = (2 * cores) + 1

# ==============================================================================
# 🧵 3. TIPO DE WORKER E CONCORRÊNCIA
# ==============================================================================
# A variável "worker_class" define o modelo de execução dos processos filhos.
# "sync" é o modelo padrão e o mais seguro/fácil de configurar. Ele atende uma
# requisição por vez (por isso precisamos de múltiplos workers e threads).
worker_class = "sync"

# A variável "threads" adiciona uma camada de simultaneidade a cada worker.
# Se você tiver 5 workers e 2 threads, o Gunicorn poderá lidar com 10 requisições
# simultâneas de forma bastante eficiente, sem consumir tanta memória extra quanto
# consumiria criando mais workers.
threads = 2

# ==============================================================================
# ⏱️ 4. TIMEOUT E CICLO DE VIDA (Prevenção de Travamentos)
# ==============================================================================
# A variável "timeout" (em segundos) determina o tempo máximo que um worker pode
# ficar trabalhando em uma requisição. Se ultrapassar esse tempo (ex: um relatório
# muito pesado ou o banco de dados travou), o Gunicorn mata o worker travado
# e inicia um novo imediatamente para o site não cair.
timeout = 120

# A variável "max_requests" é uma estratégia de ouro contra vazamento de memória (Memory Leak).
# Ela obriga cada worker a "morrer" (reiniciar automaticamente) após processar
# exatamente 1000 requisições. Isso zera a memória RAM daquele processo.
max_requests = 1000

# A variável "max_requests_jitter" impede o "Efeito Manada" (Thundering Herd).
# Se todos os workers chegassem a 1000 requisições ao mesmo tempo, todos reiniciariam
# juntos, derrubando o site por alguns segundos. O jitter adiciona um número aleatório
# (até 50) no limite de cada worker. Um reiniciará com 1020, outro com 1045, etc.
max_requests_jitter = 50

# ==============================================================================
# 📊 5. LOGS (Auditoria e Observabilidade)
# ==============================================================================
# As variáveis de log dizem ao Gunicorn onde gravar o histórico de atividades.
# O valor "-" (traço) é uma diretiva vital em ambientes Docker.
# Ele diz ao Gunicorn para gravar os logs na "Saída Padrão" (stdout) em vez de
# num arquivo de texto físico. Assim, o próprio Docker captura os logs, e você
# pode lê-los facilmente digitando `docker logs SGE_WEB`.
accesslog = "-"  # Registra quem acessou qual página
errorlog = "-"  # Registra erros e falhas da aplicação (ex: Tracebacks do Django)

# A variável "loglevel" define o nível de detalhe dos logs gerais do Gunicorn.
# "info" é excelente para produção, pois registra inícios, paradas e reinícios
# de workers sem inundar o terminal com detalhes desnecessários de depuração (debug).
loglevel = "info"
