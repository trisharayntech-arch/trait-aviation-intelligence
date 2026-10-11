import React, { useState } from 'react';
import { Search, Plane, MapPin, Clock, Luggage, Building, Compass, AlertCircle } from 'lucide-react';
import { FlightGuidance } from '../../types';
import { api } from '../../services/api';

interface FlightTrackerCardProps {
  language: string;
}

export const FlightTrackerCard: React.FC<FlightTrackerCardProps> = ({ language }) => {
  const [flightNumber, setFlightNumber] = useState('AI-204');
  const [loading, setLoading] = useState(false);
  const [guidance, setGuidance] = useState<FlightGuidance | null>(null);
  const [error, setError] = useState<string | null>(null);

  const sampleFlights = ['AI-204', '6E-531', 'BA-142', 'EK-501', 'UK-817', 'LH-760'];

  const handleLookup = async (targetFlight?: string) => {
    const flight = (targetFlight || flightNumber).trim();
    if (!flight) return;
    setLoading(true);
    setError(null);

    try {
      const data = await api.getFlightGuidance(flight, language);
      setGuidance(data.guidance);
    } catch (err: any) {
      setError(`Flight "${flight}" not found in current operational schedule.`);
      setGuidance(null);
    } finally {
      setLoading(false);
    }
  };

  // Perform initial lookup on mount
  React.useEffect(() => {
    handleLookup('AI-204');
  }, [language]);

  return (
    <div className="bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-[#1E2E4E]">
        <div className="flex items-center space-x-2.5">
          <Plane className="w-5 h-5 text-cyan-400" />
          <h3 className="font-bold text-white text-base">Direct Flight Guidance</h3>
        </div>
        <span className="text-[11px] font-mono bg-cyan-950/80 text-cyan-300 border border-cyan-800/60 px-2 py-0.5 rounded">
          Gate & Carousel
        </span>
      </div>

      {/* Flight Search Input */}
      <div className="space-y-2">
        <div className="flex items-center space-x-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input
              type="text"
              value={flightNumber}
              onChange={(e) => setFlightNumber(e.target.value.toUpperCase())}
              placeholder="e.g. AI-204, 6E-531, BA-142"
              className="w-full bg-[#121E3B] text-slate-100 placeholder-slate-500 text-sm pl-9 pr-3 py-2.5 rounded-xl border border-slate-700 focus:outline-none focus:border-cyan-500 font-mono"
            />
          </div>
          <button
            onClick={() => handleLookup()}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2.5 rounded-xl text-sm font-semibold transition-colors disabled:opacity-50"
          >
            {loading ? 'Searching...' : 'Track'}
          </button>
        </div>

        {/* Sample flight pills */}
        <div className="flex items-center space-x-1.5 overflow-x-auto text-[11px] text-slate-400">
          <span className="shrink-0">Quick Select:</span>
          {sampleFlights.map((f) => (
            <button
              key={f}
              onClick={() => {
                setFlightNumber(f);
                handleLookup(f);
              }}
              className="px-2 py-0.5 bg-[#14203D] hover:bg-[#1E2E54] text-slate-300 rounded font-mono border border-slate-700/60 transition-colors"
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="p-3 bg-rose-950/40 border border-rose-800/50 rounded-xl text-xs text-rose-300 flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Guidance Result Card */}
      {guidance && (
        <div className="space-y-3 pt-1">
          <div className="bg-[#121E3B] p-4 rounded-xl border border-[#22355A] space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-xl font-black text-white font-mono">{guidance.flight_number}</span>
                <span className="text-xs text-slate-400 block">{guidance.airline}</span>
              </div>
              <div className="text-right">
                <span
                  className={`inline-block px-2.5 py-1 rounded text-xs font-bold border ${
                    guidance.status === 'On-Time'
                      ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                      : guidance.status === 'Delayed'
                      ? 'bg-rose-500/20 text-rose-400 border-rose-500/30'
                      : 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30'
                  }`}
                >
                  {guidance.status}
                </span>
                {guidance.delay_minutes > 0 && (
                  <div className="text-[10px] text-rose-400 font-semibold mt-0.5">
                    +{guidance.delay_minutes} min ({guidance.delay_reason})
                  </div>
                )}
              </div>
            </div>

            {/* Matrix */}
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-[#0A1224] p-2.5 rounded-lg border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center space-x-1">
                  <Building className="w-3 h-3 text-cyan-400" />
                  <span>Terminal</span>
                </div>
                <div className="text-sm font-bold text-white mt-0.5">{guidance.terminal}</div>
              </div>
              <div className="bg-[#0A1224] p-2.5 rounded-lg border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center space-x-1">
                  <MapPin className="w-3 h-3 text-emerald-400" />
                  <span>Departure Gate</span>
                </div>
                <div className="text-sm font-bold text-cyan-300 mt-0.5">{guidance.gate}</div>
              </div>
              <div className="bg-[#0A1224] p-2.5 rounded-lg border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center space-x-1">
                  <Clock className="w-3 h-3 text-amber-400" />
                  <span>Check-In Counters</span>
                </div>
                <div className="text-xs font-medium text-slate-200 mt-1 truncate">{guidance.checkin_desks}</div>
              </div>
              <div className="bg-[#0A1224] p-2.5 rounded-lg border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center space-x-1">
                  <Luggage className="w-3 h-3 text-purple-400" />
                  <span>Arrival Carousel</span>
                </div>
                <div className="text-xs font-bold text-purple-300 mt-1">{guidance.baggage_carousel}</div>
              </div>
            </div>
          </div>

          {/* Turn-by-turn Navigation */}
          <div className="bg-[#121E3B] p-4 rounded-xl border border-[#22355A] space-y-2.5">
            <div className="text-xs font-bold text-cyan-300 uppercase tracking-wider flex items-center space-x-1.5">
              <Compass className="w-3.5 h-3.5" />
              <span>Step-by-Step Gate Guidance</span>
            </div>
            <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
              {guidance.navigation_steps.map((st) => (
                <div key={st.step_number} className="flex items-start space-x-2 text-xs bg-[#090F20] p-2 rounded-lg">
                  <span className="w-4 h-4 rounded-full bg-cyan-950 text-cyan-400 font-mono text-[10px] font-bold flex items-center justify-center shrink-0 border border-cyan-800">
                    {st.step_number}
                  </span>
                  <div className="flex-1">
                    <p className="text-slate-200 leading-snug">{st.instruction}</p>
                    <div className="text-[10px] text-slate-400 mt-0.5">
                      ~{st.estimated_minutes} min ({st.distance_meters}m) {st.landmark ? `• ${st.landmark}` : ''}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
