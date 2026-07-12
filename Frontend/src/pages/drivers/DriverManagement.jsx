import React, { useState, useEffect } from 'react';
import PageHeader from '../../components/shared/PageHeader';
import SearchBar from '../../components/shared/SearchBar';
import FilterBar from '../../components/shared/FilterBar';
import DataTable from '../../components/shared/DataTable';
import Button from '../../components/ui/Button';
import Select from '../../components/ui/Select';
import Dialog from '../../components/ui/Dialog';
import Input from '../../components/ui/Input';
import Badge from '../../components/ui/Badge';
import { getDrivers } from '../../services/driverService';

/**
 * DriverManagement Page.
 * Displays driver registries, license category descriptors, and compliance warning flags.
 */
const DriverManagement = () => {
  const [drivers, setDrivers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('All');
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    let active = true;
    getDrivers().then((data) => {
      if (active) {
        setDrivers(data);
        setLoading(false);
      }
    });
    return () => { active = false; };
  }, []);

  const isExpired = (dateStr) => {
    const today = new Date();
    const expiry = new Date(dateStr);
    return expiry < today;
  };

  const columns = [
    { header: 'Driver Name', accessor: 'name' },
    { header: 'License No.', accessor: 'licenseNo' },
    { header: 'Category', accessor: 'category' },
    { 
      header: 'Expiry Date', 
      accessor: 'expiryDate',
      render: (row) => {
        const expired = isExpired(row.expiryDate);
        return (
          <div className="flex items-center gap-2">
            <span>{row.expiryDate}</span>
            {expired && (
              <span className="text-[9px] font-extrabold text-primary bg-primary/10 px-1.5 py-0.5 rounded-xs uppercase tracking-wider">
                Expired
              </span>
            )}
          </div>
        );
      }
    },
    { header: 'Contact', accessor: 'contact' },
    { 
      header: 'Safety Score', 
      accessor: 'safetyScore', 
      render: (row) => (
        <span className={`font-bold ${row.safetyScore >= 90 ? 'text-status-avail-text' : 'text-text-primary'}`}>
          {row.safetyScore}/100
        </span>
      )
    },
    { header: 'Status', accessor: 'status', render: (row) => <Badge status={row.status} /> }
  ];

  // Filtering local execution
  const filteredDrivers = drivers.filter(d => {
    const matchesSearch = d.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          d.licenseNo.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'All' || d.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const hasExpiredLicense = drivers.some(d => isExpired(d.expiryDate));

  return (
    <div className="space-y-[var(--spacing-section-gap)]">
      <PageHeader 
        title="Driver Management" 
        subtitle="Manage active operators, driving license categories, safety ratings, and duty statuses."
        actions={
          <Button onClick={() => setIsModalOpen(true)}>
            + Add Driver
          </Button>
        }
      />

      {/* Warning banner */}
      {hasExpiredLicense && (
        <div className="p-4 bg-primary/5 border border-primary/20 rounded-[var(--radius-card)] flex items-center justify-between text-xs select-none">
          <div className="flex items-center gap-3 text-primary font-bold">
            <span>⚠️ Compliance Alert: Drivers with expired licenses must be suspended and cannot be dispatched to trips.</span>
          </div>
        </div>
      )}

      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
        <SearchBar 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search driver name or license no..."
        />
        <FilterBar className="sm:w-auto">
          <Select 
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="w-40 h-11"
          >
            <option value="All">All Statuses</option>
            <option value="Available">Available</option>
            <option value="On Trip">On Trip</option>
            <option value="Off Duty">Off Duty</option>
            <option value="Suspended">Suspended</option>
          </Select>
        </FilterBar>
      </div>

      {/* Table grid */}
      <DataTable 
        columns={columns} 
        data={filteredDrivers} 
        loading={loading}
        emptyMessage="No drivers matching search query."
      />

      {/* Add Driver modal */}
      <Dialog 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        title="Add Driver Registry"
      >
        <div className="space-y-4 pt-2">
          <p className="text-xs text-text-secondary leading-relaxed">
            Create a new driver profile. The system locks scheduling if licenses are expired or status is Suspended.
          </p>
          <div>
            <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Driver Name</label>
            <Input placeholder="e.g. Alex" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">License Number</label>
              <Input placeholder="e.g. DL-88213" />
            </div>
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">License Category</label>
              <Select>
                <option value="LMV">LMV (Light Motor Vehicle)</option>
                <option value="HMV">HMV (Heavy Motor Vehicle)</option>
              </Select>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">License Expiry</label>
              <Input type="date" />
            </div>
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Contact Number</label>
              <Input placeholder="e.g. 9876500123" />
            </div>
          </div>
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-border-light">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
            <Button onClick={() => setIsModalOpen(false)}>Save Driver</Button>
          </div>
        </div>
      </Dialog>
    </div>
  );
};

export default DriverManagement;
