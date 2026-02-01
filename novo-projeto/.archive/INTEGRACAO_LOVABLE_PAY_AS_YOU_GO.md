# 🔗 Guia de Integração: Pay As You Go + SPA Lovable.dev

## 🎯 Objetivo

Este documento explica como integrar o **sistema de assinaturas Pay As You Go** (backend já implementado) com a **arquitetura SPA proposta para Lovable.dev** (frontend com mapa full-screen e sidebar dinâmica).

---

## 📋 Visão Geral da Integração

### O Que Você Já Tem (Backend)
✅ Sistema completo de assinaturas com 4 planos  
✅ APIs REST para gerenciar assinaturas  
✅ Validação de limites por plano  
✅ Banco de dados PostgreSQL estruturado  

### O Que Você Quer Adicionar (Frontend)
🎨 SPA com mapa full-screen (Mapbox/Leaflet)  
🎨 Sidebar com ícones e painéis deslizantes  
🎨 Controle de acesso por roles (Premium vs Comum)  
🎨 Interface unificada sem recarregamento  

### Como Unir as Duas Partes
🔗 O sistema de assinaturas define os **limites e permissões**  
🔗 A interface SPA **adapta a UI** baseada na assinatura do usuário  
🔗 O role do usuário determina quais **ferramentas aparecem na sidebar**  

---

## 🏗️ Arquitetura Integrada

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Lovable.dev SPA)               │
│  ┌────────────┐  ┌──────────────────────────────────────┐  │
│  │  Sidebar   │  │         Mapa Full-Screen             │  │
│  │            │  │         (Mapbox/Leaflet)             │  │
│  │ [Ícones]   │  │                                      │  │
│  │            │  │  - Marcadores de projetos            │  │
│  │  ┌─────┐   │  │  - Polígonos de áreas                │  │
│  │  │Panel│   │  │  - Camadas de satélite               │  │
│  │  └─────┘   │  │                                      │  │
│  └────────────┘  └──────────────────────────────────────┘  │
│                           ▲                                 │
│                           │ Estado Global (Context/Zustand) │
│                           │ - Usuario logado                │
│                           │ - Assinatura ativa              │
│                           │ - Limites do plano              │
│                           ▼                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              BACKEND (Azure Functions - Python)             │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ GET /api/planos  │  │ Validação de     │               │
│  │ GET /assinaturas │  │ Limites          │               │
│  │ POST /projetos   │  │ verificar_limite │               │
│  └──────────────────┘  └──────────────────┘               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           BANCO DE DADOS (PostgreSQL + PostGIS)             │
│  - planos_pagamento (4 planos)                              │
│  - assinaturas (status, limites)                            │
│  - projetos / lotes (dados geoespaciais)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Mapeamento: Assinatura ↔ Roles ↔ UI

### Lógica de Negócio

| Assinatura | Role UI | Projetos Visíveis | Ferramentas Sidebar |
|------------|---------|-------------------|---------------------|
| **FREE** | Comum | Apenas seus projetos | Formulário, Documentos |
| **BÁSICO** | Comum | Apenas seus projetos | Formulário, Documentos, Upload |
| **PROFISSIONAL** | Premium | Todos os projetos | Dashboard, Análise, OCR, Config |
| **ENTERPRISE** | Premium | Todos os projetos | Todas + API, Relatórios |

### Implementação

```typescript
// types.ts
export type UserRole = 'COMUM' | 'PREMIUM';

export interface UserSubscription {
  plano: 'FREE' | 'BASICO' | 'PROFISSIONAL' | 'ENTERPRISE';
  max_projetos: number;
  max_lotes: number;
  storage_mb: number;
  permite_export_kml: boolean;
  permite_export_shp: boolean;
  permite_api_access: boolean;
}

export interface UserContext {
  id: number;
  email: string;
  role: UserRole;
  subscription: UserSubscription;
}

// Mapear assinatura para role
function getRole(plano: string): UserRole {
  if (plano === 'PROFISSIONAL' || plano === 'ENTERPRISE') {
    return 'PREMIUM';
  }
  return 'COMUM';
}
```

---

## 💻 Implementação Frontend (React + Zustand)

### 1. Estado Global com Zustand

