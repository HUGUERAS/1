/**
 * src/services/api.ts
 * Typed API client for backend communication
 */

const API_BASE = '/api';

// ============ Types ============

export interface User {
  id: string;
  email: string;
  nome: string;
  role: 'TOPOGRAFO' | 'CLIENTE';
}

export interface Project {
  id: string;
  nome: string;
  tipo: 'INDIVIDUAL' | 'DESMEMBRAMENTO' | 'LOTEAMENTO';
  status: 'RASCUNHO' | 'ATIVO' | 'CONCLUÍDO' | 'CANCELADO';
  area_ha: number;
  municipio: string;
}

export interface Lot {
  id: string;
  project_id: string;
  nome_cliente: string;
  email_cliente: string;
  status: 'PENDENTE' | 'PAGO' | 'PROCESSANDO' | 'FINALIZADO' | 'CANCELADO';
  token_acesso: string;
  area_ha: number;
}

export interface Payment {
  id: string;
  lot_id: string;
  valor_total: number;
  status: 'PENDENTE' | 'PROCESSANDO' | 'APROVADO' | 'RECUSADO';
}

export interface WmsLayer {
  id: string;
  nome: string;
  url: string;
  visivel: boolean;
  opacidade: number;
}

// ============ Auth Endpoints ============

export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
    }
    return data;
  },

  logout: async () => {
    await fetch(`${API_BASE}/auth/logout`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    localStorage.removeItem('access_token');
  },

  refresh: async () => {
    const response = await fetch(`${API_BASE}/auth/refresh`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    const data = await response.json();
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
    }
    return data;
  },
};

// ============ Project Endpoints ============

export const projectAPI = {
  list: async () => {
    return fetchAPI<Project[]>(`${API_BASE}/projects`, { method: 'GET' });
  },

  create: async (project: Partial<Project>) => {
    return fetchAPI<Project>(`${API_BASE}/projects`, {
      method: 'POST',
      body: JSON.stringify(project),
    });
  },

  get: async (id: string) => {
    return fetchAPI<Project>(`${API_BASE}/projects/${id}`, { method: 'GET' });
  },

  update: async (id: string, project: Partial<Project>) => {
    return fetchAPI<Project>(`${API_BASE}/projects/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(project),
    });
  },

  delete: async (id: string) => {
    return fetchAPI(`${API_BASE}/projects/${id}`, { method: 'DELETE' });
  },
};

// ============ Lot Endpoints ============

export const lotAPI = {
  list: async (projectId: string) => {
    return fetchAPI<Lot[]>(`${API_BASE}/projects/${projectId}/lots`, {
      method: 'GET',
    });
  },

  create: async (projectId: string, lot: Partial<Lot>) => {
    return fetchAPI<Lot & { token_acesso: string }>(
      `${API_BASE}/projects/${projectId}/lots`,
      {
        method: 'POST',
        body: JSON.stringify(lot),
      }
    );
  },

  getByToken: async (token: string) => {
    return fetchAPI<Lot>(`${API_BASE}/lots/${token}/details`, {
      method: 'GET',
      public: true, // No auth required
    });
  },

  update: async (id: string, lot: Partial<Lot>) => {
    return fetchAPI<Lot>(`${API_BASE}/lots/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(lot),
    });
  },
};

// ============ Payment Endpoints ============

export const paymentAPI = {
  create: async (payload: {
    lot_id: string;
    valor_total: number;
    customer_email: string;
  }) => {
    return fetchAPI<{
      payment_id: string;
      payment_url: string;
    }>(`${API_BASE}/payments/create`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  getStatus: async (paymentId: string) => {
    return fetchAPI<Payment>(`${API_BASE}/payments/${paymentId}/status`, {
      method: 'GET',
    });
  },

  getLotStatus: async (token: string) => {
    return fetchAPI<{ lot_status: string; payment_status: string }>(
      `${API_BASE}/lots/${token}/status`,
      {
        method: 'GET',
        public: true,
      }
    );
  },
};

// ============ WMS Layers Endpoints ============

export const wmsAPI = {
  list: async (projectId: string) => {
    return fetchAPI<WmsLayer[]>(`${API_BASE}/projects/${projectId}/wms-layers`, {
      method: 'GET',
    });
  },

  create: async (projectId: string, layer: Partial<WmsLayer>) => {
    return fetchAPI<WmsLayer>(`${API_BASE}/projects/${projectId}/wms-layers`, {
      method: 'POST',
      body: JSON.stringify(layer),
    });
  },

  update: async (projectId: string, layerId: string, layer: Partial<WmsLayer>) => {
    return fetchAPI<WmsLayer>(
      `${API_BASE}/projects/${projectId}/wms-layers/${layerId}`,
      {
        method: 'PATCH',
        body: JSON.stringify(layer),
      }
    );
  },

  delete: async (projectId: string, layerId: string) => {
    return fetchAPI(
      `${API_BASE}/projects/${projectId}/wms-layers/${layerId}`,
      { method: 'DELETE' }
    );
  },
};

// ============ Utility Functions ============

function getAuthHeaders() {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
  };
}

async function fetchAPI<T = any>(
  url: string,
  options: RequestInit & { public?: boolean } = {}
): Promise<T> {
  const { public: isPublic = false, ...fetchOptions } = options;

  const response = await fetch(url, {
    ...fetchOptions,
    headers: isPublic ? { 'Content-Type': 'application/json' } : getAuthHeaders(),
  });

  if (response.status === 401 && !isPublic) {
    // Token expired, try refresh
    await authAPI.refresh();
    return fetchAPI<T>(url, options);
  }

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

// ============ NEW ENDPOINTS (Chat, Status, Files) ============

export const chatAPI = {
  sendMessage: async (data: {
    projeto_id: number;
    sender_id: number;
    sender_role: string;
    message: string;
  }) => {
    return fetchAPI(`${API_BASE}/chat/messages`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  getMessages: async (projetoId: number, limit: number = 50) => {
    return fetchAPI(`${API_BASE}/chat/messages?projeto_id=${projetoId}&limit=${limit}`, {
      method: 'GET',
    });
  },
};

export const statusAPI = {
  getHistory: async (loteId: number) => {
    return fetchAPI(`${API_BASE}/lotes/${loteId}/status-history`, {
      method: 'GET',
    });
  },
};

export const fileAPI = {
  upload: async (data: {
    lote_id: number;
    nome: string;
    tipo: string;
    tamanho_kb: number;
    conteudo_base64: string;
    metadata?: any;
  }) => {
    return fetchAPI(`${API_BASE}/arquivos`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};

export const magicLinkAPI = {
  validate: async (token: string) => {
    return fetchAPI(`${API_BASE}/auth/magic-link/${token}`, {
      method: 'GET',
      public: true,
    });
  },
};

