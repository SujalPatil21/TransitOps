import React from 'react';
import PageHeader from '../../components/shared/PageHeader';
import DriverCompliance from './components/DriverCompliance';
import SafetyAlerts from './components/SafetyAlerts';

/**
 * Safety Officer Dashboard Page (Independent page).
 * Assembles subsections for driver compliance KPIs and safety warnings.
 */
const Dashboard = () => {
  return (
    <div className="space-y-[var(--spacing-section-gap)]">
      <PageHeader 
        title="Safety Dashboard" 
        subtitle="Manage license compliance checks, track safety scores, and log incidents."
      />
      
      {/* Driver safety details row */}
      <DriverCompliance />
      
      {/* Alert panels layout */}
      <div className="grid grid-cols-1 gap-[var(--spacing-section-gap)]">
        <SafetyAlerts />
      </div>
    </div>
  );
};

export default Dashboard;
