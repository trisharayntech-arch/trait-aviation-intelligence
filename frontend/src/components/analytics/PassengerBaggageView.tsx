import React from 'react';
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { PassengerBaggageData } from '../../types';
import { Users, Luggage, Clock, CheckCircle2, AlertTriangle } from 'lucide-react';

interface PassengerBaggageViewProps {
  data: PassengerBaggageData | null;
  loading: boolean;
}

export const PassengerBaggageView: React.FC<PassengerBaggageViewProps> = ({ data, loading }) => {
  if (loading || !data) {
    return <div className="text-center py-20 text-slate-400 text-xs">Loading passenger & baggage analytics...</div>;
  }

  const bag = data.baggage_summary;

  return (
    <div className="space-y-6">
      {/* 24-Hour Passenger Throughput Area Chart */}
      <div className="bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-3">
        <div className="flex items-center justify-between pb-2 border-b border-[#1E2E4E]">
          <div className="flex items-center space-x-2">
            <Users className="w-4 h-4 text-cyan-400" />
            <h3 className="font-bold text-white text-sm">Hourly Passenger Throughput & Terminal Load</h3>
          </div>
          <span className="text-[10px] text-slate-400 font-mono">Last 24 Hours Bank Flow</span>
        </div>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data.passenger_trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="paxInbound" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#06B6D4" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#06B6D4" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="paxOutbound" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="hour_label" stroke="#64748B" fontSize={10} />
              <YAxis stroke="#64748B" fontSize={10} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0B132B', borderColor: '#1E2E4E', borderRadius: '8px', fontSize: '11px' }}
                formatter={(val: any, name: any) => [`${val} pax`, name === 'total_inbound' ? 'Inbound' : 'Outbound']}
              />
              <Legend formatter={(val) => <span className="text-xs text-slate-300">{val === 'total_inbound' ? 'Arrival Flow' : 'Departure Flow'}</span>} />
              <Area type="monotone" dataKey="total_inbound" stroke="#06B6D4" fillOpacity={1} fill="url(#paxInbound)" strokeWidth={2} />
              <Area type="monotone" dataKey="total_outbound" stroke="#3B82F6" fillOpacity={1} fill="url(#paxOutbound)" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Baggage Operations Summary & Carousels */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Baggage KPIs */}
        <div className="lg:col-span-4 bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-4">
          <div className="flex items-center space-x-2 pb-2 border-b border-[#1E2E4E]">
            <Luggage className="w-4 h-4 text-purple-400" />
            <h3 className="font-bold text-white text-sm">Baggage Handling SLA Metrics</h3>
          </div>

          <div className="space-y-3">
            <div className="bg-[#121E3B] p-3 rounded-xl border border-slate-700/60 flex items-center justify-between">
              <div>
                <span className="text-[10px] text-slate-400 uppercase font-semibold block">Total Bags Processed</span>
                <span className="text-lg font-black text-white font-mono">{bag.total_bags.toLocaleString()}</span>
              </div>
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            </div>

            <div className="bg-[#121E3B] p-3 rounded-xl border border-slate-700/60 flex items-center justify-between">
              <div>
                <span className="text-[10px] text-slate-400 uppercase font-semibold block">SLA Compliance (&lt;45m)</span>
                <span className="text-lg font-black text-emerald-400 font-mono">{bag.sla_compliance_pct}%</span>
              </div>
              <Clock className="w-5 h-5 text-cyan-400" />
            </div>

            <div className="bg-[#121E3B] p-3 rounded-xl border border-slate-700/60 flex items-center justify-between">
              <div>
                <span className="text-[10px] text-slate-400 uppercase font-semibold block">Average First-Bag Delivery</span>
                <span className="text-lg font-black text-cyan-400 font-mono">{bag.avg_first_bag_mins} mins</span>
              </div>
              <span className="text-[10px] text-slate-400 font-mono">Target: &lt;20m</span>
            </div>

            <div className="bg-[#121E3B] p-3 rounded-xl border border-slate-700/60 flex items-center justify-between">
              <div>
                <span className="text-[10px] text-slate-400 uppercase font-semibold block">Mishandled Bag Rate</span>
                <span className="text-lg font-black text-amber-400 font-mono">{bag.mishandled_rate_per_1000}</span>
              </div>
              <span className="text-[10px] text-slate-400 font-mono">per 1,000 pax</span>
            </div>
          </div>
        </div>

        {/* Carousel Status Cards */}
        <div className="lg:col-span-8 bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-[#1E2E4E]">
            <h3 className="font-bold text-white text-sm">Active Reclaim Carousels Monitor</h3>
            <span className="text-[10px] text-slate-400 font-mono">
              {data.carousel_breakdown.length} Carousels Active
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5 max-h-[290px] overflow-y-auto pr-1">
            {data.carousel_breakdown.map((car) => {
              const isHold = car.status === 'Delayed Hold';
              return (
                <div
                  key={car.carousel_id}
                  className={`p-3 rounded-xl border transition-all ${
                    isHold
                      ? 'bg-rose-950/30 border-rose-800/60'
                      : 'bg-[#121E3B] border-slate-700/70'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="font-black text-white font-mono text-xs">{car.carousel_id}</span>
                    <span className="text-[10px] bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded font-mono">
                      {car.terminal}
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-300 flex items-center justify-between">
                    <span>Flights: {car.flights_handled}</span>
                    <span className="font-mono text-slate-200">{car.total_bags} bags</span>
                  </div>
                  <div className="text-[10px] text-slate-400 flex items-center justify-between mt-1 pt-1 border-t border-slate-800">
                    <span>Avg Dwell: {car.avg_last_bag_mins}m</span>
                    <span
                      className={`font-semibold ${
                        isHold ? 'text-rose-400 animate-pulse' : 'text-emerald-400'
                      }`}
                    >
                      {car.status}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
