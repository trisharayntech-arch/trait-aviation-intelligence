import React, { useState, useEffect } from 'react';
import { Plane, BarChart3, RefreshCw, Globe, Clock, ShieldAlert } from 'lucide-react';

interface HeaderProps {
  activeModule: 'airport-ai' | 'analytics';
  setActiveModule: (mod: 'airport-ai' | 'analytics') => void;
  language: string;
  setLanguage: (lang: string) => void;
  onReseed: () => void;
  isReseeding: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  activeModule,
  setActiveModule,
  language,
  setLanguage,
  onReseed,
  isReseeding,
}) => {
  const [time, setTime] = useState<string>('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTime(now.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  const languages = [
    { code: 'en', label: 'English' },
    { code: 'hi', label: 'हिन्दी' },
    { code: 'es', label: 'Español' },
    { code: 'fr', label: 'Français' },
    { code: 'de', label: 'Deutsch' },
    { code: 'ar', label: 'العربية' },
  ];

  return (
    <header className="bg-[#0B132B] border-b border-[#1C2D4A] sticky top-0 z-50 shadow-lg">
      {/* Top Banner: Synthetic Demonstration Warning */}
      <div className="bg-gradient-to-r from-amber-950 via-slate-900 to-amber-950 border-b border-amber-800/40 px-4 py-1.5 flex items-center justify-between text-xs text-amber-300 font-medium tracking-wide">
        <div className="flex items-center space-x-2">
          <ShieldAlert className="w-4 h-4 text-amber-400 animate-pulse" />
          <span className="font-bold tracking-wider">SYNTHETIC DEMONSTRATION DATA</span>
          <span className="hidden md:inline text-amber-400/80">| Generated for TRAIT Innovation prototype & evaluation only</span>
        </div>
        <div className="flex items-center space-x-3 text-slate-400">
          <span className="flex items-center space-x-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span className="text-emerald-400 font-mono text-[11px]">System Online (127.0.0.1:8000)</span>
          </span>
          <span className="font-mono text-slate-300 flex items-center space-x-1">
            <Clock className="w-3.5 h-3.5 text-cyan-400" />
            <span>DEL {time} IST</span>
          </span>
        </div>
      </div>

      {/* Main Navbar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Plane className="w-6 h-6 text-white transform -rotate-45" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xl font-black tracking-tight text-white font-sans">TRAIT</span>
              <span className="text-sm font-semibold text-cyan-400 tracking-wider uppercase bg-cyan-950/80 px-2 py-0.5 rounded border border-cyan-800/60">
                Aviation Intelligence
              </span>
            </div>
            <div className="text-[10px] text-slate-400 tracking-wider uppercase font-semibold">
              TRAIT Innovation • Integrated Airport Systems
            </div>
          </div>
        </div>

        {/* Module Switcher Tabs */}
        <div className="flex items-center bg-[#131F38] p-1 rounded-xl border border-[#22355A]">
          <button
            onClick={() => setActiveModule('airport-ai')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
              activeModule === 'airport-ai'
                ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-md shadow-cyan-500/20'
                : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
            }`}
          >
            <Plane className="w-4 h-4" />
            <span>TRAIT AirportAI</span>
            <span className="text-[10px] bg-black/30 px-1.5 py-0.5 rounded-full font-mono">Passenger</span>
          </button>

          <button
            onClick={() => setActiveModule('analytics')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
              activeModule === 'analytics'
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md shadow-indigo-500/20'
                : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span>TRAIT Aviation Analytics</span>
            <span className="text-[10px] bg-black/30 px-1.5 py-0.5 rounded-full font-mono">Operations</span>
          </button>
        </div>

        {/* Controls: Language & Reseed */}
        <div className="flex items-center space-x-3">
          {/* Language selector */}
          <div className="relative flex items-center bg-[#131F38] border border-[#22355A] rounded-lg px-2 py-1.5 text-xs text-slate-200">
            <Globe className="w-3.5 h-3.5 text-cyan-400 mr-1.5" />
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-transparent text-slate-200 font-medium focus:outline-none cursor-pointer"
            >
              {languages.map((l) => (
                <option key={l.code} value={l.code} className="bg-[#0B132B] text-white">
                  {l.label}
                </option>
              ))}
            </select>
          </div>

          {/* Reseed DB button */}
          <button
            onClick={onReseed}
            disabled={isReseeding}
            title="Reset database with fresh synthetic flight and passenger records"
            className="flex items-center space-x-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white px-3 py-1.5 rounded-lg border border-slate-700 text-xs font-medium transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-cyan-400 ${isReseeding ? 'animate-spin' : ''}`} />
            <span className="hidden sm:inline">{isReseeding ? 'Reseeding...' : 'Reset Data'}</span>
          </button>
        </div>
      </div>
    </header>
  );
};
