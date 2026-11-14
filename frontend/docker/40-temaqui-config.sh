#!/bin/sh
# Executado pelo nginx ao subir o container: grava o endereço da API em /config.js.
# Assim a mesma imagem funciona no docker-compose (localhost) e no Render (URL pública da API).
set -e

API="${API_BASE_URL:-http://localhost:8000/api}"

cat > /usr/share/nginx/html/config.js <<EOF
window.__TEMAQUI_CONFIG__ = { API_BASE_URL: "${API}" };
EOF

echo "TemAqui: API_BASE_URL=${API}"
