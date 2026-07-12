import { EXPENSE_TYPES } from '../constants/fuelTypes';

/**
 * Fetches the list of fuel logs and expenses.
 * Mirrors the future GET /api/expenses response contract.
 */
export const getExpenses = async () => {
  return Promise.resolve([
    {
      id: 1,
      vehicleRegNo: 'GJ01AB4521',
      vehicleModel: 'VAN-05',
      type: EXPENSE_TYPES.FUEL,
      amount: 3800, // INR
      volume: 40, // Liters
      date: '2026-07-02',
      notes: 'Shell Petrol Pump Naroda'
    },
    {
      id: 2,
      vehicleRegNo: 'GJ01AB9981',
      vehicleModel: 'TRUCK-11',
      type: EXPENSE_TYPES.TOLL,
      amount: 450,
      volume: 0,
      date: '2026-07-05',
      notes: 'Expressway Ahmedabad-Baroda Toll'
    },
    {
      id: 3,
      vehicleRegNo: 'GJ01AB1120',
      vehicleModel: 'MINI-03',
      type: EXPENSE_TYPES.FUEL,
      amount: 2850,
      volume: 30,
      date: '2026-07-08',
      notes: 'Nayara Fuel Station Sanand'
    },
    {
      id: 4,
      vehicleRegNo: 'GJ01AB4521',
      vehicleModel: 'VAN-05',
      type: EXPENSE_TYPES.MAINTENANCE,
      amount: 4500,
      volume: 0,
      date: '2026-06-26',
      notes: 'Tune-up charges from logs'
    }
  ]);
};

export default { getExpenses };
