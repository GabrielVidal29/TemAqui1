# 🛍️ TemAqui

> **Descoberta de produtos, comparação de ofertas e navegação indoor integradas para shopping centers.**

O **TemAqui** é uma plataforma digital desenvolvida no contexto do **HACKARUN (Hackathon — Engenharia de Software)**. A solução centraliza informações sobre produtos, preços, promoções, lojas e rotas internas para aprimorar a experiência presencial de compra dos consumidores, tendo como referência inicial o **Capim Dourado Shopping** (Palmas – TO).

---

## 🎯 Problema e Proposta de Valor

Em shopping centers, encontrar um produto específico, comparar preços entre diferentes lojas e localizar estabelecimentos em vários pavimentos exige deslocamento desnecessário e consulta a fontes dispersas. 

Diferentemente de um e-commerce (o sistema não realiza vendas ou pagamentos online), o **TemAqui** atua como um guia presencial integrado, conectando a pesquisa de ofertas à localização física exata das lojas por meio de três interfaces sincronizadas:

* **Totem Interativo (`1080 × 1920 px`)**: Interface vertical sensível ao toque instalada em pontos fixos do shopping para busca rápida, consulta de mapas e traçado de rotas[cite: 1].
* **Site Mobile Responsivo (`390 × 844 px`)**: Acesso direto pelo navegador do celular (sem necessidade de instalar aplicativo ou criar conta para consultas)[cite: 1], permitindo continuar uma pesquisa ou rota iniciada no totem via **QR Code**[cite: 1].
* **Painel do Lojista (`1440 × 900 px`)**: Interface web administrativa para que cada loja cadastre produtos, atualize preços, gerencie promoções e controle a disponibilidade dos itens de forma descentralizada[cite: 1].

---

## ✨ Funcionalidades

### Escopo do MVP
* **Vitrine e Busca de Produtos**: Exibição de ofertas cadastradas com pesquisa por nome/palavra-chave e filtros por categoria, preço, loja e pavimento[cite: 1].
* **Detalhes e Comparação**: Visualização de descrição, preço, loja, data/hora da última atualização e comparação de ofertas entre estabelecimentos[cite: 1].
* **Mapa Interno e Rotas Demonstrativas**: Planta ilustrativa dos pavimentos com localização de lojas, pontos de interesse (banheiros, elevadores, saídas, praça de alimentação) e traçado de rota a partir da posição fixa do totem[cite: 1].
* **Continuidade via QR Code**: Transferência da pesquisa ou rota do totem para o dispositivo móvel do consumidor[cite: 1].
* **Gestão Comercial (Lojista)**: Cadastro de produtos, edição de valores/promoções e ativação ou pausa de exibição na vitrine[cite: 1].

### Evoluções Previstas (Roadmap)
* Busca avançada por intenção/ocasião (ex.: *"presente para minha mãe"*)[cite: 1].
* Navegação indoor com acompanhamento em tempo real[cite: 1].
* Painel analítico com métricas de desempenho e interações para lojistas[cite: 1].
* Autenticação de consumidores e gamificação (validação de NFC-e e roleta de recompensas)[cite: 1].
* Painel de administração geral do shopping e expansão multi-shopping[cite: 1].

---

## 🛠️ Arquitetura e Tecnologias

O sistema é estruturado em arquitetura de três camadas (apresentação, aplicação e persistência)[cite: 1] organizada em um **Monorepo** conteinerizado[cite: 1]:

| Camada / Área | Tecnologia | Aplicação |
| :--- | :--- | :--- |
| **Frontend** | **Vue.js 3** | Interfaces do Totem, Site Mobile e Painel do Lojista[cite: 1]. |
| **Backend** | **Python + FastAPI** | API RESTful para regras de negócio, autenticação e consultas[cite: 1]. |
| **Banco de Dados** | **PostgreSQL + SQLAlchemy 2** | Persistência relacional e mapeamento objeto-relacional (ORM)[cite: 1]. |
| **Infraestrutura** | **Docker + Docker Compose** | Padronização, isolamento e orquestração local dos serviços[cite: 1]. |
| **Design & Versionamento** | **Figma, Git, GitHub** | Prototipação das interfaces e controle de versão[cite: 1]. |

### Entidades Principais (Modelagem)
`Loja` • `Produto` • `Promoção` • `Lojista` • `Totem` • `Ponto de Interesse` • `Rota`[cite: 1]

---

## 🚀 Como Executar o Projeto

A aplicação foi projetada para ser orquestrada via **Docker Compose** a partir da raiz do repositório, subindo simultaneamente os contêineres do **Frontend (Vue.js)**, **Backend (FastAPI)** e **Banco de Dados (PostgreSQL)** em uma rede interna dedicada[cite: 1].

### Pré-requisitos
* [Docker](https://www.docker.com/)[cite: 1]
* [Docker Compose](https://docs.docker.com/compose/)[cite: 1]
* [Git](https://git-scm.com/)[cite: 1]
