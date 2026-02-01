import React, { useState, useEffect } from 'react';

/**
 * ChatWidget.tsx
 * Widget de chat simples com polling para comunicação topógrafo-cliente
 */

interface Message {
  id: number;
  sender_id: number;
  sender_role: string;
  message: string;
  is_read: boolean;
  criado_em: string;
}

interface ChatWidgetProps {
  projetoId: number;
  currentUserId: number;
  currentUserRole: 'TOPOGRAFO' | 'CLIENTE';
}

export const ChatWidget: React.FC<ChatWidgetProps> = ({
  projetoId,
  currentUserId,
  currentUserRole,
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  // Polling a cada 5 segundos
  useEffect(() => {
    if (!isOpen) return;

    const fetchMessages = async () => {
      try {
        const response = await fetch(`/api/chat/messages?projeto_id=${projetoId}&limit=50`);
        if (response.ok) {
          const data = await response.json();
          setMessages(data);
        }
      } catch (error) {
        console.error('Erro ao buscar mensagens:', error);
      }
    };

    fetchMessages();
    const interval = setInterval(fetchMessages, 5000);

    return () => clearInterval(interval);
  }, [projetoId, isOpen]);

  const sendMessage = async () => {
    if (!newMessage.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('/api/chat/messages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projeto_id: projetoId,
          sender_id: currentUserId,
          sender_role: currentUserRole,
          message: newMessage,
        }),
      });

      if (response.ok) {
        const newMsg = await response.json();
        setMessages([...messages, newMsg]);
        setNewMessage('');
      }
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Toggle Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-blue-600 text-white rounded-full p-4 shadow-lg hover:bg-blue-700"
        >
          💬 Chat
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="bg-white rounded-lg shadow-xl w-96 h-[500px] flex flex-col">
          {/* Header */}
          <div className="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
            <h3 className="font-semibold">💬 Chat do Projeto</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-gray-200"
            >
              ✕
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.length === 0 ? (
              <p className="text-gray-400 text-center text-sm">
                Nenhuma mensagem ainda. Inicie a conversa!
              </p>
            ) : (
              messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.sender_id === currentUserId ? 'justify-end' : 'justify-start'
                    }`}
                >
                  <div
                    className={`max-w-[70%] rounded-lg p-3 ${msg.sender_id === currentUserId
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                      }`}
                  >
                    <p className="text-xs font-semibold mb-1">
                      {msg.sender_role === 'TOPOGRAFO' ? '👷 Topógrafo' : '👤 Cliente'}
                    </p>
                    <p className="text-sm">{msg.message}</p>
                    <p className="text-xs opacity-70 mt-1">{formatDate(msg.criado_em)}</p>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Input */}
          <div className="border-t p-3 flex gap-2">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Digite sua mensagem..."
              className="flex-1 px-3 py-2 border rounded-md"
              disabled={loading}
            />
            <button
              onClick={sendMessage}
              disabled={loading || !newMessage.trim()}
              className={`px-4 py-2 rounded-md text-white ${loading || !newMessage.trim()
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
                }`}
            >
              Enviar
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
