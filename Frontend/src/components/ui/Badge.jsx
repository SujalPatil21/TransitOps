import React from 'react';
import { cn } from '../../lib/utils';

/**
 * Reusable pastel Status Badge component.
 * Maps status properties to soft background and text colors (no highly saturated variables).
 */
const Badge = ({ className, status, children, ...props }) => {
  const getStatusClasses = (statusStr) => {
    if (!statusStr) return "bg-status-retired-bg text-status-retired-text";
    const normalized = statusStr.toLowerCase().replace(/[\s-_]/g, '');
    
    switch (normalized) {
      case 'available':
      case 'active':
        return "bg-status-avail-bg text-status-avail-text";
      case 'ontrip':
      case 'dispatched':
        return "bg-status-trip-bg text-status-trip-text";
      case 'inshop':
      case 'maintenance':
      case 'pending':
      case 'draft':
        return "bg-status-maint-bg text-status-maint-text";
      case 'completed':
        return "bg-status-complete-bg text-status-complete-text";
      case 'cancelled':
      case 'suspended':
        return "bg-status-cancel-bg text-status-cancel-text";
      case 'retired':
      case 'offduty':
        return "bg-status-retired-bg text-status-retired-text";
      default:
        return "bg-status-retired-bg text-status-retired-text";
    }
  };

  const badgeText = children || status;

  return (
    <span
      className={cn(
        "inline-flex items-center px-3 py-1 rounded-[var(--radius-badge)] text-[10px] font-extrabold uppercase tracking-wider select-none",
        getStatusClasses(status),
        className
      )}
      {...props}
    >
      {badgeText}
    </span>
  );
};

export default Badge;
