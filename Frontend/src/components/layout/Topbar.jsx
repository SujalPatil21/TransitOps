import React from 'react';
import { useLocation } from 'react-router-dom';
import { Menu, ChevronRight } from 'lucide-react';

/**
 * Topbar represents the top bar shell.
 * Exposes a mobile menu trigger and visual breadcrumb info.
 */
const Topbar = ({ user, role, setSidebarOpen }) => {
  const location = useLocation();

  // Simple title mapper based on the route
  const getPageTitle = () => {
    const path = location.pathname;
    if (path.includes('/dashboard')) return 'Dashboard Overview';
    if (path === '/vehicles') return 'Vehicle Registry';
    if (path === '/drivers') return 'Driver Management';
    if (path === '/trips') return 'Trip Management';
    if (path === '/maintenance') return 'Maintenance Logs';
    if (path === '/fuel-expense') return 'Fuel & Expenses';
    if (path === '/analytics') return 'Reports & Analytics';
    if (path === '/settings') return 'Settings';
    return 'TransitOps';
  };

  // Convert role identifier constants into readable text
  const getRoleLabel = (roleStr) => {
    if (!roleStr) return '';
    return roleStr
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <header className="h-20 bg-card-white border-b border-border-light flex items-center justify-between px-[var(--spacing-page-px)] shrink-0">
      {/* Mobile Toggle & Breadcrumbs */}
      <div className="flex items-center gap-3">
        <button 
          onClick={() => setSidebarOpen(true)}
          className="p-1.5 rounded-md text-text-secondary hover:text-text-primary hover:bg-bg-cream md:hidden focus:ring-2 focus:ring-primary focus:outline-none"
          aria-label="Open sidebar"
        >
          <Menu className="w-5 h-5" />
        </button>
        
        <div className="flex items-center gap-2 text-xs font-semibold text-text-secondary select-none">
          <span>Platform</span>
          <ChevronRight className="w-3 h-3 text-text-secondary/60" />
          <span className="text-text-primary font-bold">{getPageTitle()}</span>
        </div>
      </div>

      {/* User Information Display */}
      <div className="flex items-center gap-3">
        <div className="text-right hidden sm:block">
          <span className="block text-xs font-bold text-text-primary">{user?.name || 'Raven K.'}</span>
          <span className="block text-[10px] text-text-secondary font-semibold">{getRoleLabel(role)}</span>
        </div>
        
        <div 
          className="w-10 h-10 rounded-full bg-accent/60 flex items-center justify-center font-bold text-text-primary border border-border-light select-none cursor-pointer"
          title={`${user?.name || 'User'} - ${getRoleLabel(role)}`}
        >
          RK
        </div>
      </div>
    </header>
  );
};

export default Topbar;
