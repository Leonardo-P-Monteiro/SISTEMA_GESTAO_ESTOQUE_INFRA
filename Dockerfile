# ==============================================================================
# ⚠️ IMAGEM BASE
# A tag "FROM" é sempre a primeira instrução de um Dockerfile. Ela indica 
# qual imagem base, já pronta, será o ponto de partida para construirmos a nossa.
# ==============================================================================
# "python:3.12-slim" indica que queremos o Python 3.12 instalado sobre uma 
# versão minimalista do Debian Linux ("slim"), economizando centenas de megabytes.
FROM python:3.12-slim

# ==============================================================================
# ℹ️ METADADOS
# A tag "LABEL" adiciona metadados (informações chave=valor) à imagem final. 
# Servem para documentação, auditoria e indexação, não afetando a execução do código.
# ==============================================================================
LABEL owner="Leonardo P Monteiro"
LABEL maintainer="dev.pmonteiro@gmail.com"
LABEL version="1.0"
LABEL description="Project to practice my skills on infraestructure. On this project i implemented Nginx, Gunicorn and Docker sistem."

# ==============================================================================
# ⚙️ VARIÁVEIS DE AMBIENTE
# A tag "ENV" define variáveis de ambiente permanentes no sistema operacional do 
# container. Elas estarão disponíveis tanto no momento do build quanto na execução.
# ==============================================================================
# "PYTHONDONTWRITEBYTECODE=1" impede o Python de criar arquivos .pyc no disco.
# "PYTHONUNBUFFERED=1" obriga o Python a enviar os logs direto para o terminal 
# do Docker sem atrasos (sem buffer), essencial para ver erros em tempo real.
ENV PYTHONDONTWRITEBYTECODE=1 \ 
    PYTHONUNBUFFERED=1

# ==============================================================================
# 📁 DIRETÓRIO DE TRABALHO
# A tag "WORKDIR" cria uma pasta dentro do container (se não existir) e entra 
# nela. Funciona como um atalho para rodar "mkdir /SGE_INFRA && cd /SGE_INFRA".
# ==============================================================================
WORKDIR /SGE_INFRA

# ==============================================================================
# 🧑‍💻 CRIAÇÃO DO USUÁRIO
# A tag "RUN" executa comandos de terminal Linux DENTRO da imagem no momento da 
# construção (build). Tudo que o "RUN" faz fica salvo na estrutura final da imagem.
# ==============================================================================
RUN echo '🧑‍💻 Creating an user no root.'
# "addgroup" cria um grupo de sistema.
# "adduser" cria um usuário sem privilégios administrativos (segurança cibernética básica).
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser
RUN echo '✅ Concluded.'

# ==============================================================================
# 📦 INSTALAÇÃO DE DEPENDÊNCIAS DO SISTEMA
# Ainda usamos a tag "RUN" para instalar pacotes no nível do sistema (Debian).
# Nesse momento, ainda somos o usuário "root" (padrão inicial do Docker).
# ==============================================================================
RUN echo '🔁 Updating system packages.'
# "apt-get update" atualiza as listas de pacotes do Linux.
# "install -y --no-install-recommends" instala pacotes sem as "sugestões" extras, poupando espaço.
# "libpq-dev" e "gcc" são necessários para compilar o driver do Postgres (psycopg2) no Python.
# "rm -rf /var/lib/apt/lists/*" apaga o cache do instalador Linux para diminuir o tamanho final da imagem.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN echo '✅ Concluded.'

# ==============================================================================
# 📥 INSTALAÇÃO DAS LIBS PYTHON
# ==============================================================================
RUN echo '📥Installing dependencies of project.'
# A tag "COPY" copia arquivos do seu computador local para dentro da imagem Docker.
# Copiamos o requirements.txt ANTES de todo o código fonte para aproveitar o cache 
# de camadas do Docker (evita reinstalar tudo se você apenas mexer no código).
COPY requirements.txt /SGE_INFRA/

# Usamos o "RUN" para atualizar o pip e instalar as bibliotecas do projeto.
# "--no-cache-dir" diz ao pip para não salvar o cache de download, economizando espaço.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
RUN echo '✅ Concluded.'

# ==============================================================================
# ↔️ TRANSFERÊNCIA DO CÓDIGO FONTE
# ==============================================================================
RUN echo '↔️Coping all of directory to into of container.'
# Aqui a tag "COPY" pega todo o restante do seu código (ponto atual ".") e 
# manda para o diretório de trabalho definido no WORKDIR.
COPY . /SGE_INFRA/
RUN echo '✅ Concluded.'

# ==============================================================================
# 🚨 AJUSTE DE PERMISSÕES
# ==============================================================================
RUN echo '🔁Transfer of ownership between users.'
# Como o comando COPY padrão copia os arquivos como pertencentes ao usuário "root",
# usamos o "RUN" com "chown" para transferir a propriedade de toda a pasta /SGE_INFRA
# para o nosso usuário recém-criado, garantindo que ele consiga ler e escrever lá.
RUN chown -R appuser:appgroup /SGE_INFRA
RUN echo '✅ Concluded.'

# ==============================================================================
# 👥 TROCA DE CONTEXTO / USUÁRIO
# A tag "USER" muda a identidade ativa no sistema operacional.
# É uma barreira de segurança vital: se o container for hackeado, o invasor 
# não terá acesso "root" ao ambiente Linux.
# ==============================================================================
RUN echo '👥Changing of users.'
# A partir desta linha, perdemos os poderes de administrador (root). 
# Qualquer "RUN", "CMD" ou "ENTRYPOINT" rodará como 'appuser'.
USER appuser
RUN echo '✅ Concluded.'

# ==============================================================================
# 🌐 CONFIGURAÇÃO DE REDE
# A tag "EXPOSE" funciona estritamente como documentação dentro do Dockerfile.
# ==============================================================================
# EXPOSE informa a outros desenvolvedores e ao Docker (para alguns roteamentos dinâmicos)
# que a aplicação de dentro do container vai estar "escutando" tráfego na porta 8000.
# IMPORTANTE: Ela não publica/abre a porta para o mundo exterior (quem faz isso
# é a tag 'ports' lá no arquivo docker-compose.yml).
EXPOSE 8000

# ==============================================================================
# 🏁 COMANDO FINAL
# Você decidiu inteligentemente passar os comandos de execução no Docker Compose
# (via tag "command"). Por isso, este Dockerfile está focado apenas na construção 
# da infraestrutura do casulo.
# ==============================================================================