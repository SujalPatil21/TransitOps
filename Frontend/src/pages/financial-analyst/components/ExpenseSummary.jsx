import React from 'react';
import StatCard from '../../../components/shared/StatCard';
import WidgetContainer from '../../../components/shared/WidgetContainer';

/**
 * ExpenseSummary Widget (Financial Analyst).
 * Displays total operational expenses, fuel costs, and maintenance charges.
 */
const ExpenseSummary = () => {
  return (
    <div className="space-y-4">
      <h3 className="text-xs font-bold text-text-secondary uppercase tracking-wider select-none">
        Expense Highlights
      </h3>
      <WidgetContainer>
        <StatCard 
          title="Total Operating Cost" 
          value="₹30,100" 
          icon="IndianRupee" 
          subtitle="Fuel + Maintenance + Tolls"
          status="info"
        />
        <StatCard 
          title="Fuel Expenses" 
          value="₹6,650" 
          icon="Fuel" 
          subtitle="Mocked fuel logs total"
          status="warning"
        />
        <StatCard 
          title="Maintenance Cost" 
          value="₹23,000" 
          icon="Wrench" 
          subtitle="Mocked repair logs total"
          status="danger"
        />
      </WidgetContainer>
    </div>
  );
};

export default ExpenseSummary;
