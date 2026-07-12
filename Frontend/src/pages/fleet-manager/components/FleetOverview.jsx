import React, { useState, useEffect } from 'react';
import StatCard from '../../../components/shared/StatCard';
import WidgetContainer from '../../../components/shared/WidgetContainer';
import { getKPIs } from '../../../services/analyticsService';

/**
 * FleetOverview Widget (Fleet Manager).
 * Renders fleet KPI summary statistics cards asynchronously with pulse skeletons.
 */
const FleetOverview = () => {
  const [loading, setLoading] = useState(true);
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    let active = true;
    const loadKPIs = async () => {
      try {
        const data = await getKPIs();
        if (active) {
          setKpis(data);
        }
      } catch (err) {
        console.error('Failed to load Fleet KPIs', err);
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };
    loadKPIs();
    return () => {
      active = false;
    };
  }, []);

  return (
    <div className="space-y-4">
      <h3 className="text-xs font-bold text-text-secondary uppercase tracking-wider select-none">
        Fleet Overview Metrics
      </h3>

      {loading ? (
        <WidgetContainer>
          {Array.from({ length: 3 }).map((_, idx) => (
            <div 
              key={idx} 
              className="h-[108px] w-full bg-card-warm/50 border border-border-warm rounded-[var(--radius-card)] animate-pulse" 
              aria-hidden="true"
            />
          ))}
        </WidgetContainer>
      ) : (
        <WidgetContainer>
          <StatCard 
            title="Active Vehicles" 
            value={kpis?.activeVehicles || '0'} 
            icon="Truck" 
            subtitle="Registered in system"
            status="info"
          />
          <StatCard 
            title="Available Vehicles" 
            value={kpis?.availableVehicles || '0'} 
            icon="CheckCircle" 
            subtitle="Ready for dispatch"
            status="available"
          />
          <StatCard 
            title="In Maintenance" 
            value={kpis?.vehiclesInMaintenance || '0'} 
            icon="Wrench" 
            subtitle="Currently in shop"
            status="maintenance"
          />
        </WidgetContainer>
      )}
    </div>
  );
};

export default FleetOverview;