```typescript
// store/useAppStore.ts
import create from 'zustand';

interface AppState {
  user: UserContext | null;
  activeSidebarPanel: string | null;
  mapCenter: [number, number];
  mapZoom: number;
  
  // Actions
  setUser: (user: UserContext | null) => void;
  toggleSidebarPanel: (panelId: string) => void;
  setMapView: (center: [number, number], zoom: number) => void;
  
  // Computed
  getUserRole: () => UserRole;
  canCreateProject: () => boolean;
  getAvailableTools: () => string[];
}

export const useAppStore = create<AppState>((set, get) => ({
  user: null,
  activeSidebarPanel: null,
  mapCenter: [-15.7801, -47.9292], // Brasília
  mapZoom: 10,
  
  setUser: (user) => set({ user }),
  
  toggleSidebarPanel: (panelId) => set((state) => ({
    activeSidebarPanel: state.activeSidebarPanel === panelId ? null : panelId
  })),
  
  setMapView: (center, zoom) => set({ mapCenter: center, mapZoom: zoom }),
  
  getUserRole: () => {
    const user = get().user;
    if (!user) return 'COMUM';
    return getRole(user.subscription.plano);
  },
  
  canCreateProject: () => {
    const user = get().user;
    if (!user) return false;
    
    // Aqui você faria uma chamada à API para verificar o limite
    // Por enquanto, apenas verifica se o plano permite
    return user.subscription.max_projetos > 0;
  },
  
  getAvailableTools: () => {
    const role = get().getUserRole();
    
    if (role === 'PREMIUM') {
      return [
        'dashboard',
        'overlap-analysis',
        'pdf-ocr',
        'settings',
        'reports',
        'api-access'
      ];
    }
    
    return ['form', 'documents', 'upload'];
  }
}));
```

### 2. Hook para Verificar Limites

```typescript
// hooks/useSubscriptionLimits.ts
import { useAppStore } from '@/store/useAppStore';
import { useQuery, useMutation } from '@tanstack/react-query';
import api from '@/lib/api';

export function useSubscriptionLimits() {
  const user = useAppStore((state) => state.user);
  
  // Buscar assinatura atual
  const { data: subscription, isLoading } = useQuery({
    queryKey: ['subscription', user?.id],
    queryFn: async () => {
      if (!user) return null;
      const response = await api.get(`/assinaturas/current?usuario_id=${user.id}`);
      return response.data;
    },
    enabled: !!user
  });
  
  // Verificar se pode criar projeto
  const checkProjectLimit = async () => {
    if (!user) throw new Error('Usuário não autenticado');
    
    const response = await api.get(`/projetos?usuario_id=${user.id}`);
    const projectCount = response.data.length;
    
    if (subscription.plano.max_projetos === -1) {
      return { canCreate: true, used: projectCount, limit: '∞' };
    }
    
    return {
      canCreate: projectCount < subscription.plano.max_projetos,
      used: projectCount,
      limit: subscription.plano.max_projetos
    };
  };
  
  return {
    subscription,
    isLoading,
    checkProjectLimit,
    hasFeature: (feature: string) => {
      if (!subscription) return false;
      return subscription.plano[`permite_${feature}`] === true;
    }
  };
}
```

### 3. Componente Principal (App Shell)

```tsx
// App.tsx
import { useEffect } from 'react';
import { useAppStore } from '@/store/useAppStore';
import Sidebar from '@/components/Sidebar';
import Map from '@/components/Map';
import SlidingPanel from '@/components/SlidingPanel';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

export default function App() {
  const { user, setUser } = useAppStore();
  
  useEffect(() => {
    // Carregar usuário do Supabase/Auth
    async function loadUser() {
      // Exemplo com Supabase
      const { data: session } = await supabase.auth.getSession();
      
      if (session?.user) {
        // Buscar assinatura do usuário
        const response = await fetch(
          `/api/assinaturas/current?usuario_id=${session.user.id}`
        );
        const subscription = await response.json();
        
        setUser({
          id: session.user.id,
          email: session.user.email,
          role: getRole(subscription.plano.nome),
          subscription: subscription.plano
        });
      }
    }
    
    loadUser();
  }, []);
  
  if (!user) {
    return <LoginScreen />;
  }
  
  return (
    <QueryClientProvider client={queryClient}>
      <div className="h-screen w-screen overflow-hidden relative">
        {/* Mapa Full-Screen (Background) */}
        <Map />
        
        {/* Sidebar à Esquerda */}
        <Sidebar />
        
        {/* Painel Deslizante */}
        <SlidingPanel />
      </div>
    </QueryClientProvider>
  );
}
```

### 4. Sidebar Adaptativa

