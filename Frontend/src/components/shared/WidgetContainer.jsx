import React from 'react';
import { cn } from '../../lib/utils';

/**
 * Reusable WidgetContainer layout.
 * Formats lists of widgets or KPI blocks into responsive grids.
 */
const WidgetContainer = ({ children, className }) => {
  return (
    <div className={cn("grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-[var(--spacing-section-gap)] w-full", className)}>
      {children}
    </div>
  );
};

export default WidgetContainer;
