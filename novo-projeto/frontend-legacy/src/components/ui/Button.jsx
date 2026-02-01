import clsx from 'clsx'

const variantClasses = {
  primary:
    'bg-blue-900 hover:bg-blue-800 text-white border border-blue-900/90',
  success:
    'bg-emerald-700 hover:bg-emerald-600 text-white border border-emerald-700/90',
  info: 'bg-sky-700 hover:bg-sky-600 text-white border border-sky-700/90',
  ghost:
    'bg-white/90 text-blue-900 border border-blue-100 hover:bg-blue-50',
}

export function Button({
  children,
  variant = 'primary',
  className,
  loading = false,
  disabled,
  ...props
}) {
  return (
    <button
      className={clsx(
        'inline-flex items-center justify-center gap-2 rounded-lg px-4 py-3 font-semibold shadow-md transition disabled:cursor-not-allowed disabled:opacity-60',
        variantClasses[variant],
        className,
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" aria-hidden="true" />
      )}
      {children}
    </button>
  )
}
