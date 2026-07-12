import React from 'react';

/**
 * Standard loader component.
 * Supports basic circular spinners or paragraph-style skeleton rows.
 */
const Loading = ({ type = 'spinner' }) => {
  if (type === 'skeleton') {
    return (
      <div className="space-y-4 animate-pulse w-full py-4">
        <div className="h-4 bg-gray-200/80 rounded-[4px] w-2/3"></div>
        <div className="h-4 bg-gray-200/80 rounded-[4px] w-full"></div>
        <div className="h-4 bg-gray-200/80 rounded-[4px] w-5/6"></div>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center py-10 w-full" role="status">
      <div className="animate-spin rounded-full h-8 w-8 border-2 border-primary/20 border-t-primary" />
      <span className="sr-only">Loading...</span>
    </div>
  );
};

export default Loading;
