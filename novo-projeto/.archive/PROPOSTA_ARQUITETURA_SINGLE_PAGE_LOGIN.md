# 🏗️ PROPOSTA: ARQUITETURA SINGLE-PAGE COM LOGIN CENTRALIZADO

**Projeto:** Ativo Real - GeoPlatform  
**Data:** 31 de Janeiro de 2026  
**Versão:** 2.0 (Refatoração Completa)

---

## 📌 RESUMO EXECUTIVO

Esta proposta consolida as análises profundas realizadas nos 3 pilares do Ativo Real:
- ✅ **Frontend**: 2 aplicações paralelas, 26 componentes, 7000+ linhas
- ✅ **Backend**: 15 endpoints REST, modelo Pay-as-you-go, validação geoespacial
- ✅ **Infraestrutura**: Azure serverless, PostgreSQL+PostGIS, Cosmos DB opcional

**OBJETIVO**: Transformar a arquitetura atual em um **aplicativo single-page moderno** onde:
1. **Todo o conteúdo fica em uma única página principal** após login
2. **Navegação lateral** entre seções (Dashboard, Mapa, Projetos, Assinaturas)
3. **Autenticação JWT robusta** com controle de acesso por perfil
4. **Estado global gerenciado** via Context API + Zustand
5. **Eliminação de duplicação** (consolidar 2 frontends em 1)

---

## 🎯 OBJETIVOS DA REFATORAÇÃO

### 1. Arquitetura Single-Page Application (SPA)
- ✅ Toda a aplicação renderizada em `/app` após login
- ✅ Sidebar permanente com navegação entre módulos
- ✅ Sem recarregamento de página (React Router)
- ✅ Estado persistente entre navegações

### 2. Sistema de Login Centralizado
- ✅ Autenticação JWT com refresh tokens
- ✅ 4 perfis: Admin, Topógrafo, Proprietário, Agricultor
- ✅ RBAC (Role-Based Access Control) em frontend + backend
- ✅ Proteção de rotas por perfil

### 3. Consolidação de Código
- ✅ Eliminar `frontend/` simplificado
- ✅ Manter apenas `ativo-real/` como base
- ✅ Refatorar GlobalMap (1303 linhas → módulos <300 linhas)
- ✅ Criar biblioteca de componentes reutilizáveis

### 4. Estado Global Centralizado
- ✅ Context API para autenticação
- ✅ Zustand para estado de aplicação (projetos, mapa)
- ✅ React Query para cache de API
- ✅ Eliminar props drilling

### 5. Backend Seguro
- ✅ Implementar middleware JWT em Azure Functions
- ✅ Endpoints protegidos com decorators `@require_auth`
- ✅ Senhas hasheadas com bcrypt
- ✅ Tabela `users` em PostgreSQL

---

## 📐 ARQUITETURA PROPOSTA

### Estrutura Visual de Navegação

