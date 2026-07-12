import React, { useState, useEffect } from 'react';
import SectionCard from '../../../components/shared/SectionCard';
import Badge from '../../../components/ui/Badge';
import { getMaintenanceLogs } from '../../../services/maintenanceService';
import { MAINTENANCE_STATUS } from '../../../constants/maintenanceStatus';

/**
 * MaintenanceAlerts Widget (Fleet Manager).
 * Renders active fleet maintenance alert logs loaded dynamically.
 */
const MaintenanceAlerts = () => {
  const [loading, setLoading] = useState(true);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    let active = true;
    const fetchLogs = async () => {
      try {
        const allLogs = await getMaintenanceLogs();
        if (active) {
          // Filter for active/open logs
          const activeLogs = allLogs.filter(log => log.status === MAINTENANCE_STATUS.ACTIVE);
          setLogs(activeLogs);
        }
      } catch (err) {
        console.error('Failed to fetch maintenance logs', err);
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };
    fetchLogs();
    return () => {
      active = false;
    };
  }, []);

  return (
    <SectionCard title="Active Maintenance Logs">
      {loading ? (
        <div className="divide-y divide-border-light/60 animate-pulse" aria-hidden="true">
          {Array.from({ length: 2 }).map((_, idx) => (
            <div key={idx} className="py-3 flex items-center justify-between first:pt-0">
              <div className="space-y-2">
                <div className="h-3.5 w-32 bg-border-warm rounded" />
                <div className="h-3 w-48 bg-border-warm/65 rounded" />
              </div>
              <div className="h-5 w-16 bg-border-warm/40 rounded-full" />
            </div>
          ))}
        </div>
      ) : logs.length === 0 ? (
        <div className="py-8 text-center text-xs font-semibold text-text-secondary select-none">
          ✓ No active maintenance logs reported.
        </div>
      ) : (
        <div className="divide-y divide-border-light/60 select-none">
          {logs.map((log, idx) => (
            <div 
              key={log.id} 
              className={`py-3 flex items-center justify-between ${idx === 0 ? 'first:pt-0' : ''} ${idx === logs.length - 1 ? 'last:pb-0' : ''}`}
            >
              <div>
                <span className="text-xs font-bold text-text-primary block">
                  {log.vehicleRegNo} · {log.vehicleModel}
                </span>
                <span className="text-[11px] text-text-secondary font-medium">
                  {log.description}
                </span>
              </div>
              <Badge status={log.status} />
            </div>
          ))}
        </div>
      )}
    </SectionCard>
  );
};

export default MaintenanceAlerts;
