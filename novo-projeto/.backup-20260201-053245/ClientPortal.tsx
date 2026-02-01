// @ts-nocheck
import React, { useState, useEffect } from 'react';
import { GlobalMap } from './GlobalMap';
import { ClientForm } from './ClientForm';
import { ChatWidget } from './ChatWidget';
import { StatusTimeline } from './StatusTimeline';
import { FileUploader } from './FileUploader';
import { ContractViewer } from './ContractViewer';

/**
 * ClientPortal.tsx - VERSÃO COMPLETA
 * Portal único do cliente com todas funcionalidades integradas
 * Acesso via magic link (token UUID)
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

export const ClientPortal: React.FC<ClientPortalProps> = ({ token }) => {
  const [lot, setLot] = useState<LotData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentUserId, setCurrentUserId] = useState<number>(0);
  const [activeTab, setActiveTab] = useState<'form' | 'map' | 'contract' | 'timeline' | 'files'>('form');

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

      // Salvar JWT
      localStorage.setItem('client_token', data.access_token);
      setLot(data.lote);
      setCurrentUserId(data.lote.id);
      setLoading(false);
    } catch (err) {
      setError('Erro ao validar link. Tente novamente.');
      setLoading(false);
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
        const updatedLot = await response.json();
        setLot(updatedLot);
        alert('✅ Dados salvos com sucesso!');
      }
    } catch (error) {
      alert('❌ Erro ao salvar dados. Tente novamente.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="text-4xl mb-4">⏳</div>
          <p className="text-gray-600">Carregando seu portal...</p>
        </div>
      </div>
    );
  }

  if (error || !lot) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-lg max-w-md text-center">
          <div className="text-6xl mb-4">🚫</div>
          <h2 className="text-2xl font-bold text-red-600 mb-2">Acesso Negado</h2>
          <p className="text-gray-700">{error || 'Link inválido ou expirado.'}</p>
          <p className="text-sm text-gray-500 mt-4">
            Entre em contato com o topógrafo responsável para obter um novo link.
          </p>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'form', label: '📋 Dados', icon: '📋' },
    { id: 'map', label: '🗺️ Mapa', icon: '🗺️' },
    { id: 'contract', label: '📄 Contrato', icon: '📄' },
    { id: 'timeline', label: '📜 Andamento', icon: '📜' },
    { id: 'files', label: '📂 Arquivos', icon: '📂' },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">🏠 Portal do Cliente</h1>
              <p className="text-sm text-gray-600 mt-1">
                Lote #{lot.id} • Status: <span className="font-semibold">{lot.status}</span>
              </p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">{lot.nome_cliente || 'Cliente'}</p>
              <p className="text-xs text-gray-500">
                Área: {lot.area_ha?.toFixed(2) || '—'} ha
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex space-x-2 overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-6 py-3 font-medium text-sm whitespace-nowrap transition-colors ${activeTab === tab.id
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
                  }`}
              >
                {tab.icon} {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'form' && (
          <ClientForm
            initialData={{
              nome_cliente: lot.nome_cliente,
              cpf_cnpj_cliente: lot.cpf_cnpj_cliente,
              telefone_cliente: lot.telefone_cliente,
              endereco: lot.endereco,
            }}
            onSubmit={handleFormSubmit}
          />
        )}

        {activeTab === 'map' && (
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">🗺️ Visualização do Lote</h2>
            <div className="h-[600px] rounded-lg overflow-hidden border">
              <GlobalMap
                drawMode="none"
                readOnly={true}
                // @ts-ignore - initialGeometry prop to be added to interface
                initialGeometry={lot.geom}
              />
            </div>
            <p className="text-sm text-gray-600 mt-4">
              📍 Use o mapa para visualizar a localização do seu lote. Para desenhar ou editar,
              solicite acesso ao topógrafo via chat.
            </p>
          </div>
        )}

        {activeTab === 'contract' && (
          <ContractViewer
            contratoUrl={lot.contrato_url}
            loteId={lot.id}
            clienteNome={lot.nome_cliente}
          />
        )}

        {activeTab === 'timeline' && <StatusTimeline loteId={lot.id} />}

        {activeTab === 'files' && (
          <FileUploader
            loteId={lot.id}
            onUploadSuccess={(file) => {
              console.log('Arquivo enviado:', file);
            }}
          />
        )}
      </main>

      {/* Chat Widget (sempre visível) */}
      <ChatWidget
        projetoId={lot.projeto_id}
        currentUserId={currentUserId}
        currentUserRole="CLIENTE"
      />

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-sm text-gray-600">
          <p>
            Em caso de dúvidas, entre em contato via chat 💬 ou pelo telefone do topógrafo.
          </p>
          <p className="mt-2 text-xs text-gray-500">
            Portal criado em {new Date(lot.criado_em).toLocaleDateString('pt-BR')}
          </p>
        </div>
      </footer>
    </div>
  );
};

