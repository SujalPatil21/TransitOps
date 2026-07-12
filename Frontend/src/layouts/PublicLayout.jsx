import React from 'react';
import { Outlet } from 'react-router-dom';

/**
 * PublicLayout provides the wrapper styling for public screens
 * such as the Landing Page and Login Page.
 */
const PublicLayout = () => {
  return (
    <div className="min-h-screen bg-bg-cream text-text-primary flex flex-col antialiased">
      <Outlet />
    </div>
  );
};

export default PublicLayout;
