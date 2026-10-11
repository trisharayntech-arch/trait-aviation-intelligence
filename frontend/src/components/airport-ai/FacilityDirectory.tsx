import React, { useState, useEffect } from 'react';
import { Building2, Search, MapPin, Clock, Accessibility, Coffee, ShieldCheck, Armchair, HelpCircle } from 'lucide-react';
import { Facility } from '../../types';
import { api } from '../../services/api';

export const FacilityDirectory: React.FC = () => {
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTerminal, setSelectedTerminal] = useState<string>('ALL');
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  const terminals = ['ALL', 'T1', 'T2', 'T3'];
  const categories = [
    'ALL', 'Gate', 'Lounge', 'Security', 'Baggage', 'CheckIn', 'Food', 'Medical', 'Restroom', 'Transit'
  ];

  useEffect(() => {
    const fetchFacilities = async () => {
      setLoading(true);
      try {
        const term = selectedTerminal === 'ALL' ? undefined : selectedTerminal;
        const cat = selectedCategory === 'ALL' ? undefined : selectedCategory;
        const data = await api.getFacilities(term, cat);
        setFacilities(data.facilities);
      } catch (err) {
        console.error('Failed to load facilities', err);
      } finally {
        setLoading(false);
      }
    };
    fetchFacilities();
  }, [selectedTerminal, selectedCategory]);

  const filteredFacilities = facilities.filter((f) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      f.name.toLowerCase().includes(q) ||
      f.location_desc.toLowerCase().includes(q) ||
      (f.amenities && f.amenities.toLowerCase().includes(q))
    );
  });

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'Lounge': return <Armchair className="w-4 h-4 text-amber-400" />;
      case 'Food': return <Coffee className="w-4 h-4 text-orange-400" />;
      case 'Security': return <ShieldCheck className="w-4 h-4 text-emerald-400" />;
      default: return <Building2 className="w-4 h-4 text-cyan-400" />;
    }
  };

  return (
    <div className="bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-[#1E2E4E]">
        <div className="flex items-center space-x-2.5">
          <Building2 className="w-5 h-5 text-cyan-400" />
          <h3 className="font-bold text-white text-base">Terminal & Facility Directory</h3>
        </div>
        <span className="text-xs text-slate-400 font-mono">
          {filteredFacilities.length} Facilities Listed
        </span>
      </div>

      {/* Filter Bars */}
      <div className="space-y-3">
        {/* Search */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by facility name, lounge, food, or amenities..."
            className="w-full bg-[#121E3B] text-slate-100 placeholder-slate-500 text-xs pl-9 pr-3 py-2.5 rounded-xl border border-slate-700 focus:outline-none focus:border-cyan-500"
          />
        </div>

        {/* Terminal pills */}
        <div className="flex items-center space-x-2 overflow-x-auto text-xs">
          <span className="text-slate-400 font-semibold shrink-0">Terminal:</span>
          {terminals.map((t) => (
            <button
              key={t}
              onClick={() => setSelectedTerminal(t)}
              className={`px-3 py-1 rounded-lg font-semibold transition-all shrink-0 ${
                selectedTerminal === t
                  ? 'bg-cyan-600 text-white shadow-sm'
                  : 'bg-[#14203D] text-slate-300 hover:bg-[#1C2C50]'
              }`}
            >
              {t === 'ALL' ? 'All Terminals' : t}
            </button>
          ))}
        </div>

        {/* Category tags */}
        <div className="flex items-center space-x-1.5 overflow-x-auto text-[11px] no-scrollbar">
          {categories.map((c) => (
            <button
              key={c}
              onClick={() => setSelectedCategory(c)}
              className={`px-2 py-0.5 rounded-md font-medium transition-all shrink-0 ${
                selectedCategory === c
                  ? 'bg-slate-200 text-slate-900 font-bold'
                  : 'bg-[#121E3A] text-slate-400 hover:text-slate-200'
              }`}
            >
              {c}
            </button>
          ))}
        </div>
      </div>

      {/* Facilities List Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-[380px] overflow-y-auto pr-1">
        {loading ? (
          <div className="col-span-2 text-center py-10 text-slate-400 text-xs">Loading facilities...</div>
        ) : filteredFacilities.length === 0 ? (
          <div className="col-span-2 text-center py-10 text-slate-400 text-xs">
            No airport facilities matched your search criteria.
          </div>
        ) : (
          filteredFacilities.map((fac) => (
            <div
              key={fac.id}
              className="bg-[#121E3B] border border-[#22355A] hover:border-cyan-600/50 p-3 rounded-xl space-y-2 transition-all shadow-sm"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-2">
                  <div className="p-1.5 rounded-lg bg-[#0B132B] border border-slate-700/60">
                    {getCategoryIcon(fac.category)}
                  </div>
                  <div>
                    <h4 className="font-bold text-white text-xs leading-tight">{fac.name}</h4>
                    <span className="text-[10px] text-cyan-400 font-medium">{fac.category}</span>
                  </div>
                </div>
                <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono font-bold">
                  {fac.terminal}
                </span>
              </div>

              <div className="text-[11px] text-slate-300 flex items-start space-x-1.5">
                <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5" />
                <span>{fac.location_desc} ({fac.level})</span>
              </div>

              {fac.amenities && (
                <div className="text-[10px] text-slate-400 bg-[#090F20] p-1.5 rounded border border-slate-800/80">
                  <span className="text-slate-300 font-medium">Features: </span>
                  {fac.amenities}
                </div>
              )}

              <div className="flex items-center justify-between text-[10px] text-slate-400 pt-1 border-t border-slate-800">
                <span className="flex items-center space-x-1">
                  <Clock className="w-3 h-3 text-cyan-400" />
                  <span>{fac.opening_hours}</span>
                </span>
                <span className="flex items-center space-x-1 text-slate-300">
                  <span>~{fac.walking_time_mins} min walk</span>
                  {fac.wheelchair_accessible && (
                    <span title="Wheelchair Accessible">
                      <Accessibility className="w-3.5 h-3.5 text-emerald-400 ml-1" />
                    </span>
                  )}

                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
