import * as React from 'react'
import { cn } from '../../lib/cn'
import { useNotificationStore } from '../../stores/notification-store'
import type { ToastMessage } from '../../stores/notification-store'

export const ToastContainer: React.FC = () => {
  const toasts = useNotificationStore((state) => state.toasts);

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2.5 max-w-sm w-full pointer-events-none">
      {toasts.map((toast) => (
        <ToastItem key={toast.id} toast={toast} />
      ))}
    </div>
  );
};

interface ToastItemProps {
  toast: ToastMessage;
}

const ToastItem: React.FC<ToastItemProps> = ({ toast }) => {
  const removeToast = useNotificationStore((state) => state.removeToast);

  return (
    <div
      className={cn(
        "flex items-start gap-3 p-4 rounded-xl border shadow-xl pointer-events-auto transition-all duration-300 transform translate-y-0 scale-100",
        {
          "bg-slate-900 border-slate-800 text-slate-200": toast.type === 'info',
          "bg-emerald-950/80 border-emerald-500/30 text-emerald-350 backdrop-blur-md": toast.type === 'success',
          "bg-amber-950/80 border-amber-500/30 text-amber-350 backdrop-blur-md": toast.type === 'warning',
          "bg-red-950/80 border-red-500/30 text-red-350 backdrop-blur-md": toast.type === 'error',
        }
      )}
    >
      <div className="flex-1 text-sm font-medium">{toast.message}</div>
      <button
        onClick={() => removeToast(toast.id)}
        className="text-slate-400 hover:text-white transition-colors duration-150"
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  );
};
