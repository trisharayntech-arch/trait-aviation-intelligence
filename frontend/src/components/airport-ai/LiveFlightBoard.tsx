import React, { useCallback, useEffect, useState } from 'react';
import {
  PlaneTakeoff,
  PlaneLanding,
  RefreshCw,
  Clock,
  MapPin,
  AlertCircle,
} from 'lucide-react';

type FlightRecord = {
  number?: string;
  status?: string;
  airline?: {
    name?: string;
  };
  departure?: {
  airport?: {
    name?: string;
    iata?: string;
  };
  scheduledTime?: {
    local?: string;
    utc?: string;
  };
    revisedTime?: {
      local?: string;
      utc?: string;
    };
    terminal?: string;
    gate?: string;
    checkInDesk?: string;
  };
  arrival?: {
    airport?: {
      name?: string;
      iata?: string;
    };
    scheduledTime?: {
      local?: string;
      utc?: string;
    };
    revisedTime?: {
      local?: string;
      utc?: string;
    };
    terminal?: string;
    baggageBelt?: string;
  };
};

type FlightResponse = {
  airport: string;
  flight_type: string;
  count: number;
  flights: FlightRecord[];
  data_source: string;
};

const API_BASE = (
  import.meta.env.VITE_API_BASE_URL || ''
).replace(/\/$/, '');

const formatTime = (value?: string) => {
  if (!value) return 'Not available';

  const match = value.match(/\d{4}-\d{2}-\d{2} (\d{2}:\d{2})/);
  return match ? match[1] : value;
};

