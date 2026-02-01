/**
 * OpenRouter AI Service - React Hook
 * 
 * Provides secure API calls to backend AI endpoints
 * API key is kept secure on the backend (never exposed to frontend)
 */

// @ts-nocheck
import React, { useState, useCallback } from 'react';

interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

interface ChatResponse {
  choices: Array<{
    message: ChatMessage;
    finish_reason: string;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

interface AnalysisResponse {
  analysis: string;
}

interface ReportResponse {
  report: string;
}

interface ValidationResponse {
  is_valid: boolean;
  confidence: number;
  issues: string[];
  recommendations: string[];
  geometric_type: string;
}

interface UseOpenRouterOptions {
  baseUrl?: string;
  authToken?: string;
}

/**
 * Hook para usar OpenRouter API via backend proxy
 */
export function useOpenRouter(options: UseOpenRouterOptions = {}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const baseUrl = options.baseUrl || process.env.REACT_APP_API_URL || 'http://localhost:7071/api';
  const authToken = options.authToken;

  const call = useCallback(
    async <T,>(
      endpoint: string,
      body: Record<string, any>,
      method: string = 'POST'
    ): Promise<T | null> => {
      setLoading(true);
      setError(null);

      try {
        const headers: HeadersInit = {
          'Content-Type': 'application/json',
        };

        if (authToken) {
          headers['Authorization'] = `Bearer ${authToken}`;
        }

        const response = await fetch(`${baseUrl}${endpoint}`, {
          method,
          headers,
          body: method !== 'GET' ? JSON.stringify(body) : undefined,
        });

        if (!response.ok) {
          const errorData = await response.json();
          const errorMessage = errorData.error || `HTTP ${response.status}`;
          setError(errorMessage);
          console.error(`API Error: ${endpoint}`, errorData);
          return null;
        }

        const data = await response.json();
        return data as T;
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Unknown error';
        setError(message);
        console.error('API call failed:', message);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [baseUrl, authToken]
  );

  /**
   * Send chat message to Jamba model
   */
  const chat = useCallback(
    async (messages: ChatMessage[], options?: { model?: string; temperature?: number; maxTokens?: number }) => {
      return call<ChatResponse>('/ai/chat', {
        messages,
        model: options?.model || 'ai21/jamba-large-1.7',
        temperature: options?.temperature || 0.7,
        max_tokens: options?.maxTokens || 4096,
      });
    },
    [call]
  );

  /**
   * Analyze topography data
   */
  const analyzeTopography = useCallback(
    async (prompt: string, context?: string) => {
      return call<AnalysisResponse>('/ai/analyze-topography', {
        prompt,
        context,
      });
    },
    [call]
  );

  /**
   * Generate a formatted report
   */
  const generateReport = useCallback(
    async (data: Record<string, any>) => {
      return call<ReportResponse>('/ai/generate-report', {
        data,
      });
    },
    [call]
  );

  /**
   * Validate geometry description
   */
  const validateGeometry = useCallback(
    async (description: string) => {
      return call<ValidationResponse>('/ai/validate-geometry', {
        description,
      });
    },
    [call]
  );

  return {
    loading,
    error,
    chat,
    analyzeTopography,
    generateReport,
    validateGeometry,
  };
}

/**
 * Context component para facilitar uso em toda a aplicação
 */


interface OpenRouterContextType {
  loading: boolean;
  error: string | null;
  chat: (messages: ChatMessage[], options?: any) => Promise<ChatResponse | null>;
  analyzeTopography: (prompt: string, context?: string) => Promise<AnalysisResponse | null>;
  generateReport: (data: Record<string, any>) => Promise<ReportResponse | null>;
  validateGeometry: (description: string) => Promise<ValidationResponse | null>;
}


const OpenRouterContext = React.createContext<OpenRouterContextType | undefined>(undefined);

export function OpenRouterProvider({ children, authToken }: { children: React.ReactNode; authToken?: string }) {
  const openRouter = useOpenRouter({ authToken });

  return <OpenRouterContext.Provider value={openRouter}>{children}</OpenRouterContext.Provider>;
}

export function useOpenRouterContext() {
  const context = React.useContext(OpenRouterContext);
  if (!context) {
    throw new Error('useOpenRouterContext must be used within OpenRouterProvider');
  }
  return context;
}

/**
 * Exemplo de uso em componente React:
 *
 * function MyComponent() {
 *   const { chat, loading, error } = useOpenRouter({ authToken: 'your-jwt-token' });
 *
 *   const handleChat = async () => {
 *     const response = await chat([
 *       { role: 'user', content: 'What is this property?' }
 *     ]);
 *     if (response) {
 *       console.log(response.choices[0].message.content);
 *     }
 *   };
 *
 *   return (
 *     <div>
 *       <button onClick={handleChat} disabled={loading}>
 *         {loading ? 'Analyzing...' : 'Analyze'}
 *       </button>
 *       {error && <p style={{ color: 'red' }}>{error}</p>}
 *     </div>
 *   );
 * }
 */