```tsx
// components/Sidebar.tsx
import { useAppStore } from '@/store/useAppStore';
import { Home, Map, FileText, Settings, BarChart, Upload } from 'lucide-react';

export default function Sidebar() {
  const { getUserRole, getAvailableTools, toggleSidebarPanel, activeSidebarPanel } = useAppStore();
  const role = getUserRole();
  const tools = getAvailableTools();
  
  const toolIcons = {
    dashboard: { icon: Home, label: 'Dashboard' },
    'overlap-analysis': { icon: Map, label: 'Análise de Sobreposição' },
    'pdf-ocr': { icon: FileText, label: 'Leitor PDF/OCR' },
    settings: { icon: Settings, label: 'Configurações' },
    form: { icon: FileText, label: 'Formulário' },
    documents: { icon: Upload, label: 'Documentos' },
    reports: { icon: BarChart, label: 'Relatórios' }
  };
  
  return (
    <div className="fixed left-0 top-0 h-screen w-16 bg-gray-800 z-10 flex flex-col items-center py-4 space-y-4">
      {/* Logo */}
      <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center text-white font-bold">
        BR
      </div>
      
      {/* Ferramentas baseadas no role */}
      {tools.map((toolId) => {
        const tool = toolIcons[toolId];
        if (!tool) return null;
        
        const Icon = tool.icon;
        const isActive = activeSidebarPanel === toolId;
        
        return (
          <button
            key={toolId}
            onClick={() => toggleSidebarPanel(toolId)}
            className={`w-10 h-10 rounded-lg flex items-center justify-center transition-colors ${
              isActive 
                ? 'bg-blue-500 text-white' 
                : 'text-gray-400 hover:bg-gray-700 hover:text-white'
            }`}
            title={tool.label}
          >
            <Icon size={20} />
          </button>
        );
      })}
    </div>
  );
}
```

### 5. Mapa com Filtragem por Role

```tsx
// components/Map.tsx
import { useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import { useAppStore } from '@/store/useAppStore';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';

export default function Map() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const { user, mapCenter, mapZoom, getUserRole } = useAppStore();
  const role = getUserRole();
  
  // Buscar projetos baseado no role
  const { data: projects } = useQuery({
    queryKey: ['projects', user?.id, role],
    queryFn: async () => {
      if (role === 'PREMIUM') {
        // Premium vê todos os projetos
        const response = await api.get('/projetos');
        return response.data;
      } else {
        // Comum vê apenas seus projetos
        const response = await api.get(`/projetos?usuario_id=${user?.id}`);
        return response.data;
      }
    },
    enabled: !!user
  });
  
  useEffect(() => {
    if (!mapContainer.current || map.current) return;
    
    // Inicializar mapa
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/satellite-streets-v12',
      center: mapCenter,
      zoom: mapZoom
    });
    
    // Adicionar controles
    map.current.addControl(new mapboxgl.NavigationControl());
  }, []);
  
  // Atualizar marcadores quando projetos carregarem
  useEffect(() => {
    if (!map.current || !projects) return;
    
    // Limpar marcadores existentes
    // ... (código para limpar)
    
    // Adicionar marcadores dos projetos
    projects.forEach((project) => {
      if (project.geom) {
        // Adicionar marcador ou polígono
        const marker = new mapboxgl.Marker()
          .setLngLat([project.longitude, project.latitude])
          .setPopup(new mapboxgl.Popup().setHTML(`
            <h3>${project.nome}</h3>
            <p>${project.descricao}</p>
          `))
          .addTo(map.current!);
      }
    });
  }, [projects]);
  
  return (
    <div 
      ref={mapContainer} 
      className="absolute inset-0 w-full h-full"
    />
  );
}
```

### 6. Painel com Validação de Limites

