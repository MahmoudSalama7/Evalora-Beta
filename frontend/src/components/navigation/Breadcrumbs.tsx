import * as React from 'react'
import { Link, useLocation } from 'react-router-dom'

export const Breadcrumbs: React.FC = () => {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);

  if (pathnames.length <= 1) return null;

  return (
    <nav className="flex text-xs font-medium text-slate-500 tracking-wide uppercase select-none items-center gap-1.5 py-1">
      <Link to="/" className="hover:text-white transition-colors duration-150">
        Evalora
      </Link>
      {pathnames.map((name, index) => {
        const routeTo = `/${pathnames.slice(0, index + 1).join('/')}`;
        const isLast = index === pathnames.length - 1;
        const formattedName = name.charAt(0).toUpperCase() + name.slice(1).replace('-', ' ');

        return (
          <React.Fragment key={name}>
            <svg className="w-3 h-3 text-slate-700 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5l7 7-7 7" />
            </svg>
            {isLast ? (
              <span className="text-slate-350 font-semibold">{formattedName}</span>
            ) : (
              <Link to={routeTo} className="hover:text-white transition-colors duration-150">
                {formattedName}
              </Link>
            )}
          </React.Fragment>
        );
      })}
    </nav>
  );
};
export default Breadcrumbs;
