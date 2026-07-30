import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from './components/Header';
import StatsCards from './components/StatsCards';
import FilterBar from './components/FilterBar';
import ProductCard from './components/ProductCard';
import Footer from './components/Footer';

const API_BASE = process.env.REACT_APP_API_URL || '';

function App() {
  const [deals, setDeals] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: '',
    platform: '',
    sort: 'best_value',
    search: '',
  });

  const fetchDeals = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filters.category) params.append('category', filters.category);
      if (filters.platform) params.append('platform', filters.platform);
      if (filters.sort) params.append('sort', filters.sort);
      if (filters.search) params.append('search', filters.search);

      const res = await axios.get(`${API_BASE}/api/deals?${params}`);
      setDeals(res.data);
    } catch (err) {
      console.error('Failed to fetch deals:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/stats`);
      setStats(res.data);
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    }
  };

  useEffect(() => {
    fetchDeals();
    fetchStats();
  }, [filters]);

  return (
    <div className="min-h-screen bg-slate-950">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <StatsCards stats={stats} />

        <FilterBar filters={filters} setFilters={setFilters} />

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-500"></div>
          </div>
        ) : (
          <div className="space-y-6">
            {deals.length === 0 ? (
              <div className="text-center py-16 text-slate-400">
                <p className="text-xl">No deals found matching your criteria.</p>
                <p className="mt-2">Try adjusting your filters or search query.</p>
              </div>
            ) : (
              deals.map((deal) => (
                <ProductCard key={deal.product.id} deal={deal} />
              ))
            )}
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;
