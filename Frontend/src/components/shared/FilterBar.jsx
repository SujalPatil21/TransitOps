import React from 'react';
import { cn } from '../../lib/utils';

/**
 * FilterBar is a visual flex wrapper to format filter dropdowns
 * and filter tags side by side.
 */
const FilterBar = ({ children, className }) => {
  return (
    <div className={cn("flex flex-wrap items-center gap-3 w-full", className)}>
      {children}
    </div>
  );
};

export default FilterBar;
