import React from 'react';
import * as LucideIcons from 'lucide-react';

/**
 * Reusable Dialog modal dialog shell.
 * Renders with a dimmed background overlay and supports custom width parameters.
 */
const Dialog = ({ isOpen, onClose, title, children, maxWidth = 'max-w-lg' }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Dimmed Backdrop */}
      <div 
        className="fixed inset-0 bg-black/30 backdrop-blur-xs transition-opacity" 
        onClick={onClose}
      />

      {/* Modal Box */}
      <div className={`relative w-full ${maxWidth} bg-card-white border border-border-light shadow-md rounded-[var(--radius-card)] overflow-hidden z-10 p-[var(--spacing-card-p)] transition-all`}>
        {/* Modal Header */}
        <div className="flex items-center justify-between pb-4 border-b border-border-light mb-4">
          <h3 className="text-base font-bold text-text-primary">{title || 'Information'}</h3>
          <button 
            onClick={onClose}
            className="p-1.5 rounded-md text-text-secondary hover:text-text-primary hover:bg-bg-cream transition-all cursor-pointer"
            aria-label="Close dialog"
          >
            <LucideIcons.X className="w-4 h-4" />
          </button>
        </div>
        
        {/* Modal Content */}
        <div className="text-sm text-text-secondary">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Dialog;
