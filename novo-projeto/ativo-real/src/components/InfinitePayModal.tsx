import { useState, useEffect } from 'react';
import './InfinitePayModal.css';

interface InfinitePayModalProps {
  isOpen: boolean;
  onClose: () => void;
  projectId: number;
  projectTitle: string;
  amount: number;
  onSuccess: (paymentId: string) => void;
}

export default function InfinitePayModal({
  isOpen,
  onClose,
  projectId,
  projectTitle,
  amount,
  onSuccess
}: InfinitePayModalProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [paymentData, setPaymentData] = useState<any>(null);
  const [selectedMethod, setSelectedMethod] = useState<'pix' | 'card' | 'boleto'>('pix');
  const [checkingStatus, setCheckingStatus] = useState(false);

  // Criar pagamento ao abrir modal
  useEffect(() => {
    if (isOpen && !paymentData) {
      createPayment();
    }
  }, [isOpen]);

  // Verificar status PIX automaticamente (polling)
  useEffect(() => {
    if (paymentData && selectedMethod === 'pix' && !checkingStatus) {
      const interval = setInterval(async () => {
        await checkPaymentStatus();
      }, 3000); // Verifica a cada 3 segundos

      return () => clearInterval(interval);
    }
  }, [paymentData, selectedMethod]);

  const createPayment = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE || '/api'}/infinitepay/create-payment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          amount: amount,
          projectId: projectId,
          description: `Pagamento - ${projectTitle}`
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Erro ao criar pagamento');
      }

      const data = await response.json();
      setPaymentData(data);
      setLoading(false);
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  const checkPaymentStatus = async () => {
    if (!paymentData?.paymentId || checkingStatus) return;

    setCheckingStatus(true);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE || '/api'}/infinitepay/check-status/${paymentData.paymentId}`
      );

      if (response.ok) {
        const status = await response.json();
        if (status.status === 'succeeded' || status.status === 'paid') {
          onSuccess(paymentData.paymentId);
          onClose();
        }
      }
    } catch (err) {
      console.error('Erro ao verificar status:', err);
    } finally {
      setCheckingStatus(false);
    }
  };

  const copyPixCode = () => {
    if (paymentData?.pixCopyPaste) {
      navigator.clipboard.writeText(paymentData.pixCopyPaste);
      alert('Código PIX copiado!');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="infinitepay-overlay" onClick={onClose}>
      <div className="infinitepay-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="infinitepay-header">
          <h2>💳 Pagamento Online</h2>
          <button className="infinitepay-close" onClick={onClose}>×</button>
        </div>

        {/* Conteúdo */}
        <div className="infinitepay-content">
          {loading ? (
            <div className="infinitepay-loading">
              <div className="spinner"></div>
              <p>Gerando pagamento...</p>
            </div>
          ) : error ? (
            <div className="infinitepay-error">
              <p>❌ {error}</p>
              <button onClick={createPayment}>Tentar novamente</button>
            </div>
          ) : paymentData ? (
            <>
              {/* Informações do Pagamento */}
              <div className="payment-info">
                <h3>{projectTitle}</h3>
                <div className="amount">
                  R$ {amount.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </div>
              </div>

              {/* Seletor de Método */}
              <div className="payment-methods">
                <button
                  className={`method-btn ${selectedMethod === 'pix' ? 'active' : ''}`}
                  onClick={() => setSelectedMethod('pix')}
                >
                  <span className="method-icon">🟢</span>
                  <span>PIX</span>
                  <span className="method-badge">Instantâneo</span>
                </button>
                <button
                  className={`method-btn ${selectedMethod === 'card' ? 'active' : ''}`}
                  onClick={() => setSelectedMethod('card')}
                >
                  <span className="method-icon">💳</span>
                  <span>Cartão</span>
                </button>
                <button
                  className={`method-btn ${selectedMethod === 'boleto' ? 'active' : ''}`}
                  onClick={() => setSelectedMethod('boleto')}
                >
                  <span className="method-icon">📄</span>
                  <span>Boleto</span>
                </button>
              </div>

              {/* Conteúdo por Método */}
              {selectedMethod === 'pix' && (
                <div className="pix-content">
                  <p className="pix-instructions">
                    Escaneie o QR Code com o app do seu banco ou copie o código PIX:
                  </p>
                  {paymentData.pixQrCode && (
                    <div className="qr-code-container">
                      <img src={paymentData.pixQrCode} alt="QR Code PIX" />
                    </div>
                  )}
                  <button className="copy-btn" onClick={copyPixCode}>
                    📋 Copiar Código PIX
                  </button>
                  <div className="pix-status">
                    {checkingStatus ? (
                      <p>🔄 Aguardando pagamento...</p>
                    ) : (
                      <p>⏳ Verificando automaticamente</p>
                    )}
                  </div>
                </div>
              )}

              {selectedMethod === 'card' && (
                <div className="card-content">
                  <p>Você será redirecionado para a página de pagamento seguro:</p>
                  <a
                    href={paymentData.checkoutUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="checkout-btn"
                  >
                    🔒 Ir para Pagamento com Cartão
                  </a>
                  <p className="security-note">
                    🛡️ Pagamento 100% seguro via InfinitePay
                  </p>
                </div>
              )}

              {selectedMethod === 'boleto' && (
                <div className="boleto-content">
                  <p>Você será redirecionado para gerar o boleto bancário:</p>
                  <a
                    href={paymentData.checkoutUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="checkout-btn"
                  >
                    📄 Gerar Boleto
                  </a>
                  <p className="boleto-note">
                    Vencimento: 3 dias úteis
                  </p>
                </div>
              )}

              {/* Rodapé */}
              <div className="payment-footer">
                <p>
                  <small>Taxa: 0.99% • Processado por InfinitePay</small>
                </p>
              </div>
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
}
