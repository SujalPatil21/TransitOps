import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/shared/ProtectedRoute';
import PublicRoute from './components/shared/PublicRoute';
import PublicLayout from './layouts/PublicLayout';
import DashboardLayout from './layouts/DashboardLayout';
import { routeConfig } from './config/routes';

/**
 * Main App Router Component.
 * Wraps routes in AuthProvider, maps public and private paths dynamically 
 * from routes.js configurations, and enforces dynamic guards.
 */
function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Pages Wrapper */}
          <Route element={<PublicLayout />}>
            {routeConfig
              .filter(route => route.public)
              .map(route => {
                const PageComponent = route.element;
                return (
                  <Route
                    key={route.path}
                    path={route.path}
                    element={
                      <PublicRoute>
                        <PageComponent />
                      </PublicRoute>
                    }
                  />
                );
              })}
          </Route>

          {/* Authenticated Dashboard Pages Wrapper */}
          <Route element={<DashboardLayout />}>
            {routeConfig
              .filter(route => route.protected)
              .map(route => {
                const PageComponent = route.element;
                return (
                  <Route
                    key={route.path}
                    path={route.path}
                    element={
                      <ProtectedRoute>
                        <PageComponent />
                      </ProtectedRoute>
                    }
                  />
                );
              })}
          </Route>

          {/* Catch-all fallback */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
