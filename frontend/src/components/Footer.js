import React from 'react';
import { AlertCircle } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-slate-900 border-t border-slate-800 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-amber-500">
            <AlertCircle className="w-5 h-5" />
            <p className="text-sm">
              Risk scores are algorithmic estimates. Always verify sellers independently before purchasing.
            </p>
          </div>
          <p className="text-xs text-slate-500">
            DealSentry BD does not store payment data. Price comparison tool only.
          </p>
        </div>
      </div>
    </footer>
  );
}
