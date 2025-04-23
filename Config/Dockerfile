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

# Pour Postgres
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# App setup
WORKDIR /app
COPY app/ /app/
RUN pip install fastapi uvicorn sqlmodel pyodbc bcrypt

# Script d'attente DB
COPY wait-for-sql.sh /wait-for-sql.sh
RUN chmod +x /wait-for-sql.sh

# Point d’entrée
CMD ["/wait-for-sql.sh"]
