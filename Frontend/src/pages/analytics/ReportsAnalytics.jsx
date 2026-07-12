import React, { useState, useEffect } from 'react';
import PageHeader from '../../components/shared/PageHeader';
import SectionCard from '../../components/shared/SectionCard';
import DataTable from '../../components/shared/DataTable';
import StatCard from '../../components/shared/StatCard';
import WidgetContainer from '../../components/shared/WidgetContainer';
import Button from '../../components/ui/Button';
import { getVehicleROI } from '../../services/analyticsService';

/**
 * ReportsAnalytics Page.
 * Displays vehicle ROI, fuel efficiency summaries, and provides outline SVG placeholders for charts.
 */
const ReportsAnalytics = () => {
  const [roiData, setRoiData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    getVehicleROI().then((data) => {
      if (active) {
        setRoiData(data);
        setLoading(false);
      }
    });
    return () => { active = false; };
  }, []);

  const columns = [
    { header: 'Vehicle', accessor: 'vehicle' },
    { header: 'Fuel Efficiency', accessor: 'fuelEfficiency' },
    { 
      header: 'Total Op. Cost', 
      accessor: 'operationalCost', 
      render: (row) => `₹${row.operationalCost.toLocaleString()}` 
    },
    { 
      header: 'Revenue Generated', 
      accessor: 'revenue', 
      render: (row) => `₹${row.revenue.toLocaleString()}` 
    },
    { 
      header: 'Acq. Cost', 
      accessor: 'acquisitionCost', 
      render: (row) => `₹${row.acquisitionCost.toLocaleString()}` 
    },
    { 
      header: 'Vehicle ROI (%)', 
      accessor: 'roi', 
      render: (row) => (
        <span className="font-extrabold text-status-avail-text">
          {row.roi}%
        </span>
      ) 
    }
  ];

  return (
    <div className="space-y-[var(--spacing-section-gap)]">
      <PageHeader 
        title="Reports & Analytics" 
        subtitle="Review fleet utilization percentages, operational costs, fuel metrics, and calculated vehicle ROI."
        actions={
          <Button variant="secondary" onClick={() => alert('CSV Export triggered')}>
            💾 Export CSV
          </Button>
        }
      />

      {/* Summary KPI widgets */}
      <WidgetContainer>
        <StatCard 
          title="Overall Fleet Utilization" 
          value="81%" 
          icon="TrendingUp" 
          subtitle="Target threshold: 85%"
          status="available"
        />
        <StatCard 
          title="Avg Fuel Efficiency" 
          value="8.8 km/L" 
          icon="Zap" 
          subtitle="Across all active models"
          status="info"
        />
        <StatCard 
          title="Total ROI Generated" 
          value="2.68%" 
          icon="LineChart" 
          subtitle="Fleet average return"
          status="available"
        />
      </WidgetContainer>

      {/* SVG Chart Placeholders row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-[var(--spacing-section-gap)]">
        <SectionCard title="Utilization Trend (Placeholder)">
          <div className="h-48 w-full bg-bg-cream/40 border border-dashed border-border-light rounded-[var(--radius-input)] flex items-center justify-center text-text-secondary select-none">
            <div className="text-center space-y-2">
              <span className="block text-xs font-bold text-text-primary">📈 SVG Chart Outline Placeholder</span>
              <span className="block text-[10px] text-text-secondary">Visual chart lines will plot live backend metrics here.</span>
            </div>
          </div>
        </SectionCard>
        
        <SectionCard title="Fuel Consumption Trend (Placeholder)">
          <div className="h-48 w-full bg-bg-cream/40 border border-dashed border-border-light rounded-[var(--radius-input)] flex items-center justify-center text-text-secondary select-none">
            <div className="text-center space-y-2">
              <span className="block text-xs font-bold text-text-primary">📊 Bar Chart Outline Placeholder</span>
              <span className="block text-[10px] text-text-secondary">Fuel distribution charts will render here.</span>
            </div>
          </div>
        </SectionCard>
      </div>

      {/* Vehicle performance registry data table */}
      <div className="space-y-4">
        <h3 className="text-xs font-bold text-text-secondary uppercase tracking-wider pl-1 select-none">
          Vehicle Performance Registry
        </h3>
        <DataTable 
          columns={columns} 
          data={roiData} 
          loading={loading}
          emptyMessage="No performance logs available."
        />
      </div>
    </div>
  );
};

export default ReportsAnalytics;
