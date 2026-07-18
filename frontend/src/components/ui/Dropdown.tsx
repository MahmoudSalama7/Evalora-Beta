import * as React from 'react'
import { cn } from '../../lib/cn'

interface DropdownContextProps {
  isOpen: boolean;
  setIsOpen: (val: boolean) => void;
}

const DropdownContext = React.createContext<DropdownContextProps | undefined>(undefined);

export interface DropdownProps {
  children: React.ReactNode;
  className?: string;
}

export const Dropdown: React.FC<DropdownProps> = ({ children, className }) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const containerRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleOutsideClick);
    return () => document.removeEventListener('mousedown', handleOutsideClick);
  }, []);

  return (
    <DropdownContext.Provider value={{ isOpen, setIsOpen }}>
      <div ref={containerRef} className={cn("relative inline-block text-left", className)}>
        {children}
      </div>
    </DropdownContext.Provider>
  );
};

export interface DropdownTriggerProps {
  children: React.ReactNode;
}

export const DropdownTrigger: React.FC<DropdownTriggerProps> = ({ children }) => {
  const ctx = React.useContext(DropdownContext);
  if (!ctx) throw new Error("DropdownTrigger must be used inside a Dropdown");

  return (
    <div onClick={() => ctx.setIsOpen(!ctx.isOpen)} className="cursor-pointer">
      {children}
    </div>
  );
};

export interface DropdownMenuProps {
  children: React.ReactNode;
  align?: 'left' | 'right';
  className?: string;
}

export const DropdownMenu: React.FC<DropdownMenuProps> = ({ children, align = 'right', className }) => {
  const ctx = React.useContext(DropdownContext);
  if (!ctx) throw new Error("DropdownMenu must be used inside a Dropdown");

  if (!ctx.isOpen) return null;

  return (
    <div
      className={cn(
        "absolute mt-2 w-48 rounded-lg bg-slate-900 border border-slate-800 shadow-xl z-50 py-1.5 focus:outline-none",
        {
          "right-0 origin-top-right": align === 'right',
          "left-0 origin-top-left": align === 'left',
        },
        className
      )}
    >
      {children}
    </div>
  );
};

export interface DropdownItemProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export const DropdownItem: React.FC<DropdownItemProps> = ({ children, className, onClick, ...props }) => {
  const ctx = React.useContext(DropdownContext);
  if (!ctx) throw new Error("DropdownItem must be used inside a Dropdown");

  const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    ctx.setIsOpen(false);
    if (onClick) {
      onClick(e);
    }
  };

  return (
    <div
      onClick={handleClick}
      className={cn(
        "flex items-center px-4 py-2.5 text-sm text-slate-300 hover:bg-white/5 hover:text-white cursor-pointer transition-colors duration-150",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
