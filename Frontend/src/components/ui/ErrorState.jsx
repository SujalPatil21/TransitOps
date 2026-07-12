import React from 'react';
import { AlertCircle } from 'lucide-react';
import Button from './Button';

/**
 * Reusable Error State component.
 * Displays warning cards with retry actions for handling operations failures.
 */
const ErrorState = ({ 
  title = 'Connection error', 
  message = 'Failed to load details. Please verify your connection and try again.', 
  onRetry 
}) => {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8 border border-primary/10 rounded-[var(--radius-card)] bg-primary/5 select-none">
      <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center text-primary mb-3">
        <AlertCircle className="w-5 h-5" />
      </div>
      <h4 className="text-sm font-bold text-text-primary mb-1">{title}</h4>
      <p className="text-xs text-text-secondary max-w-xs leading-relaxed mb-4">{message}</p>
      
      {onRetry && (
        <Button variant="secondary" size="sm" onClick={onRetry}>
          Try Again
        </Button>
      )}
    </div>
  );
};

export default ErrorState;
