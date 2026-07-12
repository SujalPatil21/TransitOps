import React from 'react';

/**
 * PageHeader provides a unified page title area.
 * Displays titles, secondary subtitles, and maps an optional actions slot for toolbars.
 */
const PageHeader = ({ title, subtitle, actions }) => {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-[var(--spacing-section-gap)] select-none">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-text-primary">{title}</h2>
        {subtitle && <p className="text-sm text-text-secondary mt-1 font-medium">{subtitle}</p>}
      </div>
      
      {actions && (
        <div className="flex items-center gap-2.5 shrink-0">
          {actions}
        </div>
      )}
    </div>
  );
};

export default PageHeader;
