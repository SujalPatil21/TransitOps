import { ROLES } from './roles';

// Centralized Route Permissions mapping
export const routePermissions = {
  // Finalized Dashboard routes
  '/fleet-manager/dashboard': [ROLES.FLEET_MANAGER],
  '/dispatcher/dashboard': [ROLES.DISPATCHER],
  '/safety-officer/dashboard': [ROLES.SAFETY_OFFICER],
  '/financial-analyst/dashboard': [ROLES.FINANCIAL_ANALYST],

  // TODO: Final RBAC mappings for resource pages will be set after backend permission matrix is finalized
  '/vehicles': [],
  '/drivers': [],
  '/trips': [],
  '/maintenance': [],
  '/fuel-expense': [],
  '/analytics': [],
  '/settings': []
};

// Centralized Navigation Menu visibility mapping
export const navigationPermissions = {
  '/:role/dashboard': Object.values(ROLES),
  '/vehicles': [ROLES.FLEET_MANAGER, ROLES.DISPATCHER],
  '/drivers': [ROLES.DISPATCHER, ROLES.SAFETY_OFFICER],
  '/trips': [ROLES.DISPATCHER],
  '/maintenance': [ROLES.FLEET_MANAGER],
  '/fuel-expense': [ROLES.FINANCIAL_ANALYST],
  '/analytics': [ROLES.FINANCIAL_ANALYST],
  '/settings': Object.values(ROLES)
};

/**
 * Checks if a given role has access to a specific route path.
 */
export const hasRouteAccess = (role, path) => {
  let allowedRoles = routePermissions[path];

  if (!allowedRoles) {
    const keys = Object.keys(routePermissions);
    for (const key of keys) {
      const regex = new RegExp('^' + key.replace(/:\w+/g, '[^/]+') + '$');
      if (regex.test(path)) {
        allowedRoles = routePermissions[key];
        break;
      }
    }
  }

  if (!allowedRoles) return true; // Unmapped paths are open by default
  if (allowedRoles.length === 0) return true; // Placeholders open in Phase 1
  return allowedRoles.includes(role);
};

/**
 * Filters standard navigation items based on the user's role and navigationPermissions configuration.
 */
export const filterNavigationItems = (role, navigationItems) => {
  return navigationItems.filter(item => {
    const allowedRoles = navigationPermissions[item.path];
    if (!allowedRoles) return true; // If unmapped, default visible
    return allowedRoles.includes(role);
  });
};
