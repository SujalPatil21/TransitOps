import React from 'react';
import SectionCard from '../../../components/shared/SectionCard';
import Badge from '../../../components/ui/Badge';

/**
 * DispatchQueue Widget (Dispatcher).
 * Displays a list of active and pending dispatch runs, routes, and statuses.
 */
const DispatchQueue = () => {
  return (
    <SectionCard title="Recent Dispatch Runs">
      <div className="divide-y divide-border-light/60 select-none">
        <div className="py-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 first:pt-0">
          <div>
            <span className="text-xs font-bold text-text-primary block">TR001 · VAN-05 / Alex</span>
            <span className="text-[11px] text-text-secondary font-medium">Gandhinagar Depot ➔ Ahmedabad Hub</span>
          </div>
          <div className="flex items-center gap-3 justify-between sm:justify-start">
            <span className="text-[10px] font-bold text-text-secondary">ETA 45 MIN</span>
            <Badge status="dispatched" />
          </div>
        </div>
        
        <div className="py-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <span className="text-xs font-bold text-text-primary block">TR003 · MINI-08 / Priya</span>
            <span className="text-[11px] text-text-secondary font-medium">Sarkhej Depot ➔ Bavla Warehouse</span>
          </div>
          <div className="flex items-center gap-3 justify-between sm:justify-start">
            <span className="text-[10px] font-bold text-text-secondary">ETA 1H 10M</span>
            <Badge status="dispatched" />
          </div>
        </div>

        <div className="py-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 last:pb-0">
          <div>
            <span className="text-xs font-bold text-text-primary block">TR004 · TRUCK-04 / Suresh</span>
            <span className="text-[11px] text-text-secondary font-medium">Vatva Industrial Area ➔ Sanand Warehouse</span>
          </div>
          <div className="flex items-center gap-3 justify-between sm:justify-start">
            <span className="text-[10px] font-bold text-text-secondary">AWAITING DRIVER</span>
            <Badge status="draft" />
          </div>
        </div>
      </div>
    </SectionCard>
  );
};

export default DispatchQueue;
