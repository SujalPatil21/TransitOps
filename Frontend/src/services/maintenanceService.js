import api from './api/axios';
import { MAINTENANCE_STATUS } from '../constants/maintenanceStatus';

/**
 * Fetches the list of maintenance logs.
 * Queries GET /maintenance with mock fallback if offline.
 */
export const getMaintenanceLogs = async () => {
  try {
    const response = await api.get('/maintenance');
    if (response.data && response.data.success) {
      return response.data.data;
    }
    return response.data;
  } catch (error) {
    console.warn('maintenanceService.getMaintenanceLogs: Offline/unreachable. Loading offline mock metadata.', error.message);
    return [
      {
        id: 1,
        vehicleRegNo: 'GJ01AB1120',
        vehicleModel: 'MINI-03',
        description: 'Oil Change & Brake Inspection',
        startDate: '2026-07-10',
        endDate: '—',
        cost: 1200,
        status: MAINTENANCE_STATUS.ACTIVE
      },
      {
        id: 2,
        vehicleRegNo: 'GJ01AB4521',
        vehicleModel: 'VAN-05',
        description: 'Engine Tuning & Spark Plug Replacement',
        startDate: '2026-06-25',
        endDate: '2026-06-26',
        cost: 4500,
        status: MAINTENANCE_STATUS.CLOSED
      },
      {
        id: 3,
        vehicleRegNo: 'GJ01AB9981',
        vehicleModel: 'TRUCK-11',
        description: 'Transmission Fluid Flush & Tire Rotation',
        startDate: '2026-05-12',
        endDate: '2026-05-13',
        cost: 18500,
        status: MAINTENANCE_STATUS.CLOSED
      }
    ];
  }
};

export default { getMaintenanceLogs };
