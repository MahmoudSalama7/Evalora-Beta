import * as React from 'react'
import { useAuthStore } from '../../stores/auth-store'
import { useThemeStore } from '../../stores/theme-store'
import { Dropdown, DropdownTrigger, DropdownMenu, DropdownItem } from '../ui/Dropdown'
import { Breadcrumbs } from './Breadcrumbs'

export const TopNav: React.FC = () => {
  const { user, logout } = useAuthStore();
  const { theme, toggleTheme } = useThemeStore();
  
  const [notifications, setNotifications] = React.useState([
    { id: '1', text: 'Sarah Connor scheduled technical interview', time: '10m ago', unread: true },
    { id: '2', text: 'AI screening finished for Miles Dyson (89% match)', time: '2h ago', unread: true },
    { id: '3', text: 'New applicant for DevOps / Infrastructure position', time: '1d ago', unread: false }
  ]);

  const hasUnread = notifications.some(n => n.unread);

  const markAllRead = () => {
    setNotifications(notifications.map(n => ({ ...n, unread: false })));
  };

  return (
    <header className="h-16 border-b border-slate-800 bg-[#0b0f19]/70 backdrop-blur-md px-6 flex items-center justify-between z-40">
      {/* Left side Breadcrumbs */}
      <Breadcrumbs />

      {/* Right side Actions */}
      <div className="flex items-center gap-4">
        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-white/5 transition-colors"
          title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        >
          {theme === 'dark' ? (
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-11.314l.707.707m11.314 11.314l.707-.707M12 5a7 7 0 100 14 7 7 0 000-14z" />
            </svg>
          ) : (
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          )}
        </button>

        {/* Notifications Dropdown */}
        <Dropdown>
          <DropdownTrigger>
            <button className="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-white/5 transition-colors relative">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              {hasUnread && (
                <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-primary-500 ring-2 ring-[#0b0f19]" />
              )}
            </button>
          </DropdownTrigger>
          <DropdownMenu className="w-80">
            <div className="px-4 py-2 border-b border-slate-800/80 flex items-center justify-between">
              <span className="text-xs font-bold text-white uppercase tracking-wider">Notifications</span>
              {hasUnread && (
                <button onClick={markAllRead} className="text-xxs text-primary-400 hover:underline font-semibold">
                  Mark all read
                </button>
              )}
            </div>
            <div className="max-h-64 overflow-y-auto">
              {notifications.map((notif) => (
                <div
                  key={notif.id}
                  className={`px-4 py-3 border-b border-slate-800/40 text-xs transition-colors hover:bg-white/5 ${
                    notif.unread ? 'bg-primary-500/5' : ''
                  }`}
                >
                  <p className={`text-slate-200 ${notif.unread ? 'font-semibold' : ''}`}>{notif.text}</p>
                  <p className="text-xxs text-slate-500 mt-1">{notif.time}</p>
                </div>
              ))}
            </div>
          </DropdownMenu>
        </Dropdown>

        {/* Vertical Divider */}
        <span className="w-px h-6 bg-slate-800" />

        {/* User Account Menu */}
        <Dropdown>
          <DropdownTrigger>
            <div className="flex items-center gap-2 cursor-pointer group">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-600 to-indigo-600 text-white font-semibold flex items-center justify-center text-xs">
                {user?.name?.[0] || 'U'}
              </div>
              <span className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors max-w-[100px] truncate hidden sm:inline">
                {user?.name || 'Account'}
              </span>
            </div>
          </DropdownTrigger>
          <DropdownMenu className="w-48">
            <div className="px-4 py-2 border-b border-slate-800/80">
              <p className="text-xs font-semibold text-white truncate">{user?.name}</p>
              <p className="text-xxs text-slate-500 truncate mt-0.5">{user?.email}</p>
            </div>
            <DropdownItem onClick={() => logout()}>
              <svg className="w-4 h-4 mr-2.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Sign out
            </DropdownItem>
          </DropdownMenu>
        </Dropdown>
      </div>
    </header>
  );
};
export default TopNav;
