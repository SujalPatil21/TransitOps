import React from 'react';
import SectionCard from '../../../components/shared/SectionCard';

/**
 * CostBreakdown Widget (Financial Analyst).
 * Displays cost distributions per vehicle using styled bar graphics.
 */
const CostBreakdown = () => {
  return (
    <SectionCard title="Operating Cost Distribution">
      <div className="space-y-4 py-2 select-none">
        <div>
          <div className="flex justify-between text-xs font-bold text-text-primary mb-1.5">
            <span>GJ01AB9981 · TRUCK-11</span>
            <span>₹18,950</span>
          </div>
          <div className="h-2 w-full bg-status-cancel-bg rounded-full overflow-hidden">
            <div className="h-full bg-primary rounded-full" style={{ width: '100%' }}></div>
          </div>
        </div>

        <div>
          <div className="flex justify-between text-xs font-bold text-text-primary mb-1.5">
            <span>GJ01AB4521 · VAN-05</span>
            <span>₹8,300</span>
          </div>
          <div className="h-2 w-full bg-status-cancel-bg rounded-full overflow-hidden">
            <div className="h-full bg-primary rounded-full" style={{ width: '43%' }}></div>
          </div>
        </div>

        <div>
          <div className="flex justify-between text-xs font-bold text-text-primary mb-1.5">
            <span>GJ01AB1120 · MINI-03</span>
            <span>₹2,850</span>
          </div>
          <div className="h-2 w-full bg-status-cancel-bg rounded-full overflow-hidden">
            <div className="h-full bg-primary rounded-full" style={{ width: '15%' }}></div>
          </div>
        </div>
      </div>
    </SectionCard>
  );
};

export default CostBreakdown;
