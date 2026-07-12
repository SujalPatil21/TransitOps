import api from './api/axios';

/**
 * Fetches real-time dashboard KPIs from the backend.
 * Computed from live PostgreSQL data.
 */
export const getKPIs = async () => {
  const response = await api.get('/analytics/kpis');
  return response.data.data;
};

/**
 * Fetches per-vehicle ROI metrics from the backend.
 */
export const getVehicleROI = async () => {
  const response = await api.get('/analytics/roi');
  return response.data.data;
};

export default { getKPIs, getVehicleROI };

