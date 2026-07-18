import * as React from 'react'
import { cn } from '../../lib/cn'

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  glass?: boolean;
  glowColor?: 'primary' | 'success' | 'warning' | 'danger' | 'none';
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, glass = true, glowColor = 'none', children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "rounded-xl overflow-hidden border transition-all duration-300",
          {
            "glass-panel shadow-2xl shadow-black/10": glass,
            "bg-slate-900 border-slate-800 shadow-md": !glass,
            "hover:border-primary-500/30 hover:shadow-primary-500/5": glowColor === 'primary',
            "hover:border-success-500/30 hover:shadow-success-500/5": glowColor === 'success',
            "hover:border-warning-500/30 hover:shadow-warning-500/5": glowColor === 'warning',
            "hover:border-danger-500/30 hover:shadow-danger-500/5": glowColor === 'danger',
          },
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)
Card.displayName = 'Card'

export const CardHeader = ({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("px-6 py-5 border-b border-slate-800/50 flex flex-col gap-1.5", className)} {...props}>
    {children}
  </div>
)

export const CardTitle = ({ className, children, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
  <h3 className={cn("text-lg font-semibold text-white tracking-tight", className)} {...props}>
    {children}
  </h3>
)

export const CardDescription = ({ className, children, ...props }: React.HTMLAttributes<HTMLParagraphElement>) => (
  <p className={cn("text-sm text-slate-400 font-normal leading-relaxed", className)} {...props}>
    {children}
  </p>
)

export const CardContent = ({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("px-6 py-5", className)} {...props}>
    {children}
  </div>
)

export const CardFooter = ({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("px-6 py-4 border-t border-slate-800/50 bg-slate-900/10 flex items-center justify-end gap-3", className)} {...props}>
    {children}
  </div>
)
