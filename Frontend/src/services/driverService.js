import { DRIVER_STATUS } from '../constants/driverStatus';

/**
 * Fetches the master list of drivers.
 * Mirrors the future GET /api/drivers response structure.
 */
export const getDrivers = async () => {
  return Promise.resolve([
    {
      id: 1,
      name: 'Alex',
      licenseNo: 'DL-88213',
      category: 'LMV',
      expiryDate: '2028-12-31', // Valid
      contact: '9876500123',
      tripCompletion: '96%',
      safetyScore: 96,
      status: DRIVER_STATUS.AVAILABLE
    },
    {
      id: 2,
      name: 'John',
      licenseNo: 'DL-44120',
      category: 'HMV',
      expiryDate: '2025-03-15', // Expired
      contact: '9822004567',
      tripCompletion: '81%',
      safetyScore: 81,
      status: DRIVER_STATUS.SUSPENDED
    },
    {
      id: 3,
      name: 'Priya',
      licenseNo: 'DL-77031',
      category: 'LMV',
      expiryDate: '2029-08-20', // Valid
      contact: '9911009876',
      tripCompletion: '99%',
      safetyScore: 99,
      status: DRIVER_STATUS.ON_TRIP
    },
    {
      id: 4,
      name: 'Suresh',
      licenseNo: 'DL-90045',
      category: 'HMV',
      expiryDate: '2027-01-10', // Valid
      contact: '9744005432',
      tripCompletion: '88%',
      safetyScore: 88,
      status: DRIVER_STATUS.OFF_DUTY
    }
  ]);
};

export default { getDrivers };
