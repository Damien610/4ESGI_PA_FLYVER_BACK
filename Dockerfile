FROM --platform=linux/amd64 python:3.11-slim-bullseye

# Pré-reqs système
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        gnupg \
        unixodbc \
        unixodbc-dev \
        apt-transport-https \
        gcc \
        g++ \
        unzip \
        libssl-dev \
        libxml2 \
        libkrb5-3 \
        libcurl4 \
        netcat && \
    rm -rf /var/lib/apt/lists/*

# Microsoft ODBC Driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    echo "deb [arch=amd64] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*


# Dossier de travail de l'app
WORKDIR /app

# Copier requirements et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier toute l'app (y compris main.tf à la racine si présent)
COPY . .

# Copier le script d'entrée
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Le ENTRYPOINT est géré par docker-compose
