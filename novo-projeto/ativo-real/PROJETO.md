# 🌱 Ativo Real

Plataforma de Gestão de Ativos Rurais e Urbanos com visualização de mapas interativos.

## 🚀 Tecnologias

- **React 19** + **TypeScript**
- **Vite** para build e desenvolvimento
- **Leaflet** para mapas interativos
- **React Leaflet** para integração com React
- **Vitest** para testes

## 📋 Funcionalidades

### ✨ Mapa Interativo
- Visualização de propriedades rurais e áreas urbanas
- Camadas customizáveis (marcadores, polígonos, círculos)
- Controle de visibilidade de camadas
- Popups informativos

### 🚜 Cadastro Rural (B2B)
- Registro de fazendas e propriedades rurais
- Gestão de áreas em hectares
- Cadastro de administrador

### 🏙️ Cadastro Urbano
- Ativação de contas urbanas
- Autenticação com CPF e data de nascimento
- Gestão de senhas

## 🛠️ Instalação

```bash
# Instalar dependências
npm install

# Rodar em desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview da build
npm run preview

# Rodar testes
npm test
```

## 📂 Estrutura do Projeto

```
src/
├── components/
│   └── Map/
│       ├── MapView.tsx         # Componente principal do mapa
│       ├── MapView.css
│       ├── LayerControl.tsx    # Controle de camadas
│       ├── LayerControl.css
│       └── index.ts
├── pages/
│   ├── HomePage.tsx            # Página principal
│   ├── HomePage.css
│   └── __tests__/
│       └── HomePage.test.tsx
├── services/
│   └── onboardingService.ts    # Serviços de cadastro
├── App.tsx
├── main.tsx
└── index.css
```

## 🗺️ Sistema de Camadas

O sistema suporta três tipos de camadas:

### 1. Marcadores (Marker)
```typescript
{
  type: 'marker',
  data: {
    position: [lat, lng],
    description: 'Descrição'
  }
}
```

### 2. Polígonos (Polygon)
```typescript
{
  type: 'polygon',
  data: {
    positions: [[lat1, lng1], [lat2, lng2], ...],
    area: 100,
    description: 'Área rural'
  }
}
```

### 3. Círculos (Circle)
```typescript
{
  type: 'circle',
  data: {
    center: [lat, lng],
    radius: 5000, // metros
    description: 'Zona urbana'
  }
}
```

## 🎨 Customização

### Adicionar Nova Camada

```typescript
const newLayer: MapLayer = {
  id: 'unique-id',
  name: 'Nome da Camada',
  type: 'polygon',
  visible: true,
  color: '#4CAF50',
  data: {
    positions: [...],
    area: 100,
    description: 'Descrição'
  }
}

setLayers(prev => [...prev, newLayer])
```

### Mudar Centro do Mapa

```tsx
<MapView 
  center={[-15.7939, -47.8828]} // [latitude, longitude]
  zoom={10}
  layers={layers}
/>
```

## 🧪 Testes

Os testes estão configurados com Vitest e Testing Library:

```bash
# Rodar testes
npm test

# Rodar testes em watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

## 📝 Notas de Desenvolvimento

- O serviço `onboardingService.ts` atualmente é um mock. Substitua por chamadas reais de API quando integrar com backend.
- Os ícones do Leaflet são configurados automaticamente no `MapView.tsx`
- O CSS é modular e cada componente tem seu próprio arquivo de estilos

## 🔜 Próximas Funcionalidades

- [ ] Integração com Azure Cosmos DB
- [ ] Autenticação real com Azure AD
- [ ] Upload de arquivos KML/GeoJSON
- [ ] Desenho de camadas no mapa
- [ ] Relatórios e dashboards
- [ ] Modo escuro
- [ ] PWA com offline support

## 📄 Licença

Privado - Ativo Real © 2026
