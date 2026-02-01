import React, { useState } from 'react';

/**
 * ContractViewer.tsx
 * Visualizador e download de contrato em PDF
 */

interface ContractViewerProps {
  contratoUrl?: string;
  loteId: number;
  clienteNome?: string;
}

export const ContractViewer: React.FC<ContractViewerProps> = ({
  contratoUrl,
  loteId,
  clienteNome,
}) => {
  const [showPreview, setShowPreview] = useState(false);

  const handleDownload = () => {
    if (!contratoUrl) return;

    const link = document.createElement('a');
    link.href = contratoUrl;
    link.download = `contrato_lote_${loteId}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (!contratoUrl) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
        <div className="text-4xl mb-2">📄</div>
        <h3 className="font-semibold text-yellow-800 mb-2">Contrato em Preparação</h3>
        <p className="text-sm text-yellow-700">
          O contrato será disponibilizado em breve pelo topógrafo.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">📄 Contrato de Prestação de Serviços</h3>

      <div className="space-y-4">
        {/* Info Box */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            <strong>Cliente:</strong> {clienteNome || 'Não informado'}
          </p>
          <p className="text-sm text-blue-800">
            <strong>Lote:</strong> #{loteId}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <button
            onClick={() => setShowPreview(!showPreview)}
            className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium"
          >
            {showPreview ? '✕ Fechar Visualização' : '👁️ Visualizar Contrato'}
          </button>

          <button
            onClick={handleDownload}
            className="flex-1 px-4 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 font-medium"
          >
            ⬇️ Baixar PDF
          </button>
        </div>

        {/* PDF Preview */}
        {showPreview && (
          <div className="border rounded-lg overflow-hidden">
            <iframe
              src={contratoUrl}
              className="w-full h-[600px]"
              title="Visualização do Contrato"
            />
          </div>
        )}

        {/* Legal Notice */}
        <div className="bg-gray-50 rounded-lg p-4 text-xs text-gray-600">
          <p className="font-medium mb-1">⚖️ Informações Importantes:</p>
          <ul className="list-disc list-inside space-y-1">
            <li>Leia atentamente todos os termos antes de assinar</li>
            <li>Em caso de dúvidas, consulte o topógrafo responsável via chat</li>
            <li>O contrato é válido após assinatura digital ou física</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
