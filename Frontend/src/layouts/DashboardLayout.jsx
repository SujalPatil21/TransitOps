import React, { useState } from 'react';
import { Outlet, Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import Sidebar from '../components/layout/Sidebar';
import Topbar from '../components/layout/Topbar';
import { navigationConfig } from '../config/navigation';
import { filterNavigationItems, hasRouteAccess } from '../config/accessControl';

/**
 * DashboardLayout wraps all authenticated routes.
 * Handles route-level authorization and dynamically passes filtered 
 * navigation nodes to the visual-only Sidebar.
 */
const DashboardLayout = () => {
  const { user, role, isAuthenticated, loading } = useAuth();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // loading state fallback
  if (loading) {
    return (
      <div className="min-h-screen bg-bg-cream flex items-center justify-center">
        <div className="text-primary text-xl font-bold animate-pulse">Loading TransitOps...</div>
      </div>
    );
  }

  // Redirect to Login if the user session is unauthenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  // Check path-level access permissions
  const isAuthorized = hasRouteAccess(role, location.pathname);
  if (!isAuthorized) {
    // If not allowed to access this module, bounce to the default dashboard for their role
    const dashboardSlug = role.toLowerCase().replace(/\s+/g, '-');
    return <Navigate to={`/${dashboardSlug}/dashboard`} replace />;
  }

  // Filter navigation configs strictly based on permissions configuration
  const filteredNavigation = filterNavigationItems(role, navigationConfig);

  return (
    <div className="min-h-screen bg-bg-cream flex text-text-primary antialiased">
      {/* Mobile Backdrop overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/30 backdrop-blur-xs md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar navigation presentation */}
      <Sidebar 
        navigationItems={filteredNavigation} 
        activeRole={role}
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
      />
      
      {/* Main page panel */}
      <div className="flex-grow flex flex-col min-h-screen min-w-0">
        <Topbar 
          user={user} 
          role={role} 
          setSidebarOpen={setSidebarOpen}
        />
        
        {/* Page body content container */}
        <main className="flex-1 p-[var(--spacing-page-py)] overflow-y-auto">
          <div className="max-w-7xl mx-auto w-full">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
