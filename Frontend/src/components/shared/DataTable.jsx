import React from 'react';
import Loading from '../ui/Loading';
import EmptyState from '../ui/EmptyState';
import { cn } from '../../lib/utils';

/**
 * Reusable DataTable component.
 * Supports custom header mappers, cells render overrides, loading status, and empty fallbacks.
 * Wraps content in overflow containers for responsive screens.
 */
const DataTable = ({ 
  columns = [], 
  data = [], 
  loading = false, 
  emptyMessage = 'No records available at the moment.',
  className 
}) => {
  return (
    <div className={cn("w-full overflow-hidden border border-border-light bg-card-white shadow-soft rounded-[var(--radius-card)]", className)}>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-border-light bg-bg-cream/20 text-xs font-bold text-text-secondary select-none">
              {columns.map((col, idx) => (
                <th key={idx} className="px-6 py-4 font-extrabold uppercase tracking-wider">
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={columns.length} className="px-6 py-6">
                  <Loading type="skeleton" />
                </td>
              </tr>
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="px-6 py-8">
                  <EmptyState description={emptyMessage} />
                </td>
              </tr>
            ) : (
              data.map((row, rowIdx) => (
                <tr 
                  key={rowIdx} 
                  className="border-b border-border-light/60 last:border-b-0 hover:bg-bg-cream/10 transition-colors text-sm text-text-primary"
                >
                  {columns.map((col, colIdx) => {
                    const value = row[col.accessor];
                    return (
                      <td key={colIdx} className="px-6 py-4 truncate max-w-xs">
                        {col.render ? col.render(row) : (value !== undefined && value !== null ? String(value) : '—')}
                      </td>
                    );
                  })}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTable;
