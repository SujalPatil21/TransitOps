import React from 'react';
import { Search } from 'lucide-react';
import Input from '../ui/Input';
import { cn } from '../../lib/utils';

/**
 * Reusable SearchBar component.
 * Visual-only text field wrapper mapping search icon decorators.
 */
const SearchBar = ({ value, onChange, placeholder = 'Search...', className, ...props }) => {
  return (
    <div className={cn("relative w-full max-w-sm", className)}>
      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-text-secondary/60">
        <Search className="w-4 h-4" />
      </div>
      <Input
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="pl-10"
        {...props}
      />
    </div>
  );
};

export default SearchBar;
