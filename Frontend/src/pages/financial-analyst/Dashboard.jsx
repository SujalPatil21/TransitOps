import React from 'react';
import PageHeader from '../../components/shared/PageHeader';
import ExpenseSummary from './components/ExpenseSummary';
import CostBreakdown from './components/CostBreakdown';

/**
 * Financial Analyst Dashboard Page (Independent page).
 * Assembles subsections for operational costs and vehicle breakdowns.
 */
const Dashboard = () => {
  return (
    <div className="space-y-[var(--spacing-section-gap)]">
      <PageHeader 
        title="Financial Dashboard" 
        subtitle="Review fuel costs, total maintenance, operational ROI, and expense splits."
      />
      
      {/* Financial counters */}
      <ExpenseSummary />
      
      {/* Split breakdown grids */}
      <div className="grid grid-cols-1 gap-[var(--spacing-section-gap)]">
        <CostBreakdown />
      </div>
    </div>
  );
};

export default Dashboard;
