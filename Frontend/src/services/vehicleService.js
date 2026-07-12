import api from './api/axios';
import { VEHICLE_STATUS } from '../constants/vehicleStatus';

/**
 * Fetches the master list of vehicles.
 * Queries GET /vehicles with mock fallback if offline.
 */
export const getVehicles = async () => {
  try {
    const response = await api.get('/vehicles');
    if (response.data && response.data.success) {
      return response.data.data;
    }
    return response.data;
  } catch (error) {
    console.warn('vehicleService.getVehicles: Offline/unreachable. Loading offline mock metadata.', error.message);
    return [
      { 
        id: 1, 
        regNo: 'GJ01AB4521', 
        model: 'VAN-05', 
        type: 'Van', 
        capacity: 500, // kg
        odometer: 74000, 
        cost: 620000, 
        status: VEHICLE_STATUS.AVAILABLE 
      },
      { 
        id: 2, 
        regNo: 'GJ01AB9981', 
        model: 'TRUCK-11', 
        type: 'Truck', 
        capacity: 5000, // kg (5 Ton)
        odometer: 182000, 
        cost: 2450000, 
        status: VEHICLE_STATUS.ON_TRIP 
      },
      { 
        id: 3, 
        regNo: 'GJ01AB1120', 
        model: 'MINI-03', 
        type: 'Mini', 
        capacity: 1000, // kg (1 Ton)
        odometer: 66000, 
        cost: 410000, 
        status: VEHICLE_STATUS.IN_SHOP 
      },
      { 
        id: 4, 
        regNo: 'GJ01AB0008', 
        model: 'VAN-09', 
        type: 'Van', 
        capacity: 750, // kg
        odometer: 241900, 
        cost: 590000, 
        status: VEHICLE_STATUS.RETIRED 
      }
    ];
  }
};

export default { getVehicles };
