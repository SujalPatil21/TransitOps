import React from 'react';
import PageHeader from '../../components/shared/PageHeader';
import SectionCard from '../../components/shared/SectionCard';
import Input from '../../components/ui/Input';
import Button from '../../components/ui/Button';

/**
 * Settings Page.
 * Simple placeholder page for organization and RBAC configuration summaries.
 */
const Settings = () => {
  return (
    <div className="space-y-[var(--spacing-section-gap)]">
      <PageHeader 
        title="Settings" 
        subtitle="Manage global system settings, depot locations, and access control profiles."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-[var(--spacing-section-gap)]">
        
        {/* General Configurations */}
        <SectionCard title="General Configuration">
          <div className="space-y-4 pt-2">
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Organization Name</label>
              <Input defaultValue="TransitOps Logistics Ltd." />
            </div>
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Default Weight Unit</label>
              <Input defaultValue="kg / Ton" disabled />
            </div>
            <div>
              <label className="block text-xs font-bold text-text-primary uppercase tracking-wider mb-2">Regional Hub Depot</label>
              <Input defaultValue="Ahmedabad Hub" />
            </div>
            <div className="pt-2">
              <Button onClick={() => alert('Settings saved')}>Save General Settings</Button>
            </div>
          </div>
        </SectionCard>

        {/* RBAC Setup summaries */}
        <SectionCard title="Role Access (RBAC Setup)">
          <div className="space-y-4 pt-2">
            <p className="text-xs text-text-secondary leading-relaxed">
              Security permissions scope configuration summary. Access levels are loaded dynamically from access configurations.
            </p>
            <div className="space-y-2.5 pt-2">
              <div className="flex justify-between items-center text-xs border-b border-border-light/60 pb-2">
                <span className="font-bold text-text-primary">Fleet Manager</span>
                <span className="text-text-secondary">Oversight & Maintenance</span>
              </div>
              <div className="flex justify-between items-center text-xs border-b border-border-light/60 pb-2">
                <span className="font-bold text-text-primary">Dispatcher</span>
                <span className="text-text-secondary">Dashboard, Registry, Drivers, Trips</span>
              </div>
              <div className="flex justify-between items-center text-xs border-b border-border-light/60 pb-2">
                <span className="font-bold text-text-primary">Safety Officer</span>
                <span className="text-text-secondary">Drivers registry & License checks</span>
              </div>
              <div className="flex justify-between items-center text-xs border-b border-border-light/60 pb-2">
                <span className="font-bold text-text-primary">Financial Analyst</span>
                <span className="text-text-secondary">Fuel, Operating costs, Analytics</span>
              </div>
            </div>
          </div>
        </SectionCard>
      </div>
    </div>
  );
};

export default Settings;
