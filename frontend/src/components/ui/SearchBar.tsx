import * as React from 'react'
import { cn } from '../../lib/cn'

export interface SearchBarProps extends React.InputHTMLAttributes<HTMLInputElement> {
  onSearch?: (value: string) => void;
}

export const SearchBar = React.forwardRef<HTMLInputElement, SearchBarProps>(
  ({ className, onSearch, placeholder = 'Search...', ...props }, ref) => {
    const [val, setVal] = React.useState('');

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const v = e.target.value;
      setVal(v);
      if (onSearch) {
        onSearch(v);
      }
    };

    return (
      <div className="relative flex items-center w-full max-w-md">
        <div className="absolute left-3 text-slate-500 pointer-events-none flex items-center justify-center">
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input
          ref={ref}
          type="text"
          value={val}
          onChange={handleChange}
          placeholder={placeholder}
          className={cn(
            "w-full bg-slate-900/50 hover:bg-slate-900 border border-slate-800 rounded-lg py-2 pl-10 pr-4 text-sm text-white placeholder-slate-500 outline-none transition-all duration-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20",
            className
          )}
          {...props}
        />
      </div>
    )
  }
)
SearchBar.displayName = 'SearchBar'
