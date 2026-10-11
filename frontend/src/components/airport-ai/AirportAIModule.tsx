import React, { useState } from 'react';
import { PassengerChat } from './PassengerChat';
import { FlightTrackerCard } from './FlightTrackerCard';
import { FacilityDirectory } from './FacilityDirectory';
import { FaqAccordion } from './FaqAccordion';
import { Plane, Building2, HelpCircle } from 'lucide-react';

interface AirportAIModuleProps {
  language: string;
}

export const AirportAIModule: React.FC<AirportAIModuleProps> = ({ language }) => {
  const [rightTab, setRightTab] = useState<'tracker' | 'directory' | 'faqs'>('tracker');

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      {/* Module Title Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-[#121E3B] via-[#0E172E] to-[#142345] p-5 rounded-2xl border border-[#1E2E4E] shadow-lg">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl font-black text-white tracking-tight">TRAIT AirportAI</h1>
            <span className="bg-blue-600/30 text-cyan-300 text-xs px-2.5 py-0.5 rounded-full font-semibold border border-cyan-500/40">
              Module 1: Passenger Assistant
            </span>
          </div>
          <p className="text-xs text-slate-300 mt-1 max-w-2xl">
            Zero-API-cost intelligent passenger concierge powered by local SQLite knowledge storage, Scikit-Learn TF-IDF semantic matching, and multilingual flight & gate navigators.
          </p>
        </div>

        {/* Tab Switcher for Right Pane */}
        <div className="flex items-center bg-[#090F20] p-1 rounded-xl border border-slate-700/80 shrink-0">
          <button
            onClick={() => setRightTab('tracker')}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              rightTab === 'tracker'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Plane className="w-3.5 h-3.5" />
            <span>Flight Tracker</span>
          </button>
          <button
            onClick={() => setRightTab('directory')}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              rightTab === 'directory'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Building2 className="w-3.5 h-3.5" />
            <span>Terminal Directory</span>
          </button>
          <button
            onClick={() => setRightTab('faqs')}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              rightTab === 'faqs'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <HelpCircle className="w-3.5 h-3.5" />
            <span>Airport FAQs</span>
          </button>
        </div>
      </div>

      {/* Grid: Chat (Left) + Selected Tool (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7">
          <PassengerChat language={language} />
        </div>
        <div className="lg:col-span-5 space-y-6">
          {rightTab === 'tracker' && <FlightTrackerCard language={language} />}
          {rightTab === 'directory' && <FacilityDirectory />}
          {rightTab === 'faqs' && <FaqAccordion language={language} />}
        </div>
      </div>
    </div>
  );
};
