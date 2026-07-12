import React from 'react';
import { cn } from '../../lib/utils';

/**
 * Standard text input field.
 * Formatted with 8px borders, 11-unit heights, and custom active focus states.
 */
const Input = React.forwardRef(({ className, type = 'text', ...props }, ref) => {
  return (
    <input
      type={type}
      className={cn(
        "flex h-11 w-full rounded-[var(--radius-input)] border border-border-warm bg-[#FDFCF7] px-3.5 py-2 text-sm text-text-primary placeholder:text-text-secondary/50 focus:outline-none focus:ring-1 focus:ring-primary/25 focus:border-primary disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-150",
        className
      )}
      ref={ref}
      {...props}
    />
  );
});

Input.displayName = 'Input';

export default Input;
