import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { 
  X, LogOut, HelpCircle, LayoutDashboard, Truck, Users, 
  Navigation, Wrench, Fuel, BarChart3, Settings 
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

// Local icon mapping dictionary to bypass full library imports during build
const iconMap = { 
  X, LogOut, HelpCircle, LayoutDashboard, Truck, Users, 
  Navigation, Wrench, Fuel, BarChart3, Settings 
};

/**
 * Sidebar is a pure presentation component.
 * It receives filtered navigation items as props and renders them.
 * Contains no authorization/permissions logic.
 */
const Sidebar = ({ navigationItems = [], activeRole, sidebarOpen, setSidebarOpen }) => {
  const location = useLocation();
  const { user, logout } = useAuth();

  // Helper to dynamically render Lucide icons by name from our mapped list
  const renderIcon = (iconName, className) => {
    const IconComponent = iconMap[iconName] || HelpCircle;
    return <IconComponent className={className} />;
  };

  // Helper to format role names into user-friendly display text
  const formatRole = (roleStr) => {
    if (!roleStr) return '';
    return roleStr.replace(/_/g, ' ');
  };

  // Helper to get uppercase user initials
  const getInitials = (name) => {
    if (!name) return 'U';
    return name
      .split(' ')
      .filter(Boolean)
      .map((word) => word.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const displayName = user?.username || 'User';

  return (
    <aside 
      className={`fixed top-0 bottom-0 left-0 z-50 flex flex-col w-64 bg-card-white border-r border-border-light transition-transform duration-200 ease-in-out md:translate-x-0 md:static md:h-screen
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}
    >
      {/* Branding Logo Area */}
      <div className="flex items-center justify-between h-20 px-6 border-b border-border-light">
        <div className="flex items-center gap-3">
          {/* Flat Geometric Illustration of a truck/logo */}
          <div className="w-8 h-8 rounded bg-primary flex items-center justify-center text-card-white font-bold text-lg select-none">
            T
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-text-primary">TransitOps</h1>
            <p className="text-[10px] text-text-secondary -mt-1 font-medium">Smart Fleet Platform</p>
          </div>
        </div>
        {/* Mobile close button */}
        <button 
          onClick={() => setSidebarOpen(false)}
          className="p-1 rounded-md text-text-secondary hover:text-text-primary hover:bg-bg-cream md:hidden"
        >
          {renderIcon('X', 'w-5 h-5')}
        </button>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
        {navigationItems.map((item) => {
          // Resolve parameterized paths (e.g. /:role/dashboard) using lowercase-dashed slugs
          const roleSlug = activeRole ? activeRole.toLowerCase().replace(/\s+/g, '-') : '';
          const resolvedPath = item.path.includes('/:role')
            ? item.path.replace('/:role', `/${roleSlug}`)
            : item.path;

          // Check if link is active
          const isActive = location.pathname === resolvedPath;

          return (
            <NavLink
              key={item.label}
              to={resolvedPath}
              onClick={() => setSidebarOpen(false)}
              className={`flex items-center gap-3.5 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-150
                ${isActive 
                  ? 'bg-bg-cream text-primary border-l-4 border-primary font-semibold' 
                  : 'text-text-secondary hover:bg-bg-cream/50 hover:text-text-primary'
                }`}
            >
              {renderIcon(item.icon, `w-5 h-5 ${isActive ? 'text-primary' : 'text-text-secondary'}`)}
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Footer Profile summary & Logout action */}
      <div className="p-4 border-t border-border-light bg-bg-cream/20">
        <div className="flex items-center gap-3 px-2 py-1.5 mb-3 select-none">
          <div className="w-9 h-9 rounded-full bg-accent/60 flex items-center justify-center font-bold text-text-primary">
            {getInitials(displayName)}
          </div>
          <div className="min-w-0 flex-1">
            <p className="text-sm font-semibold text-text-primary truncate">{displayName}</p>
            <p className="text-[11px] text-text-secondary truncate">{formatRole(activeRole)}</p>
          </div>
        </div>
        <button 
          onClick={logout}
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg border border-border-light bg-card-white text-xs font-semibold text-text-secondary hover:text-primary hover:border-primary/20 hover:bg-primary/5 transition-all duration-150"
        >
          {renderIcon('LogOut', 'w-4 h-4')}
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