```
┌─────────────────────────────────────────────────────────────┐
│  LANDING PAGE (/)                                           │
│  [Sem login] 3 Cards de perfil + Informações institucionais│
└─────────────────────────────────────────────────────────────┘
                            ↓
                    [Botão: Entrar]
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  LOGIN PAGE (/login)                                        │
│  Email + Senha → JWT → Redireciona para /app               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  APP LAYOUT (/app) - SINGLE PAGE                            │
│  ┌──────────┬────────────────────────────────────────────┐  │
│  │ SIDEBAR  │  CONTEÚDO PRINCIPAL (Router Outlet)        │  │
│  │          │                                            │  │
│  │ 🏠 Início│  Renderiza componente baseado na rota:    │  │
│  │ 📊 Dashbd│  - /app → Dashboard                        │  │
│  │ 🗺️ Mapa  │  - /app/map → GlobalMap                    │  │
│  │ 📁 Projet│  - /app/projects → Lista de Projetos       │  │
│  │ 💳 Planos│  - /app/subscriptions → Gerenciar Plano    │  │
│  │ ⚙️ Config│  - /app/settings → Configurações           │  │
│  │ 🚪 Sair  │                                            │  │
│  │          │  Estado global acessível em todos componts│  │
│  │ [Avatar] │  User: {name, role, email}                │  │
│  └──────────┴────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 ESTRUTURA DE PASTAS PROPOSTA

```
novo-projeto/ativo-real/src/
├── 📂 app/                           # 🆕 Aplicação principal (tudo aqui)
│   ├── 📄 AppLayout.tsx              # Layout com Sidebar + Header + Outlet
│   ├── 📄 AppRoutes.tsx              # Rotas protegidas do app
│   │
│   ├── 📂 modules/                   # Módulos funcionais
│   │   ├── 📂 dashboard/
│   │   │   ├── DashboardTopografo.tsx
│   │   │   ├── DashboardProprietario.tsx
│   │   │   ├── DashboardAdmin.tsx
│   │   │   └── components/
│   │   │       ├── ProjectCard.tsx
│   │   │       ├── PaymentSummary.tsx
│   │   │       └── ActivityFeed.tsx
│   │   │
│   │   ├── 📂 map/                   # Módulo de mapa (refatorado)
│   │   │   ├── MapContainer.tsx      # Container principal (150 linhas)
│   │   │   ├── components/
│   │   │   │   ├── MapCore.tsx       # Setup OpenLayers (200 linhas)
│   │   │   │   ├── MapToolbar.tsx    # Ferramentas de desenho (100 linhas)
│   │   │   │   ├── MapLayers.tsx     # Gestão de camadas (150 linhas)
│   │   │   │   ├── MapPopup.tsx      # Popup de features (80 linhas)
│   │   │   │   ├── MapImport.tsx     # Importação de arquivos (120 linhas)
│   │   │   │   └── MapExport.tsx     # Exportação (100 linhas)
│   │   │   ├── hooks/
│   │   │   │   ├── useMapSetup.ts    # Inicialização do mapa
│   │   │   │   ├── useMapTools.ts    # Lógica de ferramentas CAD
│   │   │   │   ├── useMapStorage.ts  # Persistência (migrar para backend)
│   │   │   │   └── useMapImport.ts   # Lógica de importação
│   │   │   └── utils/
│   │   │       ├── cadTools.ts       # Operações CAD (offset, rotate, etc)
│   │   │       ├── coordinateUtils.ts # Conversões SIRGAS 2000
│   │   │       └── geometryValidation.ts # Validações locais
│   │   │
│   │   ├── 📂 projects/
│   │   │   ├── ProjectList.tsx       # Lista com filtros/busca
│   │   │   ├── ProjectDetail.tsx     # Detalhes do projeto
│   │   │   ├── ProjectCreate.tsx     # Modal/form de criação
│   │   │   └── components/
│   │   │       ├── ProjectCard.tsx
│   │   │       ├── ProjectFilters.tsx
│   │   │       └── ProjectStats.tsx
│   │   │
│   │   ├── 📂 subscriptions/
│   │   │   ├── SubscriptionDashboard.tsx  # Overview do plano atual
│   │   │   ├── PlanComparison.tsx         # Tabela de planos
│   │   │   ├── BillingHistory.tsx         # Histórico de pagamentos
│   │   │   └── components/
│   │   │       ├── PlanCard.tsx
│   │   │       ├── UsageMetrics.tsx       # Limites de uso
│   │   │       └── PaymentMethodSelector.tsx
│   │   │
│   │   └── 📂 settings/
│   │       ├── UserSettings.tsx      # Configurações de conta
│   │       ├── TeamSettings.tsx      # Gestão de equipe
│   │       └── IntegrationSettings.tsx # Tokens API, webhooks
│   │
│   └── 📂 components/                # Componentes compartilhados do app
│       ├── Sidebar.tsx
│       ├── Header.tsx
│       ├── UserMenu.tsx
│       └── NotificationCenter.tsx
│
├── 📂 auth/                          # 🆕 Sistema de autenticação
│   ├── 📂 pages/
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   └── ForgotPasswordPage.tsx
│   ├── 📂 contexts/
│   │   └── AuthContext.tsx           # Context global de autenticação
│   ├── 📂 hooks/
│   │   ├── useAuth.ts                # Hook conveniente
│   │   └── usePermissions.ts         # Verifica permissões RBAC
│   └── 📂 components/
│       ├── ProtectedRoute.tsx        # Wrapper de rotas protegidas
│       └── RoleGuard.tsx             # Guard por perfil
│
├── 📂 landing/                       # Páginas públicas
│   ├── LandingPage.tsx               # Landing institucional
│   └── components/
│       ├── Hero.tsx
│       ├── Features.tsx
│       ├── Pricing.tsx
│       └── ProfileCards.tsx
│
├── 📂 shared/                        # 🆕 Componentes reutilizáveis
│   ├── 📂 ui/                        # Design System
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Modal.tsx
│   │   ├── Toast.tsx
│   │   ├── Card.tsx
│   │   ├── Badge.tsx
│   │   ├── Spinner.tsx
│   │   └── Tooltip.tsx
│   ├── 📂 icons/
│   │   └── TopoIcon.tsx              # Wrapper de ícones SVG
│   └── 📂 layouts/
│       └── EmptyState.tsx
│
├── 📂 stores/                        # 🆕 Zustand stores
│   ├── projectStore.ts               # Estado de projetos
│   ├── mapStore.ts                   # Estado do mapa (layers, features)
│   └── uiStore.ts                    # Estado de UI (modals, sidebars)
│
├── 📂 services/                      # API clients
│   ├── api.ts                        # 🆕 Cliente Axios configurado
│   ├── projectsApi.ts                # CRUD de projetos
│   ├── lotesApi.ts                   # CRUD de lotes
│   ├── subscriptionsApi.ts           # 🆕 API de assinaturas
│   ├── authApi.ts                    # 🆕 Login/logout/refresh
│   └── infinitePayApi.ts             # Integração InfinitePay
│
├── 📂 types/                         # TypeScript types
│   ├── auth.ts                       # User, LoginCredentials, AuthState
│   ├── project.ts                    # Projeto, Lote, Pagamento
│   ├── subscription.ts               # 🆕 Plano, Assinatura, Histórico
│   ├── map.ts                        # Feature, Layer, MapState
│   └── api.ts                        # ApiResponse, ApiError
│
├── 📂 hooks/                         # Custom hooks globais
│   ├── useApi.ts                     # Hook para chamadas API
│   ├── useDebounce.ts
│   ├── useLocalStorage.ts
│   └── useMediaQuery.ts
│
├── 📂 utils/
│   ├── formatters.ts                 # Formatação de dados
│   ├── validators.ts                 # Validações
│   └── constants.ts                  # Constantes globais
│
├── 📂 styles/
│   ├── globals.css
│   ├── design-tokens.css             # Variáveis CSS
│   └── themes/
│       ├── light.css
│       └── dark.css
│
├── 📄 App.tsx                        # 🆕 Router principal
├── 📄 main.tsx
└── 📄 vite-env.d.ts
```

---

## 🔐 SISTEMA DE AUTENTICAÇÃO PROPOSTA

### 1. Fluxo de Autenticação

```typescript
// src/auth/contexts/AuthContext.tsx
import { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '@/services/authApi';

interface User {
  id: string;
  name: string;
  email: string;
  role: 'ADMIN' | 'TOPOGRAFO' | 'CLIENTE' | 'AGRICULTOR';
  avatar?: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Verifica token ao carregar app
    const token = localStorage.getItem('access_token');
    if (token) {
      validateToken(token);
    } else {
      setIsLoading(false);
    }
  }, []);

  const validateToken = async (token: string) => {
    try {
      const userData = await authApi.validateToken(token);
      setUser(userData);
    } catch {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const response = await authApi.login({ email, password });
    
    localStorage.setItem('access_token', response.access_token);
    localStorage.setItem('refresh_token', response.refresh_token);
    
    setUser(response.user);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  const refreshToken = async () => {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) throw new Error('No refresh token');
    
    const response = await authApi.refreshToken(refresh);
    localStorage.setItem('access_token', response.access_token);
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, isLoading, login, logout, refreshToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
```

### 2. Proteção de Rotas

```typescript
// src/auth/components/ProtectedRoute.tsx
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '@/auth/hooks/useAuth';
import { Spinner } from '@/shared/ui/Spinner';

interface ProtectedRouteProps {
  allowedRoles?: string[];
}

export const ProtectedRoute = ({ allowedRoles }: ProtectedRouteProps) => {
  const { isAuthenticated, isLoading, user } = useAuth();

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user!.role)) {
    return <Navigate to="/app" replace />;
  }

  return <Outlet />;
};
```

### 3. Rotas Principais

```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from '@/auth/contexts/AuthContext';
import { ProtectedRoute } from '@/auth/components/ProtectedRoute';
import { AppLayout } from '@/app/AppLayout';
import { LandingPage } from '@/landing/LandingPage';
import { LoginPage } from '@/auth/pages/LoginPage';

