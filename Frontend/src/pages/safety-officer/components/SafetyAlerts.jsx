import React from 'react';
import SectionCard from '../../../components/shared/SectionCard';
import Badge from '../../../components/ui/Badge';

/**
 * SafetyAlerts Widget (Safety Officer).
 * Lists urgent driver compliance warnings and license expirations.
 */
const SafetyAlerts = () => {
  return (
    <SectionCard title="Immediate Compliance Actions">
      <div className="divide-y divide-border-light/60 select-none">
        <div className="py-3.5 flex items-center justify-between first:pt-0">
          <div>
            <span className="text-xs font-bold text-text-primary block">John (DL-44120)</span>
            <span className="text-[11px] text-text-secondary font-medium">Category: HMV · Expired: 15-Mar-2025</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-[9px] font-extrabold text-primary uppercase tracking-wider px-2 py-0.5 rounded bg-primary/10">EXPIRED</span>
            <Badge status="suspended" />
          </div>
        </div>
        
        <div className="py-3.5 flex items-center justify-between last:pb-0">
          <div>
            <span className="text-xs font-bold text-text-primary block">Suresh (DL-90045)</span>
            <span className="text-[11px] text-text-secondary font-medium">Category: HMV · Expiring: 10-Jan-2027</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-[9px] font-extrabold text-text-secondary uppercase tracking-wider px-2 py-0.5 rounded bg-bg-cream">VALID</span>
            <Badge status="off_duty" />
          </div>
        </div>
      </div>
    </SectionCard>
  );
};

export default SafetyAlerts;
