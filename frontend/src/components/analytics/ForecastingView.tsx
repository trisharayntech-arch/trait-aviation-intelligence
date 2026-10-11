import React from 'react';
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, Line
} from 'recharts';
import { ForecastData } from '../../types';
import { TrendingUp, AlertCircle, Sparkles, CheckCircle2 } from 'lucide-react';

interface ForecastingViewProps {
  data: ForecastData | null;
  loading: boolean;
}

export const ForecastingView: React.FC<ForecastingViewProps> = ({ data, loading }) => {
  if (loading || !data) {
    return <div className="text-center py-20 text-slate-400 text-xs">Generating time-series forecast...</div>;
  }

  // Pre-process points for seamless multi-line / confidence interval rendering
  const chartPoints = data.points.map((p) => ({
    hour_label: p.hour_label,
    timestamp: p.timestamp,
    historical: p.actual,
    predicted: p.predicted,
    upper_bound: p.upper_bound,
    lower_bound: p.lower_bound,
    type: p.type,
  }));

  return (
    <div className="space-y-6">
      {/* Model Information Banner */}
      <div className="bg-[#121E3B] border border-cyan-800/50 p-4 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-3 shadow-lg">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-blue-950 rounded-xl border border-blue-700/60">
            <TrendingUp className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-white text-sm">{data.model_name}</span>
              <span className="text-[10px] bg-cyan-950 text-cyan-300 border border-cyan-800 px-2 py-0.5 rounded font-mono">
                {data.confidence_level}
              </span>
            </div>
            <div className="text-xs text-slate-400 mt-0.5">
              Projected 24-hour passenger volume based on diurnal bank cycles and historical additive seasonality.
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="bg-[#0B132B] px-3 py-1.5 rounded-lg border border-slate-700">
            <span className="text-slate-400">Peak Projected: </span>
            <span className="font-bold text-cyan-400">
              {data.insights.forecast_peak_hour} ({data.insights.forecast_peak_volume} pax)
            </span>
          </div>
          <div className="bg-[#0B132B] px-3 py-1.5 rounded-lg border border-slate-700">
            <span className="text-slate-400">Trough Projected: </span>
            <span className="font-bold text-slate-300">
              {data.insights.forecast_trough_hour} ({data.insights.forecast_trough_volume} pax)
            </span>
          </div>
        </div>
      </div>

      {/* Main Forecast Chart */}
      <div className="bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-3">
        <div className="flex items-center justify-between pb-2 border-b border-[#1E2E4E]">
          <h3 className="font-bold text-white text-sm">24-Hour Passenger Flow Forecast with Confidence Bounds</h3>
          <span className="text-[10px] text-cyan-400 font-mono">Unit: {data.unit}</span>
        </div>

        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartPoints} margin={{ top: 10, right: 10, left: -20, bottom: 10 }}>
              <defs>
                <linearGradient id="forecastFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="confidenceFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#06B6D4" stopOpacity={0.15} />
                  <stop offset="95%" stopColor="#06B6D4" stopOpacity={0.02} />
                </linearGradient>
              </defs>
              <XAxis dataKey="hour_label" stroke="#64748B" fontSize={10} interval={2} />
              <YAxis stroke="#64748B" fontSize={10} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0B132B', borderColor: '#1E2E4E', borderRadius: '8px', fontSize: '11px' }}
                formatter={(val: any, name: any) => {
                  if (val === null || val === undefined) return ['--', name];
                  const labels: Record<string, string> = {
                    historical: 'Historical Observation',
                    predicted: 'Forecast (Holt-Winters)',
                    upper_bound: 'Upper Bound (95% CI)',
                    lower_bound: 'Lower Bound (95% CI)',
                  };
                  return [`${val} pax/hr`, labels[name] || name];
                }}
              />
              <Legend formatter={(val) => <span className="text-xs text-slate-300">{val}</span>} />

              {/* Confidence Band (Upper and Lower) */}
              <Area type="monotone" dataKey="upper_bound" stroke="#06B6D4" strokeDasharray="3 3" fillOpacity={1} fill="url(#confidenceFill)" name="Upper Bound (95% CI)" />
              <Area type="monotone" dataKey="lower_bound" stroke="#06B6D4" strokeDasharray="3 3" fillOpacity={0} name="Lower Bound (95% CI)" />

              {/* Historical Flow */}
              <Area type="monotone" dataKey="historical" stroke="#10B981" fill="#10B981" fillOpacity={0.15} strokeWidth={2} name="Historical Passenger Flow" />

              {/* Predicted Line */}
              <Area type="monotone" dataKey="predicted" stroke="#A855F7" fillOpacity={1} fill="url(#forecastFill)" strokeWidth={2.5} name="Forecast Projected Flow" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800">
          <div className="flex items-center space-x-4">
            <span className="flex items-center space-x-1.5">
              <span className="w-3 h-0.5 bg-emerald-400"></span>
              <span>Historical 24h</span>
            </span>
            <span className="flex items-center space-x-1.5">
              <span className="w-3 h-0.5 bg-purple-400"></span>
              <span>Projected 24h</span>
            </span>
            <span className="flex items-center space-x-1.5">
              <span className="w-3 h-0.5 bg-cyan-400 border border-dashed"></span>
              <span>95% Confidence Interval</span>
            </span>
          </div>
          <span className="text-slate-500 font-mono text-[11px]">Updated every 60 mins</span>
        </div>
      </div>

      {/* Operational Staffing & Capacity Recommendations */}
      <div className="bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-3">
        <div className="flex items-center space-x-2 pb-2 border-b border-[#1E2E4E]">
          <Sparkles className="w-4 h-4 text-amber-400" />
          <h3 className="font-bold text-white text-sm">Automated Resource & Staffing Advisory</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div className="bg-[#121E3B] p-3 rounded-xl border border-slate-700 space-y-1">
            <span className="text-[10px] text-cyan-400 uppercase font-semibold block">Security Screening</span>
            <p className="text-slate-200">
              {data.insights.recommended_staffing_action}
            </p>
          </div>
          <div className="bg-[#121E3B] p-3 rounded-xl border border-slate-700 space-y-1">
            <span className="text-[10px] text-amber-400 uppercase font-semibold block">Baggage Ground Crews</span>
            <p className="text-slate-200">
              {data.insights.baggage_staffing_action || `Pre-position 3 additional baggage tug teams in Terminal 3 arrivals at ${data.insights.forecast_peak_hour} for peak inbound load.`}
            </p>
          </div>
          <div className="bg-[#121E3B] p-3 rounded-xl border border-slate-700 space-y-1">
            <span className="text-[10px] text-emerald-400 uppercase font-semibold block">Gate Allocation</span>
            <p className="text-slate-200">
              {data.insights.gate_allocation_action || `Predicted volume lull at ${data.insights.forecast_trough_hour} (${data.insights.forecast_trough_volume} pax/hr); schedule heavy aircraft turnaround slots accordingly.`}
            </p>
          </div>

        </div>
      </div>
    </div>
  );
};
