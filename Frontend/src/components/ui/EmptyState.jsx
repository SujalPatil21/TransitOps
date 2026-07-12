import React from 'react';
import { Inbox } from 'lucide-react';

/**
 * Reusable Empty State component.
 * Displays a geometric dashed box, a soft color icon, a title, and description prompts.
 */
const EmptyState = ({ 
  icon = 'Inbox', 
  title = 'No items found', 
  description = 'Try adding a new entry or clearing active search filters.' 
}) => {
  // Use Inbox directly for layout
  const IconComponent = Inbox;

  return (
    <div className="flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-border-light rounded-[var(--radius-card)] bg-card-white/50 select-none">
      <div className="w-12 h-12 rounded-full bg-bg-cream flex items-center justify-center text-text-secondary mb-3">
        <IconComponent className="w-5 h-5 text-text-secondary/80" />
      </div>
      <h4 className="text-sm font-bold text-text-primary mb-1">{title}</h4>
      <p className="text-xs text-text-secondary max-w-xs leading-relaxed">{description}</p>
    </div>
  );
};

export default EmptyState;
