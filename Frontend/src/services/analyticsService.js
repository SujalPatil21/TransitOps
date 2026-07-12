import api from './api/axios';

/**
 * Fetches the list of dashboard KPIs.
 * Queries GET /analytics/kpis with a console warning warning and mock fallback.
 */
export const getKPIs = async () => {
  try {
    const response = await api.get('/analytics/kpis');
    // If backend returns { success: true, data: { ... } }
    if (response.data && response.data.success) {
      return response.data.data;
    }
    return response.data;
  } catch (error) {
    console.warn('analyticsService.getKPIs: Offline/unreachable. Loading offline mock metadata.', error.message);
    return {
      activeVehicles: 53,
      availableVehicles: 42,
      vehiclesInMaintenance: 5,
      activeTrips: 18,
      pendingTrips: 9,
      driversOnDuty: 26,
      fleetUtilization: 81 // %
    };
  }
};

/**
 * Fetches ROI and cost metrics per vehicle.
 * Queries GET /analytics/roi with a console warning and mock fallback.
 */
export const getVehicleROI = async () => {
  try {
    const response = await api.get('/analytics/roi');
    if (response.data && response.data.success) {
      return response.data.data;
    }
    return response.data;
  } catch (error) {
    console.warn('analyticsService.getVehicleROI: Offline/unreachable. Loading offline mock metadata.', error.message);
    return [
      {
        vehicle: 'VAN-05',
        fuelEfficiency: '12.5 km/L',
        operationalCost: 8300, // fuel + maintenance
        revenue: 25000,
        acquisitionCost: 620000,
        roi: 2.69 // %
      },
      {
        vehicle: 'TRUCK-11',
        fuelEfficiency: '4.8 km/L',
        operationalCost: 18950,
        revenue: 85000,
        acquisitionCost: 2450000,
        roi: 2.69 // %
      },
      {
        vehicle: 'MINI-03',
        fuelEfficiency: '9.2 km/L',
        operationalCost: 4050,
        revenue: 15000,
        acquisitionCost: 410000,
        roi: 2.67 // %
      }
    ];
  }
};

export default { getKPIs, getVehicleROI };
