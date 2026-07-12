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
import { getVehicles } from '../../services/vehicleService';

/**
 * VehicleRegistry Page.
 * Renders page toolbar and tables of fleet assets.
 * Actions trigger Add Vehicle dialog wrappers (structural only).
 */
const VehicleRegistry = () => {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('All');
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    let active = true;
    getVehicles().then((data) => {
      if (active) {
        setVehicles(data);
        setLoading(false);
      }
    });
    return () => { active = false; };
  }, []);

  const columns = [
    { header: 'Reg No. (Unique)', accessor: 'regNo' },
    { header: 'Name/Model', accessor: 'model' },
    { header: 'Type', accessor: 'type' },
    { 
      header: 'Max Capacity', 
      accessor: 'capacity', 
      render: (row) => row.capacity >= 1000 ? `${row.capacity / 1000} Ton` : `${row.capacity} kg` 
    },
    { 
      header: 'Odometer', 
      accessor: 'odometer', 
      render: (row) => `${row.odometer.toLocaleString()} km` 
    },
    { 
      header: 'Acq. Cost', 
      accessor: 'cost', 
      render: (row) => `₹${row.cost.toLocaleString()}` 
    },
    { 
      header: 'Status', 
      accessor: 'status', 
      render: (row) => <Badge status={row.status} /> 
    }
  ];

  // Filtering helper (local execution for demo purposes)
  const filteredVehicles = vehicles.filter(v => {
    const matchesSearch = v.regNo.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          v.model.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = typeFilter === 'All' || v.type === typeFilter;
    return matchesSearch && matchesType;
  });

  return (
    <div className="space-y-[var(--spacing-section-gap)]">
      <PageHeader 
        title="Vehicle Registry" 
        subtitle="Maintain fleet models, unique registration keys, cargo load thresholds, and status."
        actions={
          <Button onClick={() => setIsModalOpen(true)}>
            + Add Vehicle
          </Button>
        }
      />

      {/* Toolbar panel */}
      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
        <SearchBar 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search registration no or model..."
        />
        <FilterBar className="sm:w-auto">
          <Select 
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="w-40 h-11"
          >
            <option value="All">All Types</option>
            <option value="Van">Van</option>
            <option value="Truck">Truck</option>
            <option value="Mini">Mini</option>
          </Select>
        </FilterBar>
      </div>

      {/* Vehicle table grid */}
      <DataTable 
        columns={columns} 
        data={filteredVehicles} 
        loading={loading}
        emptyMessage="No vehicles matching search query."
      />

      {/* Add Vehicle Registry modal */}
      <Dialog 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        title="Add Vehicle Registry"
      >
        <div className="space-y-4 pt-2">
          <p className="text-xs text-text-secondary leading-relaxed">
            Submit a new vehicle profile. The system validates unique registration codes dynamically.
          </p>
          <div>
            <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Registration Number</label>
            <Input placeholder="e.g. GJ01AB4521" />
          </div>
          <div>
            <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Vehicle Name/Model</label>
            <Input placeholder="e.g. VAN-05" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Type</label>
              <Select>
                <option value="Van">Van</option>
                <option value="Truck">Truck</option>
                <option value="Mini">Mini</option>
              </Select>
            </div>
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Max Capacity (kg)</label>
              <Input type="number" placeholder="500" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Initial Odometer (km)</label>
              <Input type="number" placeholder="0" />
            </div>
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Acquisition Cost (₹)</label>
              <Input type="number" placeholder="500000" />
            </div>
          </div>
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-border-light">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
            <Button onClick={() => setIsModalOpen(false)}>Save Vehicle</Button>
          </div>
        </div>
      </Dialog>
    </div>
  );
};

export default VehicleRegistry;
