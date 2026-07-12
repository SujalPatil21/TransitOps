import React from 'react';
import PageHeader from '../../components/shared/PageHeader';
import FleetOverview from './components/FleetOverview';
import VehicleStatus from './components/VehicleStatus';
import MaintenanceAlerts from './components/MaintenanceAlerts';

/**
 * Fleet Manager Dashboard Page (Independent page).
 * Assembles subsections for Fleet overview metrics, status distribution, and active alerts.
 */
const Dashboard = () => {
  return (
    <div className="space-y-[var(--spacing-section-gap)]">
      <PageHeader 
        title="Fleet Dashboard" 
        subtitle="Real-time registry oversight, capacity utilization, and maintenance status."
      />
      
      {/* Overview Metric Row */}
      <FleetOverview />
      
      {/* Detailed status split grids */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-[var(--spacing-section-gap)]">
        <VehicleStatus />
        <MaintenanceAlerts />
      </div>
    </div>
  );
};

export default Dashboard;
