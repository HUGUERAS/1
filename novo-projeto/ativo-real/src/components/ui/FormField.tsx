import type { InputHTMLAttributes } from 'react'
import clsx from 'clsx'

interface FormFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string
  description?: string
}

export function FormField({ label, description, id, className, ...inputProps }: FormFieldProps) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-sm font-semibold text-slate-800" htmlFor={id}>
        {label}
      </label>
      <input
        id={id}
        className={clsx(
          'rounded-lg border border-slate-200 bg-white px-3 py-3 text-slate-900 outline-none transition focus:border-blue-400 focus:ring-2 focus:ring-blue-100',
          className,
        )}
        {...inputProps}
      />
      {description && <p className="text-xs text-slate-500">{description}</p>}
    </div>
  )
}
