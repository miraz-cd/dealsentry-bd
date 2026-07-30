import React from 'react';
import { Shield, Search } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-amber-500 p-2 rounded-lg">
              <Shield className="w-6 h-6 text-slate-950" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white tracking-tight">
                DealSentry <span className="text-amber-500">BD</span>
              </h1>
              <p className="text-xs text-slate-400">Bangladesh Marketplace Deal Scanner</p>
            </div>
          </div>

          <div className="hidden md:flex items-center space-x-6 text-sm text-slate-400">
            <span className="flex items-center space-x-1">
              <Search className="w-4 h-4" />
              <span>Scanning Daraz, Pickaboo, Chaldal & more</span>
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
