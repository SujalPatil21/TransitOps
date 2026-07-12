import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

/**
 * PublicRoute ensures authenticated users cannot revisit public pages
 * (like login) and instead redirects them directly to their role-specific dashboard.
 */
const PublicRoute = ({ children }) => {
  const { isAuthenticated, role, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-bg-cream flex items-center justify-center">
        <div className="text-primary text-xl font-bold animate-pulse text-center">
          Loading TransitOps...
        </div>
      </div>
    );
  }

  if (isAuthenticated && role) {
    const dashboardSlug = role.toLowerCase().replace(/\s+/g, '-');
    return <Navigate to={`/${dashboardSlug}/dashboard`} replace />;
  }

  return children;
};

export default PublicRoute;
