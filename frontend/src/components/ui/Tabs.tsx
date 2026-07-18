import * as React from 'react'
import { cn } from '../../lib/cn'

interface TabsContextProps {
  value: string;
  onValueChange: (val: string) => void;
}

const TabsContext = React.createContext<TabsContextProps | undefined>(undefined);

export interface TabsProps extends React.HTMLAttributes<HTMLDivElement> {
  defaultValue: string;
  value?: string;
  onValueChange?: (value: string) => void;
}

export const Tabs: React.FC<TabsProps> = ({ defaultValue, value, onValueChange, className, children, ...props }) => {
  const [localVal, setLocalVal] = React.useState(defaultValue);
  
  const activeVal = value !== undefined ? value : localVal;
  const handleValChange = React.useCallback((val: string) => {
    if (value === undefined) setLocalVal(val);
    if (onValueChange) onValueChange(val);
  }, [value, onValueChange]);

  return (
    <TabsContext.Provider value={{ value: activeVal, onValueChange: handleValChange }}>
      <div className={cn("w-full", className)} {...props}>
        {children}
      </div>
    </TabsContext.Provider>
  );
};

export const TabsList = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("inline-flex h-11 items-center justify-center rounded-lg bg-slate-900/60 p-1 border border-slate-800 text-slate-400", className)}
      {...props}
    />
  )
)
TabsList.displayName = 'TabsList'

export interface TabsTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  value: string;
}

export const TabsTrigger = React.forwardRef<HTMLButtonElement, TabsTriggerProps>(
  ({ className, value, children, ...props }, ref) => {
    const ctx = React.useContext(TabsContext);
    if (!ctx) throw new Error("TabsTrigger must be used inside a Tabs component");

    const isActive = ctx.value === value;

    return (
      <button
        ref={ref}
        type="button"
        onClick={() => ctx.onValueChange(value)}
        className={cn(
          "inline-flex items-center justify-center whitespace-nowrap rounded-md px-4 py-1.5 text-sm font-medium transition-all duration-200 focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50",
          {
            "bg-gradient-to-r from-primary-600 to-indigo-600 text-white shadow-md font-semibold": isActive,
            "hover:text-slate-200": !isActive,
          },
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
)
TabsTrigger.displayName = 'TabsTrigger'

export interface TabsContentProps extends React.HTMLAttributes<HTMLDivElement> {
  value: string;
}

export const TabsContent = React.forwardRef<HTMLDivElement, TabsContentProps>(
  ({ className, value, children, ...props }, ref) => {
    const ctx = React.useContext(TabsContext);
    if (!ctx) throw new Error("TabsContent must be used inside a Tabs component");

    const isActive = ctx.value === value;

    if (!isActive) return null;

    return (
      <div
        ref={ref}
        className={cn("mt-4 focus-visible:outline-none transition-all duration-300", className)}
        {...props}
      >
        {children}
      </div>
    );
  }
)
TabsContent.displayName = 'TabsContent'
