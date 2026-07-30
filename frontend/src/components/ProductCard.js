import React, { useState } from 'react';
import { ChevronDown, ChevronUp, ExternalLink, Shield, Award, Store, TrendingDown } from 'lucide-react';

const categoryIcons = {
  'Mobile Phones': '📱',
  'Electronics': '🎧',
  'Laptops & Accessories': '💻',
  'Home Appliances': '🏠',
  'Gadgets': '🔋',
};

const platformColors = {
  daraz: 'bg-orange-600',
  pickaboo: 'bg-blue-600',
  chaldal: 'bg-green-600',
  ajkerdeal: 'bg-purple-600',
  facebook: 'bg-indigo-600',
};

const riskColors = {
  green: 'bg-emerald-500',
  yellow: 'bg-yellow-500',
  orange: 'bg-orange-500',
  red: 'bg-red-500',
};

const riskTextColors = {
  green: 'text-emerald-400',
  yellow: 'text-yellow-400',
  orange: 'text-orange-400',
  red: 'text-red-400',
};

export default function ProductCard({ deal }) {
  const [expanded, setExpanded] = useState(false);
  const { product, listings, risk_analysis, best_price, average_price, price_spread, platform_count } = deal;

  const icon = categoryIcons[product.category] || '📦';
  const maxPrice = Math.max(...listings.map(l => l.price));
  const minPrice = Math.min(...listings.map(l => l.price));

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden hover:border-slate-700 transition-colors">
      <div className="p-5">
        <div className="flex flex-col lg:flex-row lg:items-start gap-5">
          <div className="flex-1 min-w-0">
            <div className="flex items-start gap-3">
              <span className="text-3xl">{icon}</span>
              <div>
                <h3 className="text-lg font-semibold text-white leading-tight">{product.name}</h3>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-xs px-2 py-0.5 bg-slate-800 rounded text-slate-400">{product.category}</span>
                  <span className="text-xs px-2 py-0.5 bg-slate-800 rounded text-slate-400">{product.brand}</span>
                  <span className="text-xs text-slate-500">{platform_count} platforms</span>
                </div>
              </div>
            </div>

            <div className="mt-4">
              <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5">
                <span>৳{minPrice.toLocaleString()}</span>
                <span>Price spread: ৳{price_spread.toLocaleString()}</span>
                <span>৳{maxPrice.toLocaleString()}</span>
              </div>
              <div className="h-2.5 bg-slate-800 rounded-full overflow-hidden flex">
                {listings.map((listing, idx) => {
                  const width = ((listing.price - minPrice) / (maxPrice - minPrice || 1)) * 100;
                  const isBest = listing.price === minPrice;
                  return (
                    <div
                      key={idx}
                      className={`h-full ${platformColors[listing.platform] || 'bg-slate-600'} ${isBest ? 'ring-2 ring-white ring-offset-2 ring-offset-slate-900' : ''}`}
                      style={{ width: `${Math.max(width, 5)}%` }}
                      title={`${listing.platform}: ৳${listing.price.toLocaleString()}`}
                    />
                  );
                })}
              </div>
              <div className="flex gap-3 mt-2">
                {Array.from(new Set(listings.map(l => l.platform))).map(p => (
                  <div key={p} className="flex items-center gap-1 text-xs text-slate-400">
                    <div className={`w-2 h-2 rounded-full ${platformColors[p] || 'bg-slate-600'}`} />
                    <span className="capitalize">{p}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="lg:w-64 flex-shrink-0">
            <div className="bg-slate-950 rounded-lg p-4 border border-slate-800">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs text-slate-400 uppercase tracking-wider">Risk Score</span>
                <span className={`text-sm font-bold ${riskTextColors[risk_analysis.color]}`}>
                  {risk_analysis.score}/100
                </span>
              </div>

              <div className="h-3 bg-slate-800 rounded-full overflow-hidden mb-3">
                <div 
                  className={`h-full ${riskColors[risk_analysis.color]} transition-all duration-500`}
                  style={{ width: `${risk_analysis.score}%` }}
                />
              </div>

              <div className={`text-xs font-medium ${riskTextColors[risk_analysis.color]} mb-3`}>
                {risk_analysis.category} — {risk_analysis.recommendation}
              </div>

              {risk_analysis.savings_bdt > 0 && (
                <div className="flex items-center gap-2 text-emerald-400 text-sm mb-3">
                  <TrendingDown className="w-4 h-4" />
                  <span>Save ৳{risk_analysis.savings_bdt.toLocaleString()} ({risk_analysis.savings_percent}%)</span>
                </div>
              )}

              <div className="text-center py-2 border-t border-slate-800">
                <span className="text-xs text-slate-500">Best Price</span>
                <p className="text-2xl font-bold text-white">৳{best_price.toLocaleString()}</p>
                <span className="text-xs text-slate-500">avg: ৳{average_price.toLocaleString()}</span>
              </div>
            </div>
          </div>
        </div>

        <button
          onClick={() => setExpanded(!expanded)}
          className="mt-4 flex items-center gap-1 text-sm text-amber-500 hover:text-amber-400 transition-colors"
        >
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          {expanded ? 'Hide listings' : `View ${listings.length} listings`}
        </button>
      </div>

      {expanded && (
        <div className="border-t border-slate-800 bg-slate-950/50 px-5 py-4">
          <div className="space-y-3">
            {listings.map((listing, idx) => (
              <div key={idx} className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3 bg-slate-900 rounded-lg border border-slate-800">
                <div className="flex items-center gap-3">
                  <div className={`px-2 py-1 rounded text-xs font-medium text-white ${platformColors[listing.platform] || 'bg-slate-600'}`}>
                    {listing.platform}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <Store className="w-3.5 h-3.5 text-slate-400" />
                      <span className="text-sm text-white font-medium">{listing.seller_name}</span>
                      {listing.seller_verified && (
                        <Shield className="w-3.5 h-3.5 text-blue-400" title="Verified" />
                      )}
                    </div>
                    <div className="flex items-center gap-3 mt-0.5 text-xs text-slate-400">
                      {listing.seller_rating && (
                        <span>⭐ {listing.seller_rating} ({listing.seller_reviews} reviews)</span>
                      )}
                      {listing.return_policy && (
                        <span className="flex items-center gap-1">↩ Returns</span>
                      )}
                      {listing.warranty !== 'none' && (
                        <span className="flex items-center gap-1">🏆 {listing.warranty} warranty</span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <p className="text-lg font-bold text-white">৳{listing.price.toLocaleString()}</p>
                    {listing.original_price && (
                      <p className="text-xs text-slate-500 line-through">৳{listing.original_price.toLocaleString()}</p>
                    )}
                  </div>
                  <a
                    href={listing.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1 px-3 py-2 bg-amber-500 hover:bg-amber-600 text-slate-950 text-sm font-medium rounded-lg transition-colors"
                  >
                    <ExternalLink className="w-4 h-4" />
                    Visit
                  </a>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-4 p-3 bg-slate-900 rounded-lg border border-slate-800">
            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Risk Factor Breakdown</h4>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
              {Object.entries(risk_analysis.factors).map(([key, value]) => (
                <div key={key} className="text-center p-2 bg-slate-950 rounded">
                  <p className="text-lg font-bold text-white">{value}</p>
                  <p className="text-[10px] text-slate-500 capitalize">{key.replace('_', ' ')}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
