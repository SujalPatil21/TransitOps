import React from 'react';
import { cn } from '../../lib/utils';

/**
 * Standard select dropdown component.
 * Formatted to match Input heights and active focus ring outline states.
 */
const Select = React.forwardRef(({ className, children, ...props }, ref) => {
  return (
    <select
      className={cn(
        "flex h-11 w-full rounded-[var(--radius-input)] border border-border-warm bg-[#FDFCF7] px-3.5 py-2 text-sm text-text-primary focus:outline-none focus:ring-1 focus:ring-primary/25 focus:border-primary disabled:cursor-not-allowed disabled:opacity-50 cursor-pointer transition-all duration-150",
        className
      )}
      ref={ref}
      {...props}
    >
      {children}
    </select>
  );
});

Select.displayName = 'Select';

export default Select;