// Lazy loading de módulos pesados
const DashboardTopografo = lazy(() => import('@/app/modules/dashboard/DashboardTopografo'));
const MapContainer = lazy(() => import('@/app/modules/map/MapContainer'));
const ProjectList = lazy(() => import('@/app/modules/projects/ProjectList'));
const SubscriptionDashboard = lazy(() => import('@/app/modules/subscriptions/SubscriptionDashboard'));

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Suspense fallback={<Spinner fullScreen />}>
          <Routes>
            {/* Rotas públicas */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            
            {/* Rotas protegidas */}
            <Route element={<ProtectedRoute />}>
              <Route path="/app" element={<AppLayout />}>
                {/* Dashboard baseado em role */}
                <Route index element={<RoleBasedDashboard />} />
                
                {/* Módulos */}
                <Route path="map" element={<MapContainer />} />
                <Route path="map/:projectId" element={<MapContainer />} />
                <Route path="projects" element={<ProjectList />} />
                <Route path="subscriptions" element={<SubscriptionDashboard />} />
                <Route path="settings" element={<UserSettings />} />
              </Route>
            </Route>

            {/* 404 */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Suspense>
      </BrowserRouter>
    </AuthProvider>
  );
}
```

---

## 🎨 LAYOUT SINGLE-PAGE

### AppLayout.tsx (Container Principal)

```typescript
// src/app/AppLayout.tsx
import { Outlet } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { ToastContainer } from '@/shared/ui/Toast';

export const AppLayout = () => {
  return (
    <div className="flex h-screen overflow-hidden bg-gray-50 dark:bg-gray-900">
      {/* Sidebar fixa à esquerda */}
      <Sidebar />
      
      {/* Área principal */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Header fixo no topo */}
        <Header />
        
        {/* Conteúdo scrollável */}
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet /> {/* Renderiza o módulo ativo */}
        </main>
      </div>

      {/* Sistema de notificações global */}
      <ToastContainer />
    </div>
  );
};
```

### Sidebar.tsx

```typescript
// src/app/components/Sidebar.tsx
import { NavLink } from 'react-router-dom';
import { useAuth } from '@/auth/hooks/useAuth';
import { AnimatedLogo } from '@/shared/icons/AnimatedLogo';

