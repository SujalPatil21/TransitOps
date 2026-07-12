import api from './api/axios';

/**
 * Note: Dispatcher/Trip backend module is not yet implemented.
 * Returns empty dataset until the backend endpoint is available.
 */
export const getTrips = async () => {
  const response = await api.get('/dispatcher/trips');
  return response.data.data.trips;
};

export default { getTrips };

