import React, { useState, useEffect } from 'react';
import PageHeader from '../../components/shared/PageHeader';
import SectionCard from '../../components/shared/SectionCard';
import DataTable from '../../components/shared/DataTable';
import Button from '../../components/ui/Button';
import Input from '../../components/ui/Input';
import Select from '../../components/ui/Select';
import Badge from '../../components/ui/Badge';
import { getTrips } from '../../services/tripService';

/**
 * TripManagement Page.
 * Implements a split dispatcher form and Live Board table registry.
 * Inputs remain placeholders without business checks or dispatch handlers in Phase 1.
 */
const TripManagement = () => {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    getTrips().then((data) => {
      if (active) {
        setTrips(data);
        setLoading(false);
      }
    });
    return () => { active = false; };
  }, []);

  const columns = [
    { header: 'Trip ID', accessor: 'id' },
    { 
      header: 'Vehicle / Driver', 
      accessor: 'vehicle', 
      render: (row) => `${row.vehicle} / ${row.driver}` 
    },
    { 
      header: 'Route', 
      accessor: 'source', 
      render: (row) => `${row.source} ➔ ${row.destination}` 
    },
    { 
      header: 'Status', 
      accessor: 'status', 
      render: (row) => <Badge status={row.status} /> 
    },
    { header: 'ETA / Comment', accessor: 'eta' }
  ];

  return (
    <div className="space-y-[var(--spacing-section-gap)]">
      <PageHeader 
        title="Trip Dispatcher" 
        subtitle="Dispatch cargo routes, check vehicle capacities, enforce driver validation rules, and monitor deliveries."
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-[var(--spacing-section-gap)] items-start">
        
        {/* Create Trip Form Placement (1 Column) */}
        <div className="lg:col-span-1">
          <SectionCard title="Create New Trip">
            <div className="space-y-4 pt-2">
              <p className="text-xs text-text-secondary leading-relaxed">
                Input trip metrics. Business rule parameters (cargo load limitations, active drivers availability) are validated on save.
              </p>
              <div>
                <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Source Depot</label>
                <Input placeholder="e.g. Gandhinagar Depot" />
              </div>
              <div>
                <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Destination Depot</label>
                <Input placeholder="e.g. Ahmedabad Hub" />
              </div>
              <div>
                <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Select Available Vehicle</label>
                <Select defaultValue="">
                  <option value="" disabled>-- Select Vehicle --</option>
                  <option value="1">VAN-05 (Max: 500 kg)</option>
                  <option value="2">TRUCK-11 (Max: 5 Ton)</option>
                </Select>
              </div>
              <div>
                <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Select Available Driver</label>
                <Select defaultValue="">
                  <option value="" disabled>-- Select Driver --</option>
                  <option value="1">Alex (LMV Category · Valid)</option>
                  <option value="4">Suresh (HMV Category · Valid)</option>
                </Select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Cargo Weight (kg)</label>
                  <Input type="number" placeholder="450" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Distance (km)</label>
                  <Input type="number" placeholder="32" />
                </div>
              </div>
              
              {/* Informative rules helper block */}
              <div className="p-3.5 bg-primary/5 border border-primary/20 rounded-[var(--radius-input)] text-xs font-semibold text-primary leading-relaxed">
                ⚠️ Verification checks: Vehicles in maintenance are hidden; cargo weight cannot exceed max load category.
              </div>

              <div className="pt-4 border-t border-border-light flex gap-3">
                <Button variant="secondary" className="flex-1">Clear</Button>
                <Button className="flex-1">Dispatch Run</Button>
              </div>
            </div>
          </SectionCard>
        </div>

        {/* Live Board Grid Placement (2 Columns) */}
        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-xs font-bold text-text-secondary uppercase tracking-wider pl-1 select-none">
            Live Dispatch Board
          </h3>
          <DataTable 
            columns={columns} 
            data={trips} 
            loading={loading}
            emptyMessage="No active trip dispatches."
          />
        </div>
      </div>
    </div>
  );
};

export default TripManagement;
