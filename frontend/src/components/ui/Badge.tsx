import * as React from 'react'
import { cn } from '../../lib/cn'

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'primary' | 'success' | 'warning' | 'danger' | 'info' | 'gray';
  size?: 'sm' | 'md';
}

export const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant = 'primary', size = 'sm', children, ...props }, ref) => {
    return (
      <span
        ref={ref}
        className={cn(
          "inline-flex items-center font-medium rounded-full tracking-wide transition-colors duration-150",
          {
            "bg-primary-500/10 text-primary-400 border border-primary-500/20": variant === 'primary',
            "bg-success-500/10 text-success-400 border border-success-500/20": variant === 'success',
            "bg-warning-500/10 text-warning-400 border border-warning-500/20": variant === 'warning',
            "bg-danger-500/10 text-danger-400 border border-danger-500/20": variant === 'danger',
            "bg-blue-500/10 text-blue-400 border border-blue-500/20": variant === 'info',
            "bg-slate-500/10 text-slate-400 border border-slate-500/20": variant === 'gray',
            
            "px-2.5 py-0.5 text-xs": size === 'sm',
            "px-3.5 py-1 text-xs font-semibold": size === 'md',
          },
          className
        )}
        {...props}
      >
        {children}
      </span>
    )
  }
)
Badge.displayName = 'Badge'
