import * as React from 'react'
import { cn } from '../../lib/cn'

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  leftIcon?: React.ReactNode;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = 'text', label, error, leftIcon, ...props }, ref) => {
    return (
      <div className="w-full flex flex-col gap-1.5 text-left">
        {label && (
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            {label}
          </label>
        )}
        <div className="relative flex items-center">
          {leftIcon && (
            <div className="absolute left-3 text-slate-500 pointer-events-none flex items-center justify-center">
              {leftIcon}
            </div>
          )}
          <input
            type={type}
            ref={ref}
            className={cn(
              "w-full bg-slate-900/50 hover:bg-slate-900 border rounded-lg py-2.5 px-4 text-sm text-white placeholder-slate-500 outline-none transition-all duration-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20",
              leftIcon ? "pl-10" : "pl-4",
              error ? "border-red-500/50 focus:border-red-500 focus:ring-red-500/10" : "border-slate-800",
              className
            )}
            {...props}
          />
        </div>
        {error && (
          <span className="text-xs text-red-400 font-medium mt-0.5">
            {error}
          </span>
        )}
      </div>
    )
  }
)
Input.displayName = 'Input'
