// @ts-nocheck
import React, { useState, useEffect } from 'react';
import { GlobalMap } from './GlobalMap';
import { ClientForm } from './ClientForm';
import { ChatWidget } from './ChatWidget';
import { StatusTimeline } from './StatusTimeline';
import { FileUploader } from './FileUploader';
import { ContractViewer } from './ContractViewer';

/**
 * ClientPortal - SINGLE PAGE APPLICATION
 * 
 * Uma ÚNICA página com 7 abas:
 * 1. Dashboard (stats + quick actions)
 * 2. Meus Dados (formulário)
 * 3. Mapa (visualização lote)
 * 4. Confrontantes (kanban 4 colunas)
 * 5. Contrato (viewer PDF)
 * 6. Andamento (timeline)
 * 7. Documentos (upload/download)
 */

interface ClientPortalProps {
  token: string;
}

interface LotData {
  id: number;
  projeto_id: number;
  nome_cliente: string;
  email_cliente: string;
  telefone_cliente: string;
  cpf_cnpj_cliente: string;
  endereco: string;
  status: string;
  area_ha: number;
  contrato_url: string;
  geom: any;
  criado_em: string;
}

interface Confrontante {
  id: number;
  nome: string;
  contato: string;
  status: 'Identificado' | 'Contatado' | 'Assinado' | 'Litígio';
}