const navigation = [
  { name: 'Dashboard', href: '/app', icon: HomeIcon, roles: ['ALL'] },
  { name: 'Mapa', href: '/app/map', icon: MapIcon, roles: ['TOPOGRAFO', 'ADMIN'] },
  { name: 'Projetos', href: '/app/projects', icon: FolderIcon, roles: ['TOPOGRAFO', 'ADMIN'] },
  { name: 'Assinaturas', href: '/app/subscriptions', icon: CreditCardIcon, roles: ['ALL'] },
  { name: 'Configurações', href: '/app/settings', icon: CogIcon, roles: ['ALL'] },
];

export const Sidebar = () => {
  const { user, logout } = useAuth();

  const filteredNav = navigation.filter(
    item => item.roles.includes('ALL') || item.roles.includes(user!.role)
  );

  return (
    <div className="flex w-64 flex-col bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
      {/* Logo */}
      <div className="flex h-16 items-center px-6 border-b border-gray-200">
        <AnimatedLogo className="h-10" />
        <span className="ml-2 text-xl font-bold">Ativo Real</span>
      </div>

      {/* Navegação */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {filteredNav.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              `flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/50'
                  : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-gray-700'
              }`
            }
          >
            <item.icon className="mr-3 h-5 w-5" />
            {item.name}
          </NavLink>
        ))}
      </nav>

      {/* User Menu */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex items-center">
          <img
            src={user?.avatar || '/default-avatar.png'}
            alt={user?.name}
            className="h-10 w-10 rounded-full"
          />
          <div className="ml-3 flex-1">
            <p className="text-sm font-medium text-gray-700">{user?.name}</p>
            <p className="text-xs text-gray-500">{user?.email}</p>
          </div>
        </div>
        <button
          onClick={logout}
          className="mt-3 w-full rounded-lg bg-gray-100 px-3 py-2 text-sm text-gray-700 hover:bg-gray-200"
        >
          Sair
        </button>
      </div>
    </div>
  );
};
```

---

## 📊 GERENCIAMENTO DE ESTADO

### 1. Zustand Stores

```typescript
// src/stores/projectStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { projectsApi } from '@/services/projectsApi';

interface ProjectState {
  projects: Project[];
  currentProject: Project | null;
  isLoading: boolean;
  error: string | null;
  
  loadProjects: () => Promise<void>;
  setCurrentProject: (id: string) => void;
  createProject: (data: CreateProjectDto) => Promise<Project>;
  updateProject: (id: string, data: Partial<Project>) => Promise<void>;
  deleteProject: (id: string) => Promise<void>;
}

export const useProjectStore = create<ProjectState>()(
  persist(
    (set, get) => ({
      projects: [],
      currentProject: null,
      isLoading: false,
      error: null,

      loadProjects: async () => {
        set({ isLoading: true, error: null });
        try {
          const projects = await projectsApi.getAll();
          set({ projects, isLoading: false });
        } catch (error) {
          set({ error: error.message, isLoading: false });
        }
      },

      setCurrentProject: (id) => {
        const project = get().projects.find(p => p.id === id);
        set({ currentProject: project || null });
      },

      createProject: async (data) => {
        const newProject = await projectsApi.create(data);
        set(state => ({ projects: [...state.projects, newProject] }));
        return newProject;
      },

      updateProject: async (id, data) => {
        await projectsApi.update(id, data);
        set(state => ({
          projects: state.projects.map(p => p.id === id ? { ...p, ...data } : p)
        }));
      },

      deleteProject: async (id) => {
        await projectsApi.delete(id);
        set(state => ({
          projects: state.projects.filter(p => p.id !== id),
          currentProject: state.currentProject?.id === id ? null : state.currentProject
        }));
      }
    }),
    { name: 'project-store' }
  )
);
```

```typescript
// src/stores/mapStore.ts
import { create } from 'zustand';

interface MapState {
  map: Map | null;
  vectorSource: VectorSource | null;
  activeTool: 'draw' | 'modify' | 'snap' | 'measure' | null;
  features: Feature[];
  
  setMap: (map: Map) => void;
  setVectorSource: (source: VectorSource) => void;
  setActiveTool: (tool: MapState['activeTool']) => void;
  addFeature: (feature: Feature) => void;
  removeFeature: (id: string) => void;
  clearFeatures: () => void;
}

export const useMapStore = create<MapState>((set) => ({
  map: null,
  vectorSource: null,
  activeTool: null,
  features: [],

  setMap: (map) => set({ map }),
  setVectorSource: (source) => set({ vectorSource: source }),
  setActiveTool: (tool) => set({ activeTool: tool }),
  
  addFeature: (feature) => 
    set(state => ({ features: [...state.features, feature] })),
  
  removeFeature: (id) => 
    set(state => ({ features: state.features.filter(f => f.getId() !== id) })),
  
  clearFeatures: () => set({ features: [] })
}));
```

### 2. React Query para API

```typescript
// src/services/api.ts
import axios from 'axios';
import { QueryClient } from '@tanstack/react-query';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: 10000,
});

// Interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para refresh token em 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refresh = localStorage.getItem('refresh_token');
        const { data } = await axios.post('/api/auth/refresh', { refresh_token: refresh });
        
        localStorage.setItem('access_token', data.access_token);
        originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
        
        return api(originalRequest);
      } catch {
        // Redirect to login
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutos
    },
  },
});
```

```typescript
// src/hooks/useProjects.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { projectsApi } from '@/services/projectsApi';

export const useProjects = () => {
  const queryClient = useQueryClient();

  const { data: projects, isLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: projectsApi.getAll
  });

  const createMutation = useMutation({
    mutationFn: projectsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
    }
  });

  return {
    projects,
    isLoading,
    createProject: createMutation.mutate
  };
};
```

---

## 🔧 BACKEND: IMPLEMENTAÇÃO JWT

### 1. Middleware de Autenticação

```python
# novo-projeto/backend/auth_middleware.py
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from azure.functions import HttpRequest, HttpResponse
import json

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(user_id: int, role: str) -> str:
    """Cria JWT access token"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": expire,
        "type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    """Cria JWT refresh token"""
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "user_id": user_id,
        "exp": expire,
        "type": "refresh"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    """Verifica e decodifica JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")

def require_auth(func):
    """Decorator para proteger endpoints"""
    @wraps(func)
    def wrapper(req: HttpRequest, *args, **kwargs):
        auth_header = req.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return HttpResponse(
                json.dumps({"error": "Token não fornecido"}),
                status_code=401,
                mimetype="application/json"
            )
        
        token = auth_header.split(" ")[1]
        
        try:
            payload = verify_token(token)
            
            if payload.get("type") != "access":
                raise ValueError("Token inválido")
            
            # Adiciona user_id e role ao request
            req.user_id = payload["user_id"]
            req.user_role = payload["role"]
            
            return func(req, *args, **kwargs)
            
        except ValueError as e:
            return HttpResponse(
                json.dumps({"error": str(e)}),
                status_code=401,
                mimetype="application/json"
            )
    
    return wrapper

def require_role(*allowed_roles):
    """Decorator para verificar role"""
    def decorator(func):
        @wraps(func)
        def wrapper(req: HttpRequest, *args, **kwargs):
            if not hasattr(req, 'user_role'):
                return HttpResponse(
                    json.dumps({"error": "Usuário não autenticado"}),
                    status_code=401,
                    mimetype="application/json"
                )
            
            if req.user_role not in allowed_roles:
                return HttpResponse(
                    json.dumps({"error": "Permissão negada"}),
                    status_code=403,
                    mimetype="application/json"
                )
            
            return func(req, *args, **kwargs)
        
        return wrapper
    return decorator
