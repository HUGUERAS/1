import { createContext, useCallback, useContext, useState, type PropsWithChildren } from 'react'
import clsx from 'clsx'
import type { Toast, ToastType } from './Toast'

interface ToastContextValue {
  showToast: (type: ToastType, message: string) => void
  dismissToast: (id: string) => void
}

const ToastContext = createContext<ToastContextValue | null>(null)

export function ToastProvider({ children }: PropsWithChildren) {
  const [toasts, setToasts] = useState<Toast[]>([])

  const dismissToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  const showToast = useCallback((type: ToastType, message: string) => {
    const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`
    setToasts(prev => [...prev, { id, type, message }])
    setTimeout(() => dismissToast(id), 3500)
  }, [dismissToast])

  return (
    <ToastContext.Provider value={{ showToast, dismissToast }}>
      {children}
      <div className="pointer-events-none fixed right-4 top-4 z-50 flex flex-col gap-3">
        {toasts.map(toast => (
          <div
            key={toast.id}
            className={clsx(
              'pointer-events-auto flex items-start justify-between gap-3 rounded-lg px-4 py-3 shadow-lg ring-1 ring-black/5 border',
              toast.type === 'success'
                ? 'bg-emerald-50 text-emerald-800 border-emerald-100'
                : 'bg-red-50 text-red-800 border-red-100'
            )}
          >
            <div className="text-sm font-medium">{toast.message}</div>
            <button
              onClick={() => dismissToast(toast.id)}
              className="ml-2 text-xs font-semibold text-slate-500 hover:text-slate-700"
            >
              Fechar
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) {
    throw new Error('useToast must be used within ToastProvider')
  }
  return ctx
}
