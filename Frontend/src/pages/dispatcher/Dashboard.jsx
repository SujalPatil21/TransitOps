import React from 'react';
import PageHeader from '../../components/shared/PageHeader';
import TripOverview from './components/TripOverview';
import DispatchQueue from './components/DispatchQueue';

/**
 * Dispatcher Dashboard Page (Independent page).
 * Assembles subsections for dispatch KPIs and recent dispatch queues.
 */
const Dashboard = () => {
  return (
    <div className="space-y-[var(--spacing-section-gap)]">
      <PageHeader 
        title="Dispatcher Dashboard" 
        subtitle="Monitor active trips, dispatch pending orders, and track driver schedules."
      />
      
      {/* Dispatch operations counters */}
      <TripOverview />
      
      {/* Dispatch queues list */}
      <div className="grid grid-cols-1 gap-[var(--spacing-section-gap)]">
        <DispatchQueue />
      </div>
    </div>
  );
};

export default Dashboard;
