<p align="center">
  <img src="public/logos/logo-oficial.png" alt="Logo Bem Real" width="320">
</p>

<h1 align="center">Bem Real - Ativo Real</h1>

<p align="center">
  <strong>A tecnologia que conecta seu patrimônio à regularidade.</strong>
</p>

<p align="center">
  <a href="https://gray-plant-08ef6cf0f.2.azurestaticapps.net">🌐 Demo Live</a> •
  <a href="#funcionalidades">📋 Funcionalidades</a> •
  <a href="#tecnologias">🛠️ Stack</a> •
  <a href="#como-rodar">🚀 Como Rodar</a> •
  <a href="#documentacao">📚 Documentação</a>
</p>

---

## 📋 Sobre o Projeto

**Bem Real - Ativo Real** é uma plataforma completa de **topografia e geoprocessamento** para gestão de ativos rurais e urbanos. O sistema oferece ferramentas profissionais para topógrafos, proprietários e agricultores gerenciarem regularizações fundiárias, CAR (Cadastro Ambiental Rural) e certificações INCRA/SIGEF.

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
- **39 ícones SVG profissionais** (Bronze #CD7F32, 2px stroke)
- Estação total virtual para medições angulares
- Controle de precisão (3 casas decimais)
- Conversão de coordenadas (UTM ↔ Lat/Lon)
- Geração de memorial descritivo automático

### 💰 Pagamentos (InfinitePay)
- Gateway integrado: PIX, Cartão, Boleto
- Taxa de 0.99% por transação
- Webhook para confirmação automática
- Modal de checkout responsivo

### 🤖 AI Assistant
- Chatbot com contexto técnico (área, coordenadas, SIGEF)
- Interface glassmorphism (Azul Marinho 90%)
- FAB button com pulse animation
- Placeholder para integração com LLM (OpenAI/Azure OpenAI)

### 📊 Relatórios Técnicos
- Exportação PDF, KML, JSON
- Layout NBR 13.133 compliant
- Tabela de coordenadas com numeração automática
- Análise de sobreposições com órgãos oficiais
- Assinatura digital (futuro)

---

## 🛠️ Tecnologias

### Frontend
- **React 19.0.0** - Library UI
- **TypeScript 5.6.2** - Type safety
- **Vite 5.4.21** - Build tool
- **OpenLayers 10.7.0** - Mapa interativo
- **Tailwind CSS** - Estilização

### Backend (Azure Functions - Python 3.11)
- **func-ativoreal-api** - 8 endpoints REST
- **Azure Storage** - Arquivos e blobs
- **Application Insights** - Logs e monitoramento
- **CORS** - Configurado para domínio de produção

### Infraestrutura (Azure)
- **Static Web Apps** - Hosting frontend
- **Function App** - Serverless backend
- **Storage Account** - Standard_LRS
- **Bicep** - Infrastructure as Code

### Design System
- **Cores Oficiais**:
  - Azul Marinho: `#001F3F`
  - Bronze Fosco: `#CD7F32`
  - Titânio Metálico: `#B0B0B0`
- **Tipografia**: Roboto Condensed, JetBrains Mono
- **Ícones**: 39 SVG customizados (2px stroke, round caps)

---

## 🚀 Como Rodar

### Pré-requisitos
- **Node.js 20+**
- **npm 10+**
- **Git**

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/ativo-real.git
cd ativo-real
```

### 2. Instale as dependências
```bash
npm install
```

### 3. Configure variáveis de ambiente
Crie `.env` na raiz:
```env
VITE_API_BASE=https://func-ativoreal-api.azurewebsites.net/api
VITE_AZURE_MAPS_KEY=sua-chave-azure-maps
INFINITEPAY_API_KEY=sua-chave-infinitepay-sandbox
```

### 4. Rode em desenvolvimento
```bash
npm run dev
```
Acesse: `http://localhost:5173`

### 5. Build de produção
```bash
npm run build
npm run preview
```

---

## 📦 Deploy

### Azure Static Web Apps (Automático)
```bash
# Build
npm run build

# Deploy
swa deploy ./dist \
  --app-name ativoreal-web-bfrrbwmkfi6xe \
  --resource-group rg-ativoreal-chile \
  --env production
```

**URL de Produção**: https://gray-plant-08ef6cf0f.2.azurestaticapps.net

### Build Stats
- **Bundle Total**: 768.67 KB (228.87 KB gzipped)
- **CSS**: 36.41 KB (8.28 KB gzipped)
- **Módulos**: 441 transformados
- **Tempo**: ~5s

---

## 📁 Estrutura do Projeto

```
ativo-real/
├── src/
│   ├── components/
│   │   ├── AIBotChat.tsx          # Chatbot AI (180 linhas)
│   │   ├── InfinitePayModal.tsx   # Gateway de pagamento
│   │   ├── ui/
│   │   │   ├── TopoIcon.tsx       # Wrapper de ícones (4 estados)
│   │   │   └── Button.tsx         # Componente base
│   │   └── Forms/                 # Formulários de cadastro
│   ├── pages/
│   │   └── LoginPage.tsx          # Landing page com logo oficial
│   ├── assets/icons/topography/
│   │   ├── 24px/                  # 35 ícones principais
│   │   ├── 32px/                  # 3 ícones CTA
│   │   └── 16px/                  # 1 ícone tiny
│   ├── GlobalMap.tsx              # Mapa OpenLayers (900+ linhas)
│   ├── DashboardTopografo.tsx     # Dashboard de projetos
│   └── App.tsx                    # Router principal
├── api/                           # Azure Functions (Python)
│   ├── function_app.py            # 8 endpoints REST
│   ├── infinitepay_payment.py     # Integração pagamentos
│   ├── ai_assistant.py            # Placeholder LLM
│   └── requirements.txt           # Dependências Python
├── public/logos/
│   ├── logo-oficial.png           # Logo única autorizada
│   ├── preview-oficial.html       # Showcase com restrições
│   └── *.svg                      # Variações de logo
├── infra/
│   ├── main.bicep                 # Azure infrastructure
│   └── main.parameters.json       # Parâmetros de deploy
└── docs/
    ├── GUIA_ESTILO_LOGO.md        # Brand guidelines
    ├── CHATBOT_AI_SPECS.md        # Specs do chatbot
    ├── GALERIA_COMPLETA_ICONES.md # 39 ícones documentados
    ├── RELATORIO_TOPOGRAFIA_SPECS.md # NBR 13.133
    └── INFINITEPAY_CONFIGURACAO_COMPLETA.md
```

---

## 📚 Documentação

### Guias Técnicos
- [🎨 Guia de Estilo da Logo](GUIA_ESTILO_LOGO.md) - Diretrizes oficiais da marca
- [🤖 Chatbot AI Specs](CHATBOT_AI_SPECS.md) - Design system e interações
- [📐 Relatórios Topográficos](RELATORIO_TOPOGRAFIA_SPECS.md) - NBR 13.133
- [🖼️ Galeria de Ícones](GALERIA_COMPLETA_ICONES.md) - 39 ícones documentados
- [💳 InfinitePay Setup](INFINITEPAY_CONFIGURACAO_COMPLETA.md) - Gateway de pagamento

### Design System
- **Paleta de Cores**: Azul Marinho (#001F3F), Bronze (#CD7F32), Titânio (#B0B0B0)
- **Logo Oficial**: Única versão autorizada (curvas topográficas 3D)
- **Restrições**: ❌ Sem alterações de cor, sombreamento, distorções
- **Tipografia**: Montserrat (300/700), Roboto Mono

### Preview da Logo
Acesse: `public/logos/preview-oficial.html`
- Showcase da logo oficial
- Paleta de cores
- Restrições de uso
- Contatos de suporte

---

## 🎨 Brand Identity

### Logo Oficial Bem Real
<p align="center">
  <img src="public/logos/logo-oficial.png" alt="Logo Oficial" width="256">
</p>

**Especificações:**
- **Aspect Ratio**: 1:1 (quadrado)
- **Cores**: Bronze Fosco (#CD7F32) + Azul Marinho (#001F3F)
- **Efeitos**: Curvas topográficas 3D com highlights metálicos
- **Fundo Obrigatório**: Azul Marinho (#001F3F)
- **Área de Respiro**: Mínimo 20% do tamanho

**⚠️ IMPORTANTE**: Esta é a **ÚNICA versão autorizada** do logotipo. Qualquer variação ou uso que não siga as especificações do [Guia de Estilo](GUIA_ESTILO_LOGO.md) é **PROIBIDO** sem aprovação formal.

---

## 🧪 Testes

### Executar testes
```bash
npm test
```

### Lint e formatação
```bash
npm run lint
```

---

## 🔒 Segurança

- **HTTPS Obrigatório** em produção
- **CORS** configurado para domínio específico
- **Environment Variables** para chaves sensíveis
- **Webhook Signature** para validação InfinitePay
- **Rate Limiting** nos endpoints da API

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -m 'feat: Adiciona nova funcionalidade'`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

**Padrão de Commits**: [Conventional Commits](https://www.conventionalcommits.org/)
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação (sem mudança de código)
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Tarefas de build/config

---

## 📞 Suporte

**Dúvidas sobre uso da logo:**  
📧 design@bemreal.com.br  
📞 +55 (11) 9xxxx-xxxx

**Suporte técnico:**  
📧 dev@bemreal.com.br

**Denúncia de uso indevido da marca:**  
📧 compliance@bemreal.com.br

---

## 📝 Licença

© 2026 Bem Real - Todos os direitos reservados.

**Logo e Marca Registrada**: A logo "Bem Real" e todos os elementos visuais associados são propriedade exclusiva da Bem Real. O uso não autorizado está sujeito a penalidades legais.

---

<p align="center">
  Desenvolvido com ❤️ pela equipe <strong>Bem Real</strong>
</p>

<p align="center">
  <a href="https://gray-plant-08ef6cf0f.2.azurestaticapps.net">🌐 Visite o site</a>
</p>
