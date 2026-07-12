import React, { useState, useEffect } from 'react';
import SectionCard from '../../../components/shared/SectionCard';
import { getVehicles } from '../../../services/vehicleService';
import { VEHICLE_STATUS } from '../../../constants/vehicleStatus';

/**
 * VehicleStatus Widget (Fleet Manager).
 * Displays progress bars showing vehicle status percentages computed dynamically.
 */
const VehicleStatus = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    available: 0,
    onTrip: 0,
    inShop: 0,
    total: 0
  });

  useEffect(() => {
    let active = true;
    const fetchStats = async () => {
      try {
        const vehicles = await getVehicles();
        if (active) {
          const availCount = vehicles.filter(v => v.status === VEHICLE_STATUS.AVAILABLE).length;
          const tripCount = vehicles.filter(v => v.status === VEHICLE_STATUS.ON_TRIP).length;
          const shopCount = vehicles.filter(v => v.status === VEHICLE_STATUS.IN_SHOP).length;
          // Count all except retired as active total, or count all. Let's count all.
          const totalCount = vehicles.length;

          setStats({
            available: availCount,
            onTrip: tripCount,
            inShop: shopCount,
            total: totalCount
          });
        }
      } catch (err) {
        console.error('Failed to compute vehicle stats', err);
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };
    fetchStats();
    return () => {
      active = false;
    };
  }, []);

  // Safe percentage helper
  const getPct = (val) => {
    if (!stats.total) return 0;
    return Math.round((val / stats.total) * 100);
  };

  return (
    <SectionCard title="Vehicle Status Distribution">
      {loading ? (
        <div className="space-y-5 py-2 animate-pulse" aria-hidden="true">
          {Array.from({ length: 3 }).map((_, idx) => (
            <div key={idx} className="space-y-2">
              <div className="h-3 w-24 bg-border-warm rounded" />
              <div className="h-2 w-full bg-border-warm/40 rounded-full" />
            </div>
          ))}
        </div>
      ) : (
        <div className="space-y-4 py-2 select-none">
          <div>
            <div className="flex justify-between text-xs font-bold text-text-primary mb-1.5">
              <span>Available</span>
              <span>{stats.available} / {stats.total} ({getPct(stats.available)}%)</span>
            </div>
            <div className="h-2 w-full bg-status-avail-bg rounded-full overflow-hidden">
              <div 
                className="h-full bg-status-avail-text rounded-full transition-all duration-500" 
                style={{ width: `${getPct(stats.available)}%` }}
              />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-bold text-text-primary mb-1.5">
              <span>On Trip</span>
              <span>{stats.onTrip} / {stats.total} ({getPct(stats.onTrip)}%)</span>
            </div>
            <div className="h-2 w-full bg-status-trip-bg rounded-full overflow-hidden">
              <div 
                className="h-full bg-status-trip-text rounded-full transition-all duration-500" 
                style={{ width: `${getPct(stats.onTrip)}%` }}
              />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-bold text-text-primary mb-1.5">
              <span>In Shop / Maintenance</span>
              <span>{stats.inShop} / {stats.total} ({getPct(stats.inShop)}%)</span>
            </div>
            <div className="h-2 w-full bg-status-maint-bg rounded-full overflow-hidden">
              <div 
                className="h-full bg-status-maint-text rounded-full transition-all duration-500" 
                style={{ width: `${getPct(stats.inShop)}%` }}
              />
            </div>
          </div>
        </div>
      )}
    </SectionCard>
  );
};

export default VehicleStatus;