```tsx
// components/panels/CreateProjectPanel.tsx
import { useState } from 'react';
import { useSubscriptionLimits } from '@/hooks/useSubscriptionLimits';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/lib/api';
import { AlertCircle } from 'lucide-react';

export default function CreateProjectPanel() {
  const { subscription, checkProjectLimit } = useSubscriptionLimits();
  const queryClient = useQueryClient();
  const [projectName, setProjectName] = useState('');
  const [error, setError] = useState<string | null>(null);
  
  const createProjectMutation = useMutation({
    mutationFn: async (data: any) => {
      // Verificar limite ANTES de criar
      const limitCheck = await checkProjectLimit();
      
      if (!limitCheck.canCreate) {
        throw new Error(
          `Limite de ${limitCheck.limit} projetos atingido. ` +
          `Você tem ${limitCheck.used} projetos. ` +
          `Faça upgrade para criar mais projetos.`
        );
      }
      
      return api.post('/projetos', data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['projects']);
      setProjectName('');
      setError(null);
    },
    onError: (error: any) => {
      setError(error.message);
    }
  });
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createProjectMutation.mutate({
      nome: projectName,
      descricao: '',
      tipo: 'INDIVIDUAL'
    });
  };
  
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Novo Projeto</h2>
      
      {/* Indicador de Uso */}
      {subscription && (
        <div className="mb-4 p-3 bg-blue-50 rounded-lg">
          <p className="text-sm text-gray-600">
            Plano: <strong>{subscription.plano.nome}</strong>
          </p>
          <p className="text-sm text-gray-600">
            Projetos: <strong>{subscription.projetos_usados || 0} / {
              subscription.plano.max_projetos === -1 
                ? '∞' 
                : subscription.plano.max_projetos
            }</strong>
          </p>
        </div>
      )}
      
      {/* Erro de Limite */}
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-start gap-2">
          <AlertCircle className="text-red-500 flex-shrink-0" size={20} />
          <div className="flex-1">
            <p className="text-sm text-red-700">{error}</p>
            <a 
              href="/upgrade" 
              className="text-sm text-blue-600 hover:underline mt-1 inline-block"
            >
              Fazer upgrade agora →
            </a>
          </div>
        </div>
      )}
      
      {/* Formulário */}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={projectName}
          onChange={(e) => setProjectName(e.target.value)}
          placeholder="Nome do projeto"
          className="w-full p-2 border rounded mb-4"
          required
        />
        <button
          type="submit"
          disabled={createProjectMutation.isLoading}
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {createProjectMutation.isLoading ? 'Criando...' : 'Criar Projeto'}
        </button>
      </form>
    </div>
  );
}
```

---

## 🔄 Fluxo Completo: Login → Validação → UI Adaptada

```
1. Usuário faz login no Supabase
   ↓
2. Frontend busca assinatura via API
   GET /api/assinaturas/current?usuario_id={id}
   ↓
3. Determina role baseado no plano
   - FREE/BÁSICO → COMUM
   - PROFISSIONAL/ENTERPRISE → PREMIUM
   ↓
4. Carrega ferramentas da sidebar baseado no role
   - COMUM: [form, documents]
   - PREMIUM: [dashboard, overlap-analysis, pdf-ocr, settings]
   ↓
5. Carrega projetos no mapa
   - COMUM: apenas seus projetos
   - PREMIUM: todos os projetos
   ↓
6. Valida limites ANTES de cada ação
   - Criar projeto: checkProjectLimit()
   - Exportar: subscription.permite_export_kml
   - API: subscription.permite_api_access
   ↓
7. Mostra erro ou upgrade prompt se limite atingido
```

---

## 📁 Estrutura de Pastas Sugerida

```
src/
├── components/
│   ├── Sidebar.tsx
│   ├── Map.tsx
│   ├── SlidingPanel.tsx
│   └── panels/
│       ├── DashboardPanel.tsx
│       ├── FormPanel.tsx
│       ├── DocumentsPanel.tsx
│       ├── CreateProjectPanel.tsx
│       └── UpgradePrompt.tsx
├── hooks/
│   ├── useSubscriptionLimits.ts
│   ├── useAuth.ts
│   └── useProjects.ts
├── store/
│   └── useAppStore.ts
├── lib/
│   ├── api.ts
│   └── supabase.ts
├── types/
│   └── index.ts
└── App.tsx
```

---

## 🎨 Componente de Upgrade Prompt

