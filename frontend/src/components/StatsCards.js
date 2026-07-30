import React from 'react';
import { Scan, TrendingDown, AlertTriangle, Wallet } from 'lucide-react';

export default function StatsCards({ stats }) {
  if (!stats) return null;

  const cards = [
    { label: 'Items Scanned', value: stats.items_scanned, icon: Scan, color: 'text-blue-400' },
    { label: 'Best Deals Found', value: stats.best_deals_found, icon: TrendingDown, color: 'text-green-400' },
    { label: 'Average Risk', value: `${stats.average_risk}%`, icon: AlertTriangle, color: 'text-amber-400' },
    { label: 'Potential Savings', value: `৳${stats.total_potential_savings.toLocaleString()}`, icon: Wallet, color: 'text-emerald-400' },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {cards.map((card) => (
        <div key={card.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-xs uppercase tracking-wider">{card.label}</p>
              <p className="text-2xl font-bold text-white mt-1">{card.value}</p>
            </div>
            <card.icon className={`w-8 h-8 ${card.color} opacity-80`} />
          </div>
        </div>
      ))}
    </div>
  );
}
