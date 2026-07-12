import React from 'react';
import StatCard from '../../../components/shared/StatCard';
import WidgetContainer from '../../../components/shared/WidgetContainer';

/**
 * DriverCompliance Widget (Safety Officer).
 * Displays safety compliance rates and pending alerts.
 */
const DriverCompliance = () => {
  return (
    <div className="space-y-4">
      <h3 className="text-xs font-bold text-text-secondary uppercase tracking-wider select-none">
        Driver Compliance Summary
      </h3>
      <WidgetContainer>
        <StatCard 
          title="Overall Compliance" 
          value="94%" 
          icon="ShieldAlert" 
          subtitle="Passed safety guidelines"
          status="available"
        />
        <StatCard 
          title="Expired Licenses" 
          value="1" 
          icon="FileText" 
          subtitle="Requires immediate renewal"
          status="danger"
        />
        <StatCard 
          title="Safety Alerts" 
          value="2" 
          icon="AlertTriangle" 
          subtitle="Recent safety incidents"
          status="warning"
        />
      </WidgetContainer>
    </div>
  );
};

export default DriverCompliance;
