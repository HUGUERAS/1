// Service to communicate with Azure Functions backend
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:7071/api';

export const api = {
  // Projetos
  getProjetos: async () => {
    const response = await fetch(`${API_URL}/projetos`);
    if (!response.ok) throw new Error('Falha ao buscar projetos');
    return response.json();
  },

  createProjeto: async (data) => {
    const response = await fetch(`${API_URL}/projetos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Falha ao criar projeto');
    return response.json();
  },

  getProjetoById: async (id) => {
    const response = await fetch(`${API_URL}/projetos/${id}`);
    if (!response.ok) throw new Error('Falha ao buscar projeto');
    return response.json();
  },

  // Lotes
  getLotes: async (projetoId) => {
    const url = projetoId ? `${API_URL}/lotes?projeto_id=${projetoId}` : `${API_URL}/lotes`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Falha ao buscar lotes');
    return response.json();
  },

  createLote: async (loteData) => {
    const response = await fetch(`${API_URL}/lotes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(loteData),
    });
    
    // Azure Functions returns 400/409 for validation errors
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || 'Falha ao criar lote');
    }
    return response.json();
  }
};
