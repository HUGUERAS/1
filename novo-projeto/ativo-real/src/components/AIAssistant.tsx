/**
 * AI Assistant Component - Example Usage
 * 
 * Demonstrates how to use OpenRouter integration to:
 * - Chat with AI assistant
 * - Analyze topography
 * - Generate reports
 * - Validate geometries
 */

import React, { useState } from 'react';
import { useOpenRouter } from '../services/useOpenRouter';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export function AIAssistant() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  
  // Get JWT token from wherever you store it (localStorage, context, etc)
  const authToken = localStorage.getItem('access_token') || '';
  
  const { chat, analyzeTopography, loading, error } = useOpenRouter({ authToken });

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    const newMessages = [...messages, { role: 'user' as const, content: input }];
    setMessages(newMessages);
    setInput('');

    // Call AI
    const response = await chat(newMessages);
    
    if (response && response.choices && response.choices.length > 0) {
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: response.choices[0].message.content,
        },
      ]);
    }
  };

  const handleAnalyzeProperty = async () => {
    const prompt = 'Analyze the agricultural potential of a 100 hectare property in Sao Paulo state with Latossolo soil type';
    
    const response = await analyzeTopography(prompt);
    
    if (response) {
      setMessages([
        ...messages,
        { role: 'user', content: prompt },
        { role: 'assistant', content: response.analysis },
      ]);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      <div className="bg-white rounded-lg shadow-lg flex flex-col flex-1">
        {/* Header */}
        <div className="bg-green-600 text-white p-4 rounded-t-lg">
          <h1 className="text-xl font-bold">🤖 AI Topography Assistant</h1>
          <p className="text-sm opacity-90">Powered by Jamba 1.5 Large (256K context)</p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-8">
              <p className="mb-4">👋 Welcome! I can help you with:</p>
              <ul className="text-left max-w-md mx-auto space-y-2">
                <li>📍 Topography analysis</li>
                <li>📊 Property reports</li>
                <li>✓ Geometry validation</li>
                <li>💬 General questions about land management</li>
              </ul>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[70%] rounded-lg p-3 ${
                  msg.role === 'user'
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-lg p-3">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              <strong>Error:</strong> {error}
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="border-t p-3 bg-gray-50">
          <div className="flex gap-2 mb-2 overflow-x-auto">
            <button
              onClick={handleAnalyzeProperty}
              disabled={loading}
              className="px-3 py-1 text-sm bg-blue-100 hover:bg-blue-200 rounded whitespace-nowrap disabled:opacity-50"
            >
              📍 Analyze Property
            </button>
            <button
              onClick={() => setInput('What are the best crops for Latossolo soil?')}
              className="px-3 py-1 text-sm bg-blue-100 hover:bg-blue-200 rounded whitespace-nowrap"
            >
              🌾 Crop Suggestions
            </button>
            <button
              onClick={() => setInput('How to validate land boundaries in Brazil?')}
              className="px-3 py-1 text-sm bg-blue-100 hover:bg-blue-200 rounded whitespace-nowrap"
            >
              ✓ Validation Help
            </button>
          </div>
        </div>

        {/* Input */}
        <div className="border-t p-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !loading && handleSendMessage()}
              placeholder="Ask me anything about topography..."
              className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              disabled={loading}
            />
            <button
              onClick={handleSendMessage}
              disabled={loading || !input.trim()}
              className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? '...' : 'Send'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AIAssistant;
