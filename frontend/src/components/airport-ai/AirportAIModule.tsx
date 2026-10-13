import React, { useState } from 'react';
import { PassengerChat } from './PassengerChat';
import { FlightTrackerCard } from './FlightTrackerCard';
import { FacilityDirectory } from './FacilityDirectory';
import { FaqAccordion } from './FaqAccordion';
import { Plane, Building2, HelpCircle } from 'lucide-react';
import { LiveFlightBoard } from './LiveFlightBoard';

interface AirportAIModuleProps {
  language: string;
}

export const AirportAIModule: React.FC<AirportAIModuleProps> = ({
  language,
}) => {
  const [rightTab, setRightTab] = useState<
    'tracker' | 'directory' | 'faqs'
  >('tracker');

  const tabClass = (tab: typeof rightTab) =>
    `flex items-center gap-2 rounded-lg px-3 py-2 text-xs font-semibold transition-all ${
      rightTab === tab
        ? 'bg-blue-600 text-white shadow-sm'
        : 'text-slate-400 hover:bg-slate-800 hover:text-white'
    }`;

  return (
    <div className="w-full max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

      {/* Module heading */}
      <section className="flex flex-col xl:flex-row xl:items-center xl:justify-between gap-5 rounded-2xl border border-[#1E2E4E] bg-gradient-to-r from-[#121E3B] via-[#0E172E] to-[#142345] p-5 sm:p-6 shadow-lg">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-white">
              TRAIT AirportAI
            </h1>

            <span className="rounded-full border border-cyan-500/40 bg-blue-600/30 px-3 py-1 text-xs font-semibold text-cyan-300">
              Passenger Assistant
            </span>
          </div>

          <p className="mt-2 max-w-3xl text-sm leading-relaxed text-slate-300">
            Airport assistance, provider-supplied live flight information,
            terminal facilities, and passenger FAQs in one place.
          </p>
        </div>

        {/* Tool navigation */}
        <div className="flex w-full flex-wrap items-center gap-1 rounded-xl border border-slate-700/80 bg-[#090F20] p-1 xl:w-auto">
          <button
            onClick={() => setRightTab('tracker')}
            className={tabClass('tracker')}
          >
            <Plane className="h-4 w-4" />
            Flight Information
          </button>

          <button
            onClick={() => setRightTab('directory')}
            className={tabClass('directory')}
          >
            <Building2 className="h-4 w-4" />
            Terminal Directory
          </button>

          <button
            onClick={() => setRightTab('faqs')}
            className={tabClass('faqs')}
          >
            <HelpCircle className="h-4 w-4" />
            Airport FAQs
          </button>
        </div>
      </section>

      {/* Main content */}
      <div className="grid grid-cols-1 items-start gap-6 xl:grid-cols-12">

        {/* Passenger assistant */}
        <section className="min-w-0 xl:col-span-4">
          <PassengerChat language={language} />
        </section>

        {/* Flight board and other airport tools */}
        <section className="min-w-0 space-y-6 xl:col-span-8">
          {rightTab === 'tracker' && (
            <>
              <LiveFlightBoard />
              <FlightTrackerCard language={language} />
            </>
          )}

          {rightTab === 'directory' && <FacilityDirectory />}

          {rightTab === 'faqs' && <FaqAccordion language={language} />}
        </section>
      </div>
    </div>
  );
};

export default AirportAIModule;