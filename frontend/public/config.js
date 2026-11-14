// Configuração em tempo de execução.
// Em desenvolvimento (npm run dev) fica vazia e o app usa VITE_API_BASE_URL ou http://localhost:8000/api.
// No container Docker este arquivo é recriado ao subir, com o valor da variável API_BASE_URL.
window.__TEMAQUI_CONFIG__ = window.__TEMAQUI_CONFIG__ || {}
