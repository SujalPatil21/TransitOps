import React from 'react';
import { cn } from '../../lib/utils';

/**
 * Base Card component representing the master container layout.
 * Styled with Card White, 16px rounded corners, thin light-gray border, and soft drop shadows.
 */
const Card = ({ className, ...props }) => {
  return (
    <div
      className={cn(
        "border border-border-light bg-card-white shadow-soft rounded-[var(--radius-card)] p-[var(--spacing-card-p)]",
        className
      )}
      {...props}
    />
  );
};

export default Card;
