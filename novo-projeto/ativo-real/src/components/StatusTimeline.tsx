import React, { useState, useEffect } from 'react';

/**
 * StatusTimeline.tsx
 * Timeline visual do histórico de status do lote
 */

interface StatusHistoryItem {
  id: number;
  status_anterior: string | null;
  status_novo: string;
  observacao?: string;
  alterado_por?: number;
  criado_em: string;
}

interface StatusTimelineProps {
  loteId: number;
}

const STATUS_LABELS: Record<string, { label: string; icon: string; color: string }> = {
  PENDENTE: { label: 'Pendente', icon: '⏳', color: 'gray' },
  DESENHO: { label: 'Em Desenho', icon: '✏️', color: 'blue' },
  VALIDACAO_SIGEF: { label: 'Validação SIGEF', icon: '🔍', color: 'yellow' },
  CONTRATO_PENDENTE: { label: 'Contrato Pendente', icon: '📄', color: 'orange' },
  AGUARDANDO_PAGAMENTO: { label: 'Aguardando Pagamento', icon: '💳', color: 'purple' },
  PAGO: { label: 'Pago', icon: '✅', color: 'green' },
  FINALIZADO: { label: 'Finalizado', icon: '🎉', color: 'green' },
};

export const StatusTimeline: React.FC<StatusTimelineProps> = ({ loteId }) => {
  const [history, setHistory] = useState<StatusHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(`/api/lotes/${loteId}/status-history`);
        if (response.ok) {
          const data = await response.json();
          setHistory(data);
        }
      } catch (error) {
        console.error('Erro ao buscar histórico:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [loteId]);

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusInfo = (status: string) => {
    return STATUS_LABELS[status] || { label: status, icon: '📌', color: 'gray' };
  };

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <p className="text-gray-500">Carregando histórico...</p>
      </div>
    );
  }

  if (history.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">📜 Histórico do Serviço</h3>
        <p className="text-gray-500">Nenhum histórico registrado ainda.</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-6">📜 Acompanhamento do Serviço</h3>

      <div className="relative">
        {/* Vertical Line */}
        <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-300"></div>

        {/* Timeline Items */}
        <div className="space-y-6">
          {history.map((item, index) => {
            const statusInfo = getStatusInfo(item.status_novo);
            const isLast = index === history.length - 1;

            return (
              <div key={item.id} className="relative pl-12">
                {/* Icon Circle */}
                <div
                  className={`absolute left-0 w-8 h-8 rounded-full flex items-center justify-center text-white ${isLast ? 'bg-blue-600 ring-4 ring-blue-200' : 'bg-gray-400'
                    }`}
                >
                  <span className="text-sm">{statusInfo.icon}</span>
                </div>

                {/* Content */}
                <div
                  className={`bg-gray-50 rounded-lg p-4 ${isLast ? 'border-2 border-blue-600' : 'border border-gray-200'
                    }`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold text-gray-800">{statusInfo.label}</h4>
                    <span className="text-xs text-gray-500">{formatDate(item.criado_em)}</span>
                  </div>

                  {item.status_anterior && (
                    <p className="text-sm text-gray-600 mb-1">
                      De: <span className="font-medium">{getStatusInfo(item.status_anterior).label}</span>
                    </p>
                  )}

                  {item.observacao && (
                    <p className="text-sm text-gray-700 mt-2 italic">
                      💬 {item.observacao}
                    </p>
                  )}

                  {isLast && (
                    <div className="mt-2 text-xs text-blue-600 font-medium">
                      ● Status Atual
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
