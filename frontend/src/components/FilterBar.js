import React from 'react';
import { Filter, Search, SlidersHorizontal } from 'lucide-react';

export default function FilterBar({ filters, setFilters }) {
  const categories = ['', 'Mobile Phones', 'Electronics', 'Laptops & Accessories', 'Home Appliances', 'Gadgets'];
  const platforms = ['', 'daraz', 'pickaboo', 'chaldal', 'ajkerdeal'];
  const sortOptions = [
    { value: 'best_value', label: 'Best Value' },
    { value: 'lowest_price', label: 'Lowest Price' },
    { value: 'lowest_risk', label: 'Lowest Risk' },
    { value: 'biggest_savings', label: 'Biggest Savings' },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 mb-8">
      <div className="flex items-center space-x-2 mb-4">
        <SlidersHorizontal className="w-5 h-5 text-amber-500" />
        <h2 className="text-sm font-semibold text-white">Filters & Sorting</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search products..."
            value={filters.search}
            onChange={(e) => setFilters({ ...filters, search: e.target.value })}
            className="w-full bg-slate-950 border border-slate-700 rounded-lg pl-10 pr-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 transition-colors"
          />
        </div>

        <select
          value={filters.category}
          onChange={(e) => setFilters({ ...filters, category: e.target.value })}
          className="bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-amber-500 transition-colors"
        >
          <option value="">All Categories</option>
          {categories.filter(c => c).map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        <select
          value={filters.platform}
          onChange={(e) => setFilters({ ...filters, platform: e.target.value })}
          className="bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-amber-500 transition-colors"
        >
          <option value="">All Platforms</option>
          {platforms.filter(p => p).map(p => (
            <option key={p} value={p}>{p.charAt(0).toUpperCase() + p.slice(1)}</option>
          ))}
        </select>

        <select
          value={filters.sort}
          onChange={(e) => setFilters({ ...filters, sort: e.target.value })}
          className="bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-amber-500 transition-colors"
        >
          {sortOptions.map(opt => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
      </div>
    </div>
  );
}
