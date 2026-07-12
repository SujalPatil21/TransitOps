import React, { useState, useEffect } from 'react';
import PageHeader from '../../components/shared/PageHeader';
import SearchBar from '../../components/shared/SearchBar';
import DataTable from '../../components/shared/DataTable';
import StatCard from '../../components/shared/StatCard';
import WidgetContainer from '../../components/shared/WidgetContainer';
import Button from '../../components/ui/Button';
import Select from '../../components/ui/Select';
import Dialog from '../../components/ui/Dialog';
import Input from '../../components/ui/Input';
import Badge from '../../components/ui/Badge';
import { getExpenses } from '../../services/fuelService';

/**
 * FuelExpense Page.
 * Displays fuel log lists, toll expenses, and operating cost summaries.
 */
const FuelExpense = () => {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    let active = true;
    getExpenses().then((data) => {
      if (active) {
        setExpenses(data);
        setLoading(false);
      }
    });
    return () => { active = false; };
  }, []);

  const columns = [
    { header: 'Vehicle Reg', accessor: 'vehicleRegNo' },
    { header: 'Model', accessor: 'vehicleModel' },
    { 
      header: 'Expense Type', 
      accessor: 'type', 
      render: (row) => <Badge status={row.type === 'Fuel' ? 'ontrip' : 'retired'}>{row.type}</Badge> 
    },
    { 
      header: 'Volume (L)', 
      accessor: 'volume', 
      render: (row) => row.volume > 0 ? `${row.volume} L` : '—' 
    },
    { 
      header: 'Cost', 
      accessor: 'amount', 
      render: (row) => `₹${row.amount.toLocaleString()}` 
    },
    { header: 'Date', accessor: 'date' },
    { header: 'Notes', accessor: 'notes' }
  ];

  // Filtering local execution
  const filteredExpenses = expenses.filter(exp => {
    return exp.vehicleRegNo.toLowerCase().includes(searchQuery.toLowerCase()) || 
           exp.notes.toLowerCase().includes(searchQuery.toLowerCase()) ||
           exp.type.toLowerCase().includes(searchQuery.toLowerCase());
  });

  return (
    <div className="space-y-[var(--spacing-section-gap)]">
      <PageHeader 
        title="Fuel & Expenses" 
        subtitle="Log vehicle fuel additions, tolls, and repair costs to calculate overall fleet operations expenses."
        actions={
          <Button onClick={() => setIsModalOpen(true)}>
            + Log Expense
          </Button>
        }
      />

      {/* KPI summaries row */}
      <WidgetContainer className="mb-6">
        <StatCard 
          title="Total Operating Cost" 
          value="₹30,100" 
          icon="IndianRupee" 
          subtitle="Fuel + Maintenance + Tolls"
          status="info"
        />
        <StatCard 
          title="Fuel Cost Total" 
          value="₹6,650" 
          icon="Fuel" 
          subtitle="Total volume logged: 70 Liters"
          status="warning"
        />
        <StatCard 
          title="Toll & Other Costs" 
          value="₹23,450" 
          icon="Receipt" 
          subtitle="Includes repairs and road taxes"
          status="available"
        />
      </WidgetContainer>

      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
        <SearchBar 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search registration no, type or notes..."
        />
      </div>

      {/* Data Table */}
      <DataTable 
        columns={columns} 
        data={filteredExpenses} 
        loading={loading}
        emptyMessage="No expenses found matching query."
      />

      {/* Add Expense modal dialog */}
      <Dialog 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        title="Log Fleet Expense"
      >
        <div className="space-y-4 pt-2">
          <p className="text-xs text-text-secondary leading-relaxed">
            Record a new expense item. Operating costs are calculated dynamically per vehicle based on fuel and maintenance logs.
          </p>
          <div>
            <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Select Vehicle</label>
            <Select defaultValue="">
              <option value="" disabled>-- Select Vehicle --</option>
              <option value="1">GJ01AB4521 (VAN-05)</option>
              <option value="2">GJ01AB9981 (TRUCK-11)</option>
            </Select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Expense Type</label>
              <Select>
                <option value="Fuel">Fuel</option>
                <option value="Toll">Toll</option>
                <option value="Maintenance">Maintenance</option>
                <option value="Other">Other</option>
              </Select>
            </div>
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Cost (₹)</label>
              <Input type="number" placeholder="1000" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Fuel Volume (Liters)</label>
              <Input type="number" placeholder="e.g. 15 (Optional)" />
            </div>
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Date</label>
              <Input type="date" />
            </div>
          </div>
          <div>
            <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Notes</label>
            <Input placeholder="e.g. Toll booth details or station brand" />
          </div>
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-border-light">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
            <Button onClick={() => setIsModalOpen(false)}>Log Expense</Button>
          </div>
        </div>
      </Dialog>
    </div>
  );
};

export default FuelExpense;
