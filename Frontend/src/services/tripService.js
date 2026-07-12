import { TRIP_STATUS } from '../constants/tripStatus';

/**
 * Fetches the list of active/logged trips.
 * Mirrors the future GET /api/trips response contract.
 */
export const getTrips = async () => {
  return Promise.resolve([
    {
      id: 'TR001',
      vehicle: 'VAN-05',
      driver: 'Alex',
      source: 'Gandhinagar Depot',
      destination: 'Ahmedabad Hub',
      cargoWeight: 450, // kg
      plannedDistance: 32, // km
      status: TRIP_STATUS.DISPATCHED, // "On Trip" / Dispatched
      eta: '45 min'
    },
    {
      id: 'TR002',
      vehicle: 'TRK-12',
      driver: 'John',
      source: 'Naroda GIDC',
      destination: 'Baroda Logistics Park',
      cargoWeight: 4000,
      plannedDistance: 110,
      status: TRIP_STATUS.COMPLETED,
      eta: '—'
    },
    {
      id: 'TR003',
      vehicle: 'MINI-08',
      driver: 'Priya',
      source: 'Sarkhej Depot',
      destination: 'Bavla Warehouse',
      cargoWeight: 800,
      plannedDistance: 25,
      status: TRIP_STATUS.DISPATCHED,
      eta: '1h 10m'
    },
    {
      id: 'TR004',
      vehicle: 'TRUCK-04',
      driver: 'Suresh',
      source: 'Vatva Industrial Area',
      destination: 'Sanand Warehouse',
      cargoWeight: 4200,
      plannedDistance: 45,
      status: TRIP_STATUS.DRAFT,
      eta: 'Awaiting driver'
    },
    {
      id: 'TR006',
      vehicle: '—',
      driver: '—',
      source: 'Mansa',
      destination: 'Kalol Depot',
      cargoWeight: 0,
      plannedDistance: 18,
      status: TRIP_STATUS.CANCELLED,
      eta: 'Vehicle went to shop'
    }
  ]);
};

export default { getTrips };
