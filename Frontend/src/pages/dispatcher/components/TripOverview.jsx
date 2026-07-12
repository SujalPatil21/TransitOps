import React from 'react';
import StatCard from '../../../components/shared/StatCard';
import WidgetContainer from '../../../components/shared/WidgetContainer';

/**
 * TripOverview Widget (Dispatcher).
 * Displays active trips, pending runs, and driver duty metrics.
 */
const TripOverview = () => {
  return (
    <div className="space-y-4">
      <h3 className="text-xs font-bold text-text-secondary uppercase tracking-wider select-none">
        Dispatch Operations
      </h3>
      <WidgetContainer>
        <StatCard 
          title="Active Trips" 
          value="18" 
          icon="Navigation" 
          subtitle="Trips currently on road"
          status="info"
        />
        <StatCard 
          title="Pending Trips" 
          value="9" 
          icon="Clock" 
          subtitle="Awaiting vehicle/driver"
          status="warning"
        />
        <StatCard 
          title="Drivers On Duty" 
          value="26" 
          icon="Users" 
          subtitle="Active driver profiles"
          status="available"
        />
      </WidgetContainer>
    </div>
  );
};

export default TripOverview;
