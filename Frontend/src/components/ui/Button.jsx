import React from 'react';
import { cn } from '../../lib/utils';

/**
 * Reusable Button component matching the corporate visual style.
 * Supports primary (filled red), secondary (gray outline), outline (red outline), and ghost options.
 */
const Button = React.forwardRef(({ className, variant = 'primary', size = 'default', ...props }, ref) => {
  return (
    <button
      ref={ref}
      className={cn(
        "inline-flex items-center justify-center font-bold rounded-[var(--radius-input)] text-sm transition-all focus:outline-none focus:ring-2 focus:ring-primary/40 focus:ring-offset-1 disabled:opacity-50 disabled:pointer-events-none cursor-pointer select-none",
        // Variants
        variant === 'primary' && "bg-primary text-card-white hover:bg-secondary shadow-xs",
        variant === 'secondary' && "border border-border-light bg-card-white text-text-primary hover:bg-bg-cream/40",
        variant === 'outline' && "border border-primary text-primary bg-transparent hover:bg-primary/5",
        variant === 'ghost' && "bg-transparent text-text-secondary hover:bg-bg-cream/60 hover:text-text-primary",
        // Sizes
        size === 'default' && "h-11 px-5 py-2.5",
        size === 'sm' && "h-9 px-4 py-1.5 text-xs",
        size === 'lg' && "h-12 px-6 py-3 text-base",
        className
      )}
      {...props}
    />
  );
});

Button.displayName = 'Button';

export default Button;
