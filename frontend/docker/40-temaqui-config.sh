#!/bin/sh
# Executado pelo nginx ao subir o container: grava o endereço da API em /config.js.
# Assim a mesma imagem funciona no docker-compose (localhost) e no Render (URL pública da API).
set -e

API="${API_BASE_URL:-http://localhost:8000/api}"
# Endereço do site aberto pelo QR Code no celular (vazio = mesmo domínio do totem)
SITE="${PUBLIC_SITE_URL:-}"

cat > /usr/share/nginx/html/config.js <<EOF
window.__TEMAQUI_CONFIG__ = { API_BASE_URL: "${API}", PUBLIC_SITE_URL: "${SITE}" };
EOF

echo "TemAqui: API_BASE_URL=${API} PUBLIC_SITE_URL=${SITE:-mesmo dominio}"
