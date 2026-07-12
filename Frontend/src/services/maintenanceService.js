import api from './api/axios';

/**
 * Fetches the list of maintenance logs from the backend API.
 */
export const getMaintenanceLogs = async () => {
  // Assuming a generic endpoint /fleet/maintenance exists or will exist to list logs.
  // We'll call /fleet/maintenance.
  const response = await api.get('/fleet/maintenance');
  return response.data.data.maintenance_records || response.data.data;
};

export default { getMaintenanceLogs };