```

### 2. Modelo de Usuário

```python
# novo-projeto/backend/models.py (adicionar)
import bcrypt
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, Enum
import enum

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    TOPOGRAFO = "TOPOGRAFO"
    CLIENTE = "CLIENTE"
    AGRICULTOR = "AGRICULTOR"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENTE)
    avatar = Column(String)
    
    # Controle
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    
    # Timestamps
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    atualizado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    ultimo_login = Column(TIMESTAMP)
    
    def set_password(self, password: str):
        """Hasheia senha com bcrypt"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Verifica senha"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
```

### 3. Endpoints de Autenticação

```python
# novo-projeto/backend/function_app.py (adicionar rotas)
import azure.functions as func
from auth_middleware import create_access_token, create_refresh_token, verify_token, require_auth
from models import User
from database import SessionLocal
from datetime import datetime

@app.route(route="auth/login", methods=["POST"])
def login(req: func.HttpRequest) -> func.HttpResponse:
    """Login endpoint"""
    try:
        body = req.get_json()
        email = body.get("email")
        password = body.get("password")
        
        if not email or not password:
            return func.HttpResponse(
                json.dumps({"error": "Email e senha são obrigatórios"}),
                status_code=400,
                mimetype="application/json"
            )
        
        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not user.check_password(password):
            return func.HttpResponse(
                json.dumps({"error": "Credenciais inválidas"}),
                status_code=401,
                mimetype="application/json"
            )
        
        if not user.is_active:
            return func.HttpResponse(
                json.dumps({"error": "Conta desativada"}),
                status_code=403,
                mimetype="application/json"
            )
        
        # Atualizar último login
        user.ultimo_login = datetime.utcnow()
        db.commit()
        
        # Gerar tokens
        access_token = create_access_token(user.id, user.role.value)
        refresh_token = create_refresh_token(user.id)
        
        return func.HttpResponse(
            json.dumps({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": 1800,  # 30 minutos
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role.value,
                    "avatar": user.avatar
                }
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()

@app.route(route="auth/refresh", methods=["POST"])
def refresh(req: func.HttpRequest) -> func.HttpResponse:
    """Refresh token endpoint"""
    try:
        body = req.get_json()
        refresh_token = body.get("refresh_token")
        
        if not refresh_token:
            return func.HttpResponse(
                json.dumps({"error": "Refresh token não fornecido"}),
                status_code=400,
                mimetype="application/json"
            )
        
        payload = verify_token(refresh_token)
        
        if payload.get("type") != "refresh":
            return func.HttpResponse(
                json.dumps({"error": "Token inválido"}),
                status_code=401,
                mimetype="application/json"
            )
        
        db = SessionLocal()
        user = db.query(User).filter(User.id == payload["user_id"]).first()
        
        if not user or not user.is_active:
            return func.HttpResponse(
                json.dumps({"error": "Usuário inválido"}),
                status_code=401,
                mimetype="application/json"
            )
        
        # Gerar novo access token
        access_token = create_access_token(user.id, user.role.value)
        
        return func.HttpResponse(
            json.dumps({
                "access_token": access_token,
                "token_type": "Bearer",
                "expires_in": 1800
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=401,
            mimetype="application/json"
        )
    finally:
        db.close()

@app.route(route="auth/me", methods=["GET"])
@require_auth
def get_current_user(req: func.HttpRequest) -> func.HttpResponse:
    """Retorna dados do usuário autenticado"""
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.id == req.user_id).first()
        
        return func.HttpResponse(
            json.dumps({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role.value,
                "avatar": user.avatar
            }),
            status_code=200,
            mimetype="application/json"
        )
    finally:
        db.close()
```

### 4. Proteger Endpoints Existentes

```python
# Exemplo de proteção de endpoints
from auth_middleware import require_auth, require_role

@app.route(route="projetos", methods=["GET"])
@require_auth
def listar_projetos(req: func.HttpRequest) -> func.HttpResponse:
    """Lista projetos do usuário autenticado"""
    db = SessionLocal()
    try:
        # req.user_id está disponível graças ao @require_auth
        projetos = db.query(Projeto).filter(
            Projeto.criado_por == req.user_id
        ).all()
        
        return func.HttpResponse(
            json.dumps([p.to_dict() for p in projetos]),
            status_code=200,
            mimetype="application/json"
        )
    finally:
        db.close()

@app.route(route="admin/users", methods=["GET"])
@require_auth
@require_role("ADMIN")
def listar_usuarios(req: func.HttpRequest) -> func.HttpResponse:
    """Lista todos usuários (apenas ADMIN)"""
    # Endpoint protegido por role
    pass
```

---

## 📋 MIGRATION SQL - TABELA USERS

```sql
-- novo-projeto/database/init/04_users_auth.sql

-- Enum de roles
DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('ADMIN', 'TOPOGRAFO', 'CLIENTE', 'AGRICULTOR');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role DEFAULT 'CLIENTE',
    avatar VARCHAR(500),
    
    -- Controle
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_login TIMESTAMP,
    
    -- Índices
    CONSTRAINT check_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- Trigger para atualizar 'atualizado_em'
CREATE TRIGGER trigger_update_users 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE PROCEDURE update_updated_at();

-- Usuário admin padrão (senha: admin123 - MUDAR EM PRODUÇÃO!)
INSERT INTO users (name, email, password_hash, role, is_active, email_verified)
VALUES (
    'Administrador',
    'admin@ativoreal.com.br',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5/d8xQK8wd92u', -- bcrypt hash de 'admin123'
    'ADMIN',
    TRUE,
    TRUE
)
ON CONFLICT (email) DO NOTHING;

-- Relacionamentos com outras tabelas
ALTER TABLE projetos ADD COLUMN IF NOT EXISTS criado_por INTEGER REFERENCES users(id);
ALTER TABLE assinaturas DROP COLUMN IF EXISTS usuario_id;
ALTER TABLE assinaturas ADD COLUMN IF NOT EXISTS usuario_id INTEGER REFERENCES users(id);

COMMENT ON TABLE users IS 'Usuários do sistema com autenticação JWT';
COMMENT ON COLUMN users.password_hash IS 'Hash bcrypt da senha';
COMMENT ON COLUMN users.role IS 'Perfil de acesso (ADMIN, TOPOGRAFO, CLIENTE, AGRICULTOR)';
```

---

## 🎯 ROADMAP DE IMPLEMENTAÇÃO

### FASE 1: FUNDAÇÃO (2 semanas)
**Objetivo**: Setup de autenticação e estado global

**Checklist**:
- [ ] 1.1 Backend: Migration SQL de `users` table
- [ ] 1.2 Backend: Implementar `auth_middleware.py`
- [ ] 1.3 Backend: Endpoints de auth (`/login`, `/refresh`, `/me`)
- [ ] 1.4 Backend: Adicionar bcrypt às dependencies
- [ ] 1.5 Frontend: Criar `AuthContext.tsx`
- [ ] 1.6 Frontend: Página de login funcional
- [ ] 1.7 Frontend: Componente `ProtectedRoute`
- [ ] 1.8 Frontend: Instalar Zustand + React Query
- [ ] 1.9 Frontend: Setup de `api.ts` com interceptors
- [ ] 1.10 Testar fluxo completo de login/logout

**Entregável**: Sistema de autenticação funcionando end-to-end

---

### FASE 2: ESTRUTURA SINGLE-PAGE (2 semanas)
**Objetivo**: Layout principal e navegação

**Checklist**:
- [ ] 2.1 Frontend: Criar `AppLayout.tsx`
- [ ] 2.2 Frontend: Criar `Sidebar.tsx` com navegação
- [ ] 2.3 Frontend: Criar `Header.tsx` com user menu
- [ ] 2.4 Frontend: Reorganizar rotas em `App.tsx`
- [ ] 2.5 Frontend: Implementar lazy loading de módulos
- [ ] 2.6 Frontend: Migrar `LandingPage` para `landing/`
- [ ] 2.7 Frontend: Adicionar `RoleBasedDashboard` component
- [ ] 2.8 Frontend: Sistema de notificações (Toast)
- [ ] 2.9 Frontend: Loading states e Skeletons
- [ ] 2.10 Testar navegação entre módulos

**Entregável**: SPA funcionando com layout completo

---

### FASE 3: REFATORAÇÃO DO MAPA (3 semanas)
**Objetivo**: Modularizar GlobalMap

**Checklist**:
- [ ] 3.1 Criar estrutura `app/modules/map/`
- [ ] 3.2 Extrair `MapCore.tsx` (setup OpenLayers)
- [ ] 3.3 Extrair `MapToolbar.tsx` (ferramentas)
- [ ] 3.4 Extrair `MapLayers.tsx` (gestão de camadas)
- [ ] 3.5 Extrair `MapPopup.tsx`
- [ ] 3.6 Extrair `MapImport.tsx`
- [ ] 3.7 Extrair `MapExport.tsx`
- [ ] 3.8 Criar hooks: `useMapSetup`, `useMapTools`, `useMapImport`
- [ ] 3.9 Criar `mapStore.ts` com Zustand
- [ ] 3.10 Migrar persistência de localStorage para backend
- [ ] 3.11 Implementar Web Worker para processamento de Shapefile
- [ ] 3.12 Adicionar Error Boundaries
- [ ] 3.13 Testes unitários dos hooks
- [ ] 3.14 Documentação dos componentes

**Entregável**: Mapa modular, testável e performático

---

### FASE 4: MÓDULOS DE NEGÓCIO (2 semanas)
**Objetivo**: Implementar dashboards e gestão

**Checklist**:
- [ ] 4.1 Dashboard Topógrafo refatorado
- [ ] 4.2 Módulo de Projetos (`ProjectList`, `ProjectDetail`)
- [ ] 4.3 Módulo de Assinaturas (`SubscriptionDashboard`)
- [ ] 4.4 Integração com endpoints Pay-as-you-go
- [ ] 4.5 Criar `projectStore.ts`
- [ ] 4.6 Implementar React Query em todos módulos
- [ ] 4.7 Modal de criação de projetos
- [ ] 4.8 Sistema de filtros e busca
- [ ] 4.9 Métricas e KPIs

**Entregável**: Módulos de negócio funcionais

---

### FASE 5: PROTEÇÃO DE ENDPOINTS (1 semana)
**Objetivo**: Segurança backend

**Checklist**:
- [ ] 5.1 Adicionar `@require_auth` em todos endpoints
- [ ] 5.2 Implementar RBAC com `@require_role`
- [ ] 5.3 Atualizar endpoints de projetos com filtro por `user_id`
- [ ] 5.4 Atualizar endpoints de assinaturas com filtro por `user_id`
- [ ] 5.5 Testes de permissões
- [ ] 5.6 Documentação de rotas e roles

**Entregável**: Backend seguro e auditável

---

### FASE 6: CONSOLIDAÇÃO E OTIMIZAÇÃO (2 semanas)
**Objetivo**: Performance e qualidade

**Checklist**:
- [ ] 6.1 Remover frontend simplificado (`frontend/`)
- [ ] 6.2 Code splitting e lazy loading
- [ ] 6.3 Otimizar bundle size
- [ ] 6.4 Implementar PWA (offline support)
- [ ] 6.5 Adicionar ESLint + Prettier
- [ ] 6.6 Testes E2E com Playwright
- [ ] 6.7 Lighthouse audit (performance)
- [ ] 6.8 Documentação completa (Storybook?)
- [ ] 6.9 CI/CD pipeline
- [ ] 6.10 Deploy em staging

**Entregável**: Aplicação otimizada e documentada

---

## 📊 MATRIZ DE PERMISSÕES (RBAC)

| Endpoint | ADMIN | TOPOGRAFO | CLIENTE | AGRICULTOR |
|----------|-------|-----------|---------|------------|
| `GET /projetos` | Todos | Próprios | Próprios | Próprios |
| `POST /projetos` | ✅ | ✅ | ❌ | ❌ |
| `GET /lotes` | Todos | Próprios | Próprios | Próprios |
| `POST /lotes` | ✅ | ✅ | ❌ | ❌ |
| `GET /assinaturas` | Todas | Própria | Própria | Própria |
| `POST /assinaturas` | ✅ | ✅ | ✅ | ✅ |
| `GET /planos` | ✅ | ✅ | ✅ | ✅ |
| `POST /planos` | ✅ | ❌ | ❌ | ❌ |
| `GET /admin/*` | ✅ | ❌ | ❌ | ❌ |
| `POST /ai/chat` | ✅ | ✅ | ✅ | ✅ |
| `POST /pagamentos` | ✅ | ✅ | ✅ | ✅ |

---

## 🔍 ANTES vs DEPOIS

### ANTES (Arquitetura Atual)

```
┌─────────────────┐     ┌─────────────────┐
│  ativo-real/    │     │   frontend/     │
│  (TypeScript)   │     │   (JavaScript)  │
│  7000+ linhas   │     │   500 linhas    │
└─────────────────┘     └─────────────────┘
        │                       │
        └───────┬───────────────┘
                │
        ┌───────▼────────┐
        │  Azure Functions│
        │  (15 endpoints) │
        │  🔓 ANONYMOUS   │
        └────────────────┘
                │
        ┌───────▼────────┐
        │  PostgreSQL    │
        └────────────────┘

❌ Problemas:
- Duplicação de código
- Props drilling
- Sem autenticação real
- localStorage como DB
- GlobalMap monolítico
```

### DEPOIS (Arquitetura Proposta)

```
┌──────────────────────────────────────┐
│  ATIVO REAL SPA (Único Frontend)     │
│  ┌──────────┬─────────────────────┐  │
│  │ Sidebar  │  Router Outlet      │  │
│  │ Fixo     │  (Lazy Loaded)      │  │
│  ├──────────┼─────────────────────┤  │
│  │🏠 Dashbd │  <DashboardModule>  │  │
│  │🗺️ Mapa   │  <MapModule>        │  │
│  │📁 Project│  <ProjectsModule>   │  │
│  │💳 Planos │  <SubscriptModule>  │  │
│  └──────────┴─────────────────────┘  │
│                                       │
│  Estado: Zustand + React Query       │
│  Auth: Context API + JWT             │
└──────────────────────────────────────┘
                │
                │ Authorization: Bearer {JWT}
                │
        ┌───────▼────────┐
        │  Azure Functions│
        │  🔒 @require_auth│
        │  🔐 @require_role│
        └────────────────┘
                │
        ┌───────▼────────┐
        │  PostgreSQL    │
        │  + users table │
        └────────────────┘

✅ Benefícios:
- Código único e organizado
- Estado global centralizado
- JWT com RBAC
- Backend seguro
- Componentes modulares (<300 linhas)
```

---

## 📈 MÉTRICAS DE SUCESSO

| Métrica | Antes | Depois (Meta) |
|---------|-------|---------------|
| Frontends ativos | 2 | 1 |
| Linhas por componente (média) | 650 | <250 |
| Props drilling depth | 5+ níveis | 0 |
| Tempo de autenticação | localStorage (0 seg) | JWT (0.5 seg) |
| Segurança de endpoints | 0/15 protegidos | 15/15 protegidos |
| Bundle size | 2.5 MB | <1.8 MB |
| Lighthouse Performance | 65 | >90 |
| Test Coverage | 0% | >70% |

---

## 🚨 RISCOS E MITIGAÇÕES

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Quebra de features existentes | Média | Alto | Testes E2E antes de refatorar |
| Performance degradada | Baixa | Médio | Lazy loading + code splitting |
| Resistência da equipe | Baixa | Baixo | Documentação + treinamento |
| Atraso no cronograma | Média | Médio | Fases incrementais, entregas parciais |
| Bugs em produção | Média | Alto | Staging environment + QA |

---

## 💡 RECOMENDAÇÕES FINAIS

### Prioridade CRÍTICA 🔴
1. **Implementar autenticação JWT** - Vulnerabilidade de segurança atual
2. **Consolidar em um único frontend** - Reduzir débito técnico
3. **Refatorar GlobalMap** - Manutenibilidade crítica

### Prioridade ALTA 🟠
4. **Implementar estado global** - Melhorar DX e UX
5. **Proteger todos endpoints** - Segurança backend
6. **Adicionar testes** - Garantir qualidade

### Prioridade MÉDIA 🟡
7. **Otimizar performance** - Melhorar UX
8. **Documentar componentes** - Facilitar onboarding
9. **CI/CD automatizado** - Agilizar deploys

### Opcional ⚪
10. **PWA offline support** - Funcionalidade extra
11. **Storybook** - Design system
12. **Analytics** - Métricas de uso

---

## 📞 PRÓXIMOS PASSOS

1. **Validar proposta** com stakeholders
2. **Criar branch `refactor/single-page-auth`**
3. **Começar FASE 1** (Autenticação)
4. **Review semanal** de progresso
5. **Deploy incremental** em staging

---

**Documento criado por**: GitHub Copilot (Análise Automatizada)  
**Data**: 31 de Janeiro de 2026  
**Versão**: 2.0  
**Status**: 🟢 Pronto para implementação
