import api from './api/axios';

/**
 * Fetches the master list of vehicles from the backend API.
 */
export const getVehicles = async () => {
  const response = await api.get('/fleet/vehicles');
  return response.data.data.vehicles;
};

export default { getVehicles };
