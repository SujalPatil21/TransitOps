import React, { useState, useEffect } from 'react';
import PageHeader from '../../components/shared/PageHeader';
import SearchBar from '../../components/shared/SearchBar';
import DataTable from '../../components/shared/DataTable';
import Button from '../../components/ui/Button';
import Select from '../../components/ui/Select';
import Dialog from '../../components/ui/Dialog';
import Input from '../../components/ui/Input';
import Badge from '../../components/ui/Badge';
import { getMaintenanceLogs } from '../../services/maintenanceService';

/**
 * Maintenance Registry Page.
 * Displays maintenance logs and allows opening Log Maintenance forms.
 */
const Maintenance = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    let active = true;
    getMaintenanceLogs().then((data) => {
      if (active) {
        setLogs(data);
        setLoading(false);
      }
    });
    return () => { active = false; };
  }, []);

  const columns = [
    { header: 'Vehicle Reg', accessor: 'vehicleRegNo' },
    { header: 'Model', accessor: 'vehicleModel' },
    { header: 'Work Description', accessor: 'description' },
    { header: 'Start Date', accessor: 'startDate' },
    { header: 'End Date', accessor: 'endDate' },
    { 
      header: 'Cost', 
      accessor: 'cost', 
      render: (row) => `₹${row.cost.toLocaleString()}` 
    },
    { 
      header: 'Status', 
      accessor: 'status', 
      render: (row) => <Badge status={row.status} /> 
    }
  ];

  // Filtering local execution
  const filteredLogs = logs.filter(log => {
    return log.vehicleRegNo.toLowerCase().includes(searchQuery.toLowerCase()) || 
           log.description.toLowerCase().includes(searchQuery.toLowerCase());
  });

  return (
    <div className="space-y-[var(--spacing-section-gap)]">
      <PageHeader 
        title="Maintenance Logs" 
        subtitle="Schedule active service records, monitor repair charges, and manage vehicle shop times."
        actions={
          <Button onClick={() => setIsModalOpen(true)}>
            + Log Maintenance
          </Button>
        }
      />

      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
        <SearchBar 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search registration no or description..."
        />
      </div>

      {/* Table grid */}
      <DataTable 
        columns={columns} 
        data={filteredLogs} 
        loading={loading}
        emptyMessage="No maintenance logs found."
      />

      {/* Log Maintenance modal dialog */}
      <Dialog 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        title="Log Vehicle Maintenance"
      >
        <div className="space-y-4 pt-2">
          <p className="text-xs text-text-secondary leading-relaxed">
            Record a new active service file. Under business rules, submitting a maintenance record sets the vehicle's status to **In Shop** automatically.
          </p>
          <div>
            <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Select Vehicle</label>
            <Select defaultValue="">
              <option value="" disabled>-- Select Vehicle --</option>
              <option value="1">GJ01AB4521 (VAN-05)</option>
              <option value="2">GJ01AB9981 (TRUCK-11)</option>
            </Select>
          </div>
          <div>
            <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Work Description</label>
            <Input placeholder="e.g. Engine tuning, oil change..." />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Start Date</label>
              <Input type="date" />
            </div>
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Estimated Cost (₹)</label>
              <Input type="number" placeholder="5000" />
            </div>
          </div>
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-border-light">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
            <Button onClick={() => setIsModalOpen(false)}>Log Maintenance</Button>
          </div>
        </div>
      </Dialog>
    </div>
  );
};

export default Maintenance;