export const LiveFlightBoard: React.FC = () => {
  const [flightType, setFlightType] = useState<
    'arrivals' | 'departures'
  >('departures');

  const [airport, setAirport] = useState('BLR');
  const [result, setResult] = useState<FlightResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  const loadFlights = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const query = new URLSearchParams({
        flight_type: flightType,
        duration_minutes: '360',
      });

      const response = await fetch(
        `${API_BASE}/api/airport-ai/live-flights/${airport}?${query}`,
      );

      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(
          body.detail || `Flight request failed (${response.status})`,
        );
      }

      const data: FlightResponse = await response.json();

      setResult(data);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to retrieve flight information.',
      );
      setResult(null);
    } finally {
      setLoading(false);
    }
  }, [airport, flightType]);

  useEffect(() => {
    void loadFlights();
  }, [loadFlights]);

  useEffect(() => {
    const timer = window.setInterval(() => {
      void loadFlights();
    }, 120000);

    return () => window.clearInterval(timer);
  }, [loadFlights]);

  return (
    <section className="rounded-2xl border border-[#1E2E4E] bg-[#0B132B] p-4 sm:p-5 space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-bold text-white">
            Live Flight Board
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Provider-supplied flight information
          </p>
        </div>

        <button
          onClick={() => void loadFlights()}
          disabled={loading}
          className="inline-flex items-center gap-2 rounded-lg border border-slate-700 px-3 py-2 text-xs text-cyan-300 hover:bg-slate-800 disabled:opacity-50"
        >
          <RefreshCw
            className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`}
          />
          Refresh
        </button>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <label className="text-xs text-slate-400">
          Airport
          <select
            value={airport}
            onChange={(event) => setAirport(event.target.value)}
            className="ml-2 rounded-lg border border-slate-700 bg-[#070D1E] px-3 py-2 text-sm text-white"
          >
            <option value="BLR">Bengaluru (BLR)</option>
            <option value="DEL">Delhi (DEL)</option>
            <option value="BOM">Mumbai (BOM)</option>
            <option value="HYD">Hyderabad (HYD)</option>
            <option value="MAA">Chennai (MAA)</option>
          </select>
        </label>

        <div className="flex rounded-lg border border-slate-700 p-1">
          <button
            onClick={() => setFlightType('departures')}
            className={`flex items-center gap-2 rounded-md px-3 py-2 text-xs ${
              flightType === 'departures'
                ? 'bg-blue-600 text-white'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <PlaneTakeoff className="h-4 w-4" />
            Departures
          </button>

          <button
            onClick={() => setFlightType('arrivals')}
            className={`flex items-center gap-2 rounded-md px-3 py-2 text-xs ${
              flightType === 'arrivals'
                ? 'bg-blue-600 text-white'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <PlaneLanding className="h-4 w-4" />
            Arrivals
          </button>
        </div>
      </div>

      {lastUpdated && (
        <p className="text-xs text-slate-500">
          <Clock className="inline h-3.5 w-3.5 mr-1" />
          Last updated: {lastUpdated}
        </p>
      )}

      {error && (
        <div className="flex gap-2 rounded-xl border border-rose-800/60 bg-rose-950/30 p-3 text-sm text-rose-300">
          <AlertCircle className="h-5 w-5 shrink-0" />
          <div>
            <p className="font-semibold">Unable to load flights</p>
            <p className="mt-1 break-words">{error}</p>
          </div>
        </div>
      )}

      {loading && !result && (
        <p className="py-8 text-center text-sm text-slate-400">
          Loading flight information...
        </p>
      )}

      {!loading && !error && result?.count === 0 && (
        <p className="py-8 text-center text-sm text-slate-400">
          No flights were returned for this airport and time window.
        </p>
      )}

      {result && result.flights.length > 0 && (
        <>
          <div className="flex flex-wrap items-center justify-between gap-2">
            <p className="text-sm text-white">
              <span className="text-2xl font-black text-cyan-300">
                {result.count}
              </span>{' '}
              flights returned
            </p>
            <span className="rounded-full border border-emerald-700/50 bg-emerald-950/30 px-3 py-1 text-xs text-emerald-300">
              Source: {result.data_source}
            </span>
          </div>

          <div className="space-y-3">
            {result.flights.map((flight, index) => {
              const time =
                flightType === 'departures'
                  ? flight.departure?.revisedTime?.local ||
                    flight.departure?.scheduledTime?.local
                  : flight.arrival?.revisedTime?.local ||
                    flight.arrival?.scheduledTime?.local;

              const location =
                flightType === 'departures'
                  ? flight.arrival?.airport?.name ||
                    flight.arrival?.airport?.iata
                  : flight.departure?.airport?.name ||
                    flight.departure?.airport?.iata;

              const terminal =
                flightType === 'departures'
                  ? flight.departure?.terminal
                  : flight.arrival?.terminal;

              const gate = flight.departure?.gate;

              return (
                <article
                  key={`${flight.number || 'flight'}-${index}`}
                  className="rounded-xl border border-[#223454] bg-[#101B34] p-4"
                >
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <p className="font-bold text-white">
                        {flight.number || 'Flight number unavailable'}
                      </p>
                      <p className="mt-1 text-sm text-slate-300">
                        {flight.airline?.name || 'Airline unavailable'}
                      </p>
                    </div>

                    <span className="rounded-full bg-blue-950/60 px-3 py-1 text-xs text-cyan-300">
                      {flight.status || 'Status unavailable'}
                    </span>
                  </div>

                  <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-xs text-slate-500">
                        {flightType === 'departures'
                          ? 'Destination'
                          : 'Origin'}
                      </p>
                      <p className="mt-1 flex items-center gap-1 text-slate-200">
                        <MapPin className="h-3.5 w-3.5 text-cyan-400" />
                        {location || 'Not available'}
                      </p>
                    </div>

                    <div>
                      <p className="text-xs text-slate-500">
                        {flightType === 'departures'
                          ? 'Departure time'
                          : 'Arrival time'}
                      </p>
                      <p className="mt-1 font-semibold text-white">
                        {formatTime(time)}
                      </p>
                    </div>

                    <div>
                      <p className="text-xs text-slate-500">Terminal</p>
                      <p className="mt-1 text-slate-200">
                        {terminal || 'Not provided'}
                      </p>
                    </div>

                    <div>
                      <p className="text-xs text-slate-500">
                        {flightType === 'departures'
                          ? 'Gate'
                          : 'Baggage belt'}
                      </p>
                      <p className="mt-1 text-slate-200">
                        {flightType === 'departures'
                          ? gate || 'Not provided'
                          : flight.arrival?.baggageBelt || 'Not provided'}
                      </p>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        </>
      )}

      <p className="border-t border-slate-800 pt-3 text-[11px] leading-relaxed text-amber-300/80">
        Flight information is supplied by an external provider and may be
        incomplete or delayed. Verify important travel details with the airline
        or airport. Provider usage limits and licensing apply.
      </p>
    </section>
  );
};