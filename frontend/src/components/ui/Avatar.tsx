import * as React from 'react'
import { cn } from '../../lib/cn'

export interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  src?: string;
  name: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

export const Avatar = React.forwardRef<HTMLDivElement, AvatarProps>(
  ({ className, src, name, size = 'md', ...props }, ref) => {
    const initials = name
      .split(' ')
      .map((n) => n[0])
      .slice(0, 2)
      .join('')
      .toUpperCase();

    return (
      <div
        ref={ref}
        className={cn(
          "relative flex shrink-0 overflow-hidden rounded-full items-center justify-center bg-gradient-to-br from-primary-600 to-indigo-600 text-white font-semibold border border-white/10",
          {
            "h-8 w-8 text-xs": size === 'sm',
            "h-10 w-10 text-sm": size === 'md',
            "h-14 w-14 text-base": size === 'lg',
            "h-20 w-20 text-xl": size === 'xl',
          },
          className
        )}
        {...props}
      >
        {src ? (
          <img
            src={src}
            alt={name}
            className="aspect-square h-full w-full object-cover"
            onError={(e) => {
              // Hide image on error to fallback to initials
              (e.target as HTMLElement).style.display = 'none';
            }}
          />
        ) : null}
        <span className="flex h-full w-full items-center justify-center">
          {initials}
        </span>
      </div>
    )
  }
)
Avatar.displayName = 'Avatar'
