import api from './api/axios';

/**
 * Fetches the master list of drivers from the backend API.
 */
export const getDrivers = async () => {
  const response = await api.get('/safety/drivers');
  return response.data.data.drivers;
};

export default { getDrivers };
