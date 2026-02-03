# Ativo Real - GeoPlatform 🌍

<p align="center">
  <strong>A tecnologia que conecta seu patrimônio à regularidade</strong>
</p>

<p align="center">
  <a href="https://gray-plant-08ef6cf0f.2.azurestaticapps.net">🌐 Demo Live</a> •
  <a href="#sobre">📋 Sobre</a> •
  <a href="#funcionalidades">✨ Funcionalidades</a> •
  <a href="#tecnologias">🛠️ Stack</a> •
  <a href="#status">📊 Status</a>
</p>

---

## 📋 Sobre

**Ativo Real** é uma plataforma completa de topografia e geoprocessamento para gestão de ativos rurais e urbanos. O sistema oferece ferramentas profissionais para topógrafos, proprietários e agricultores gerenciarem regularizações fundiárias, CAR (Cadastro Ambiental Rural) e certificações INCRA/SIGEF.

### 🎯 Perfis de Usuário

- **🔧 Topógrafo**: Ferramentas técnicas de desenho, medição e geração de relatórios NBR 13.133
- **🏠 Proprietário**: Acompanhamento da regularização de imóveis com validações automáticas
- **🚜 Agricultor**: Gestão de CAR, áreas produtivas e sobreposições ambientais

---

## ✨ Funcionalidades

### 🗺️ Mapa Interativo (OpenLayers 10.7.0)
- Basemaps road/satellite com alternância em tempo real
- Ferramentas de desenho: polígonos, círculos, linhas, marcadores
- Edição de vértices com snap automático
- Importação de camadas: KML, GeoJSON, CSV, TXT
- Cálculo automático de área, perímetro e azimutes
- Análise de sobreposições com SIGEF/INCRA/CAR

### 📐 Ferramentas Topográficas
- Estação total virtual para medições angulares
- Controle de precisão (3 casas decimais)
- Conversão de coordenadas (UTM ↔ Lat/Lon)
- Geração de memorial descritivo automático

### 💰 Pagamentos (InfinitePay)
- Gateway integrado: PIX, Cartão, Boleto
- Taxa de 0.99% por transação
- Webhook para confirmação automática

### 🤖 AI Assistant
- Chatbot com contexto técnico (área, coordenadas, SIGEF)
- Interface glassmorphism
- Placeholder para integração com LLM

### 📊 Relatórios Técnicos
- Exportação PDF, KML, JSON
- Layout NBR 13.133 compliant
- Tabela de coordenadas com numeração automática
- Análise de sobreposições com órgãos oficiais

---

## 🛠️ Tecnologias

### Frontend
- **React 19.0.0** - Library UI
- **TypeScript 5.6.2** - Type safety
- **Vite 5.4.21** - Build tool
- **OpenLayers 10.7.0** - Mapa interativo
- **Tailwind CSS** - Estilização

### Backend (Azure Functions - Python 3.11)
- **12 REST endpoints** - Complete API
- **JWT Authentication** - Secure access
- **PostGIS Integration** - Spatial operations
- **Azure Storage** - Arquivos e blobs

### Infraestrutura (Azure)
- **Static Web Apps** - Hosting frontend
- **Function App** - Serverless backend
- **PostgreSQL + PostGIS** - Database
- **Bicep** - Infrastructure as Code

---

## 📊 Status

| Componente | Status | Descrição |
|------------|--------|-----------|
| Backend | 90% | 12 endpoints REST com JWT e PostGIS |
| Frontend | 85% | Single-page client e dashboards |
| Database | 100% | Schema completo com PostGIS |

---

## 🏗️ Arquitetura

**⚠️ IMPORTANTE**: Este projeto é 100% Cloud-Native. Não usa localhost.

- **Frontend**: React + TypeScript + Ant Design + OpenLayers → Azure Static Web Apps
- **Backend**: Python Serverless (Azure Functions v2)
- **Database**: PostgreSQL + PostGIS (Azure Database for PostgreSQL)

### 🛡️ Diferenciais

1. **Validação Geométrica no Backend**: Matemática pesada (Shapely + GeoAlchemy2)
2. **Topologia Rígida**: Constraints `CHECK(ST_IsValid(geom))`
3. **Single-Page Application**: Cliente vê tudo em 1 página só

---

## 📂 Estrutura

```
/
├── novo-projeto/
│   ├── ativo-real/              ✅ FRONTEND OFICIAL (React + TS)
│   ├── backend/                 ✅ BACKEND OFICIAL (Azure Functions)
│   ├── database/                ✅ SQL SCRIPTS (PostGIS)
│   └── README.md                📖 Documentação técnica
├── index.html                   🌐 Project Website
├── vercel.json                  ⚙️  Vercel Configuration
└── README.md                    📖 Este arquivo
```

---

## 🚀 Deploy

### Website (Vercel)
O website do projeto está hospedado no Vercel e é automaticamente deployado a cada push na branch principal.

### Aplicação (Azure)
A aplicação principal está deployada no Azure Static Web Apps:
- **URL**: https://gray-plant-08ef6cf0f.2.azurestaticapps.net
- **Deploy**: Automático via GitHub Actions

---

## 📚 Documentação

Para documentação técnica completa, consulte:
- [novo-projeto/README.md](novo-projeto/README.md) - Documentação técnica
- [novo-projeto/ARCHITECTURE_SPECS.md](novo-projeto/ARCHITECTURE_SPECS.md) - Especificações de arquitetura
- [novo-projeto/PROJECT_STATUS.md](novo-projeto/PROJECT_STATUS.md) - Status do projeto

---

## 🔒 Segurança

- **HTTPS Obrigatório** em produção
- **CORS** configurado para domínio específico
- **Environment Variables** para chaves sensíveis
- **JWT Authentication** para acesso seguro
- **Rate Limiting** nos endpoints da API

---

## 📝 Licença

© 2026 Ativo Real - Todos os direitos reservados.

**Logo e Marca Registrada**: A logo "Ativo Real" e todos os elementos visuais associados são propriedade exclusiva. O uso não autorizado está sujeito a penalidades legais.

---

<p align="center">
  Desenvolvido com ❤️ pela equipe <strong>Ativo Real</strong>
</p>

<p align="center">
  <a href="https://gray-plant-08ef6cf0f.2.azurestaticapps.net">🌐 Visite a aplicação</a>
</p>