```tsx
// components/UpgradePrompt.tsx
import { useAppStore } from '@/store/useAppStore';
import { Crown, X } from 'lucide-react';

interface UpgradePromptProps {
  feature: string;
  onClose: () => void;
}

export default function UpgradePrompt({ feature, onClose }: UpgradePromptProps) {
  const subscription = useAppStore((state) => state.user?.subscription);
  
  const plans = [
    {
      id: 2,
      name: 'BÁSICO',
      price: 99,
      features: ['10 projetos', '50 lotes', 'Exportar KML']
    },
    {
      id: 3,
      name: 'PROFISSIONAL',
      price: 299,
      features: ['50 projetos', '200 lotes', 'Exportar SHP/DXF', 'Análise de sobreposição']
    },
    {
      id: 4,
      name: 'ENTERPRISE',
      price: 999,
      features: ['Ilimitado', 'API Access', 'Suporte dedicado']
    }
  ];
  
  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-auto">
        {/* Header */}
        <div className="p-6 border-b flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Crown className="text-yellow-500" />
              Upgrade Necessário
            </h2>
            <p className="text-gray-600 mt-1">
              A funcionalidade "{feature}" requer um plano superior
            </p>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X size={24} />
          </button>
        </div>
        
        {/* Planos */}
        <div className="p-6 grid grid-cols-3 gap-4">
          {plans.map((plan) => (
            <div 
              key={plan.id}
              className="border rounded-lg p-4 hover:border-blue-500 transition-colors"
            >
              <h3 className="font-bold text-lg">{plan.name}</h3>
              <p className="text-3xl font-bold my-2">
                R$ {plan.price}<span className="text-sm text-gray-500">/mês</span>
              </p>
              <ul className="space-y-2 mb-4">
                {plan.features.map((feature, idx) => (
                  <li key={idx} className="text-sm text-gray-600">✓ {feature}</li>
                ))}
              </ul>
              <button 
                onClick={() => {
                  // Redirecionar para upgrade
                  window.location.href = `/upgrade?plano_id=${plan.id}`;
                }}
                className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
              >
                Escolher {plan.name}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

---

## 🔗 API Client

```typescript
// lib/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://sua-api.azurewebsites.net/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Adicionar token de autenticação
api.interceptors.request.use(async (config) => {
  const { data: session } = await supabase.auth.getSession();
  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`;
  }
  return config;
});

export default api;
```

---

## ✅ Checklist de Implementação

### Backend (Já Implementado)
- [x] Tabelas de assinaturas
- [x] APIs REST
- [x] Validação de limites
- [x] Planos configurados

### Frontend (A Fazer no Lovable.dev)
- [ ] Configurar Zustand store
- [ ] Criar componente Sidebar adaptativo
- [ ] Integrar Mapbox/Leaflet
- [ ] Implementar painéis deslizantes
- [ ] Adicionar hook useSubscriptionLimits
- [ ] Criar componente UpgradePrompt
- [ ] Implementar autenticação Supabase
- [ ] Conectar APIs do backend
- [ ] Filtrar projetos por role
- [ ] Validar limites antes de ações

---

## 🎯 Prompt Completo para Lovable.dev

Use este prompt no Lovable.dev para criar o frontend integrado:

```
Crie uma SPA React com Tailwind CSS e Supabase que se integra com uma API REST existente.

ARQUITETURA:
- Mapa full-screen (Mapbox GL JS) como background
- Sidebar fixa à esquerda (64px) com ícones
- Painéis deslizantes que se abrem ao clicar nos ícones
- Estado global com Zustand

AUTENTICAÇÃO E ROLES:
- Login via Supabase Auth
- Ao logar, buscar assinatura do usuário via GET /api/assinaturas/current?usuario_id={id}
- Determinar role baseado no plano:
  - FREE/BÁSICO → role "COMUM"
  - PROFISSIONAL/ENTERPRISE → role "PREMIUM"

SIDEBAR ADAPTATIVA:
- Role COMUM: [form, documents, upload]
- Role PREMIUM: [dashboard, overlap-analysis, pdf-ocr, settings, reports]

MAPA:
- Role COMUM: mostrar apenas projetos do usuário (GET /projetos?usuario_id={id})
- Role PREMIUM: mostrar todos projetos (GET /projetos)
- Adicionar marcadores clicáveis
- Zoom para projeto ao clicar na lista

VALIDAÇÃO DE LIMITES:
- Antes de criar projeto, verificar limite via API
- Se limite atingido, mostrar modal de upgrade
- Indicador de uso no painel (X/Y projetos usados)

COMPONENTES NECESSÁRIOS:
1. Sidebar (com ícones adaptativos por role)
2. Map (com filtro de projetos por role)
3. SlidingPanel (container para painéis)
4. CreateProjectPanel (com validação de limite)
5. UpgradePrompt (modal de upgrade)
6. useSubscriptionLimits (hook customizado)
7. useAppStore (Zustand store)

API ENDPOINTS:
- GET /api/planos
- GET /api/assinaturas/current?usuario_id={id}
- POST /api/assinaturas
- GET /api/projetos
- POST /api/projetos

ESTILO:
- Sidebar: bg-gray-800, ícones inativos text-gray-400
- Ícone ativo: bg-blue-500 text-white
- Painéis: bg-white shadow-lg w-96
- Transições suaves (transition-all duration-300)
```

---

## 📞 Suporte

Para dúvidas sobre:
- **Backend/APIs**: Ver `GUIA_PRATICO_PAY_AS_YOU_GO.md`
- **Arquitetura**: Ver `ARQUITETURA_PAY_AS_YOU_GO.md`
- **Frontend/React**: Seguir exemplos deste documento

---

**Última atualização:** 31/01/2026  
**Versão:** 1.0  
**Status:** ✅ Guia de Integração Completo