export const ClientPortal: React.FC<ClientPortalProps> = ({ token }) => {
  const [lot, setLot] = useState<LotData | null>(null);
  const [confrontantes, setConfrontantes] = useState<Confrontante[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'form' | 'map' | 'neighbors' | 'contract' | 'timeline' | 'files'>('dashboard');

  useEffect(() => {
    validateMagicLink();
  }, [token]);

  const validateMagicLink = async () => {
    try {
      const response = await fetch(`/api/auth/magic-link/${token}`);
      const data = await response.json();

      if (!data.valid) {
        setError(data.error || 'Link inválido ou expirado');
        setLoading(false);
        return;
      }

      localStorage.setItem('client_token', data.access_token);
      setLot(data.lote);
      loadConfrontantes(data.lote.id);
      setLoading(false);
    } catch (err) {
      setError('Erro ao validar link');
      setLoading(false);
    }
  };

  const loadConfrontantes = async (loteId: number) => {
    try {
      const response = await fetch(`/api/lotes/${loteId}/confrontantes`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('client_token')}` },
      });
      if (response.ok) {
        setConfrontantes(await response.json());
      }
    } catch (err) {
      console.error('Erro ao carregar confrontantes:', err);
    }
  };

  const handleFormSubmit = async (formData: any) => {
    try {
      const response = await fetch(`/api/lotes/${lot?.id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('client_token')}`,
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setLot(await response.json());
        alert('✅ Dados salvos!');
      }
    } catch (error) {
      alert('❌ Erro ao salvar');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-bounce">⏳</div>
          <p className="text-xl text-gray-700 font-medium">Carregando seu portal...</p>
        </div>
      </div>
    );
  }

  if (error || !lot) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-pink-100">
        <div className="bg-white p-10 rounded-2xl shadow-2xl max-w-md text-center">
          <div className="text-7xl mb-4">🚫</div>
          <h2 className="text-3xl font-bold text-red-600 mb-4">Acesso Negado</h2>
          <p className="text-gray-700">{error || 'Link inválido'}</p>
        </div>
      </div>
    );
  }

  const stats = [
    { label: 'Área Total', value: `${lot.area_ha?.toFixed(2) || '—'} ha`, icon: '📏' },
    { label: 'Status', value: lot.status, icon: '📊' },
    { label: 'Confrontantes', value: confrontantes.length, icon: '👥' },
    { label: 'Progresso', value: '75%', icon: '⚡' },
  ];

  const kanbanColumns = {
    'Identificado': { color: 'border-yellow-400', bg: 'bg-yellow-50' },
    'Contatado': { color: 'border-blue-400', bg: 'bg-blue-50' },
    'Assinado': { color: 'border-green-400', bg: 'bg-green-50' },
    'Litígio': { color: 'border-red-400', bg: 'bg-red-50' },
  };

  const getConfrontantesByStatus = (status: string) =>
    confrontantes.filter((c) => c.status === status);

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'form', label: 'Meus Dados', icon: '📋' },
    { id: 'map', label: 'Mapa', icon: '🗺️' },
    { id: 'neighbors', label: 'Confrontantes', icon: '👥' },
    { id: 'contract', label: 'Contrato', icon: '📄' },
    { id: 'timeline', label: 'Andamento', icon: '📜' },
    { id: 'files', label: 'Documentos', icon: '📂' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <header className="bg-white shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="text-3xl">🏠</div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Portal do Cliente</h1>
                <p className="text-sm text-gray-600">Lote #{lot.id} • {lot.nome_cliente}</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-lg font-semibold">{lot.status}</p>
              <p className="text-sm text-gray-600">{lot.area_ha?.toFixed(2)} ha</p>
            </div>
          </div>
        </div>

        <nav className="bg-gradient-to-r from-blue-600 to-indigo-600">
          <div className="max-w-7xl mx-auto px-6">
            <div className="flex space-x-1 overflow-x-auto">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`px-6 py-3 font-medium text-sm whitespace-nowrap transition-all ${
                    activeTab === tab.id
                      ? 'bg-white text-blue-600 rounded-t-lg shadow-lg'
                      : 'text-white hover:bg-white/10'
                  }`}
                >
                  {tab.icon} {tab.label}
                </button>
              ))}
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {activeTab === 'dashboard' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {stats.map((stat, idx) => (
                <div key={idx} className="bg-white p-6 rounded-xl shadow-md">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">{stat.label}</p>
                      <p className="text-2xl font-bold">{stat.value}</p>
                    </div>
                    <div className="text-4xl">{stat.icon}</div>
                  </div>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <button onClick={() => setActiveTab('form')} className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6 rounded-xl shadow-lg">
                <div className="text-4xl mb-3">📋</div>
                <h3 className="text-xl font-bold">Atualizar Dados</h3>
              </button>
              <button onClick={() => setActiveTab('map')} className="bg-gradient-to-r from-green-500 to-green-600 text-white p-6 rounded-xl shadow-lg">
                <div className="text-4xl mb-3">🗺️</div>
                <h3 className="text-xl font-bold">Ver no Mapa</h3>
              </button>
              <button onClick={() => setActiveTab('neighbors')} className="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-6 rounded-xl shadow-lg">
                <div className="text-4xl mb-3">👥</div>
                <h3 className="text-xl font-bold">Confrontantes</h3>
              </button>
            </div>
          </div>
        )}

        {activeTab === 'form' && (
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <h2 className="text-2xl font-bold mb-6">📋 Meus Dados</h2>
            <ClientForm initialData={lot} onSubmit={handleFormSubmit} />
          </div>
        )}

        {activeTab === 'map' && (
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <h2 className="text-2xl font-bold mb-6">🗺️ Mapa do Lote</h2>
            <div className="h-[600px] rounded-lg overflow-hidden border-4 border-blue-200">
              <GlobalMap drawMode="none" readOnly={true} initialGeometry={lot.geom} />
            </div>
          </div>
        )}

        {activeTab === 'neighbors' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {Object.entries(kanbanColumns).map(([status, styles]) => {
                const cards = getConfrontantesByStatus(status);
                return (
                  <div key={status} className={`${styles.bg} p-6 rounded-xl min-h-[400px]`}>
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-bold">{status}</h3>
                      <span className="bg-white px-3 py-1 rounded-full text-sm font-semibold">{cards.length}</span>
                    </div>
                    <div className="space-y-3">
                      {cards.map((card) => (
                        <div key={card.id} className={`bg-white p-4 rounded-lg shadow border-l-4 ${styles.color}`}>
                          <p className="font-semibold">{card.nome}</p>
                          <p className="text-sm text-gray-600">{card.contato}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {activeTab === 'contract' && (
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <h2 className="text-2xl font-bold mb-6">📄 Contrato</h2>
            <ContractViewer contratoUrl={lot.contrato_url} loteId={lot.id} />
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <h2 className="text-2xl font-bold mb-6">📜 Andamento</h2>
            <StatusTimeline loteId={lot.id} />
          </div>
        )}

        {activeTab === 'files' && (
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <h2 className="text-2xl font-bold mb-6">📂 Documentos</h2>
            <FileUploader loteId={lot.id} />
          </div>
        )}
      </main>

      <ChatWidget userId={lot.id} userName={lot.nome_cliente} projetoId={lot.projeto_id} role="CLIENTE" />
    </div>
  );
};
