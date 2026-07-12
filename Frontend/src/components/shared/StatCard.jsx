import React from 'react';
import Card from '../ui/Card';
import { 
  Truck, CheckCircle, Wrench, Clock, Users, ShieldAlert, 
  FileText, AlertTriangle, IndianRupee, Fuel, Receipt, 
  TrendingUp, Zap, LineChart, AlertCircle, HelpCircle, Navigation 
} from 'lucide-react';
import { cn } from '../../lib/utils';

// Local icon map dictionary to bypass importing the whole lucide library
const iconMap = { 
  Truck, CheckCircle, Wrench, Clock, Users, ShieldAlert, 
  FileText, AlertTriangle, IndianRupee, Fuel, Receipt, 
  TrendingUp, Zap, LineChart, AlertCircle, HelpCircle, Navigation 
};

/**
 * Reusable StatCard (KPI Widget).
 * Renders large bold numbers, titles, custom decorators, and soft left-border colors.
 */
const StatCard = ({ title, value, icon, subtitle, status, className }) => {
  const IconComponent = icon ? iconMap[icon] : null;

  // Left-accent highlight colors based on active statuses
  const getStatusBorder = (statusStr) => {
    if (!statusStr) return "";
    const normalized = statusStr.toLowerCase().replace(/[\s-_]/g, '');
    switch (normalized) {
      case 'available':
      case 'success':
        return "border-l-4 border-l-status-avail-text";
      case 'ontrip':
      case 'info':
        return "border-l-4 border-l-status-trip-text";
      case 'inshop':
      case 'maintenance':
      case 'warning':
        return "border-l-4 border-l-status-maint-text";
      case 'cancelled':
      case 'danger':
        return "border-l-4 border-l-status-cancel-text";
      default:
        return "";
    }
  };

  return (
    <Card className={cn("flex items-start gap-4 p-5 hover:-translate-y-[2px] transition-all-custom", getStatusBorder(status), className)}>
      {IconComponent && (
        <div className="w-10 h-10 rounded-lg bg-bg-cream flex items-center justify-center text-text-secondary shrink-0 select-none">
          <IconComponent className="w-5 h-5 text-text-secondary/80" />
        </div>
      )}
      <div className="min-w-0 flex-1">
        <p className="text-xs font-bold text-text-secondary uppercase tracking-wider select-none">{title}</p>
        <h3 className="text-2xl font-black text-text-primary mt-1.5">{value}</h3>
        {subtitle && <p className="text-[11px] text-text-secondary/80 font-medium mt-1 truncate">{subtitle}</p>}
      </div>
    </Card>
  );
};

export default StatCard;
