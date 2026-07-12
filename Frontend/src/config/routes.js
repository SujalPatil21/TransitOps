import LandingPage from '../pages/landing/LandingPage';
import LoginPage from '../pages/login/LoginPage';
import FleetDashboard from '../pages/fleet-manager/Dashboard';
import DispatcherDashboard from '../pages/dispatcher/Dashboard';
import SafetyDashboard from '../pages/safety-officer/Dashboard';
import FinancialDashboard from '../pages/financial-analyst/Dashboard';
import VehicleRegistry from '../pages/vehicles/VehicleRegistry';
import DriverManagement from '../pages/drivers/DriverManagement';
import TripManagement from '../pages/trips/TripManagement';
import Maintenance from '../pages/maintenance/Maintenance';
import FuelExpense from '../pages/fuel-expense/FuelExpense';
import ReportsAnalytics from '../pages/analytics/ReportsAnalytics';
import Settings from '../pages/settings/Settings';

export const routeConfig = [
  // Public routes
  { path: '/', element: LandingPage, public: true },
  { path: '/login', element: LoginPage, public: true },

  // Role Dashboard routes
  { path: '/fleet-manager/dashboard', element: FleetDashboard, protected: true },
  { path: '/dispatcher/dashboard', element: DispatcherDashboard, protected: true },
  { path: '/safety-officer/dashboard', element: SafetyDashboard, protected: true },
  { path: '/financial-analyst/dashboard', element: FinancialDashboard, protected: true },

  // Resource Module routes
  { path: '/vehicles', element: VehicleRegistry, protected: true },
  { path: '/drivers', element: DriverManagement, protected: true },
  { path: '/trips', element: TripManagement, protected: true },
  { path: '/maintenance', element: Maintenance, protected: true },
  { path: '/fuel-expense', element: FuelExpense, protected: true },
  { path: '/analytics', element: ReportsAnalytics, protected: true },
  { path: '/settings', element: Settings, protected: true }
];
