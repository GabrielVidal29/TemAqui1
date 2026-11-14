# ---------- Etapa 1: build do site (Vue + Vite) ----------
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# ---------- Etapa 2: servidor de produção (nginx) ----------
FROM nginx:1.27-alpine

# Porta do nginx (o Render define PORT; no docker-compose usamos 8080)
ENV PORT=8080 \
    API_BASE_URL=http://localhost:8000/api

# Configuração do nginx com a porta vinda de $PORT (o nginx processa /etc/nginx/templates na inicialização)
COPY docker/nginx.conf.template /etc/nginx/templates/default.conf.template

# Gera /config.js com o endereço da API na hora em que o container sobe
COPY docker/40-temaqui-config.sh /docker-entrypoint.d/40-temaqui-config.sh
RUN sed -i 's/\r$//' /docker-entrypoint.d/40-temaqui-config.sh \
    && chmod +x /docker-entrypoint.d/40-temaqui-config.sh

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080
