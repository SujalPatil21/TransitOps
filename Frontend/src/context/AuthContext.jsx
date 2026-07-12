import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [role, setRole] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Restore authenticated session state on application mount
  useEffect(() => {
    try {
      const storedUser = localStorage.getItem('transitops_user');
      const storedRole = localStorage.getItem('transitops_role');
      const storedToken = localStorage.getItem('transitops_token');

      if (storedToken && storedUser && storedRole) {
        setUser(JSON.parse(storedUser));
        setRole(storedRole);
        setIsAuthenticated(true);
      }
    } catch (e) {
      console.error('Failed to restore session:', e);
    } finally {
      setLoading(false);
    }

    // Event listener to automatically process 401 logs
    const handleUnauthorized = () => {
      logout();
    };

    window.addEventListener('auth-unauthorized', handleUnauthorized);
    return () => {
      window.removeEventListener('auth-unauthorized', handleUnauthorized);
    };
  }, []);

  /**
   * Initializes the session with user details, role title, and JWT token.
   * Updates state variables and synchronizes with localStorage.
   */
  const setSession = (userData, roleData, tokenData) => {
    setUser(userData);
    setRole(roleData);
    setIsAuthenticated(true);

    if (tokenData) {
      localStorage.setItem('transitops_token', tokenData);
    }
    if (userData) {
      localStorage.setItem('transitops_user', JSON.stringify(userData));
    }
    if (roleData) {
      localStorage.setItem('transitops_role', roleData);
    }
  };

  /**
   * Logs out the user session.
   * Resets active states and deletes storage parameters.
   */
  const logout = () => {
    setUser(null);
    setRole(null);
    setIsAuthenticated(false);
    localStorage.removeItem('transitops_user');
    localStorage.removeItem('transitops_role');
    localStorage.removeItem('transitops_token');
  };

  return (
    <AuthContext.Provider value={{ user, role, isAuthenticated, loading, setSession, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
