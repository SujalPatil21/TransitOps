import React from 'react';
import Card from '../ui/Card';
import { cn } from '../../lib/utils';

/**
 * Reusable SectionCard component.
 * Builds on top of Card, providing custom headers, titles, and layout slots.
 */
const SectionCard = ({ title, actions, children, className, ...props }) => {
  return (
    <Card className={cn("p-6", className)} {...props}>
      {(title || actions) && (
        <div className="flex items-center justify-between pb-4 border-b border-border-light mb-5 select-none">
          {title && <h3 className="text-sm font-bold text-text-primary uppercase tracking-wider">{title}</h3>}
          {actions && <div className="flex items-center gap-2">{actions}</div>}
        </div>
      )}
      <div className="text-sm text-text-secondary">{children}</div>
    </Card>
  );
};

export default SectionCard;
