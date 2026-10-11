import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie, Legend
} from 'recharts';
import { DelayAnalysisData } from '../../types';
import { AlertCircle, Plane, Award } from 'lucide-react';

interface DelayAnalysisViewProps {
  data: DelayAnalysisData | null;
  loading: boolean;
}

export const DelayAnalysisView: React.FC<DelayAnalysisViewProps> = ({ data, loading }) => {
  if (loading || !data) {
    return <div className="text-center py-20 text-slate-400 text-xs">Loading flight delay analysis...</div>;
  }

  const causeColors: Record<string, string> = {
    'Carrier': '#3B82F6',
    'Weather': '#06B6D4',
    'NAS/ATC': '#8B5CF6',
    'Late Aircraft': '#F59E0B',
    'Security': '#EF4444'
  };

  const pieData = data.causality_breakdown.map((c) => ({
    name: c.cause,
    value: c.flight_count,
    percentage: c.percentage,
  }));

  return (
    <div className="space-y-6">
      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Causality Breakdown (Pie Chart) */}
        <div className="lg:col-span-5 bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-[#1E2E4E]">
            <h3 className="font-bold text-white text-sm">Delay Causality Breakdown</h3>
            <span className="text-[10px] text-slate-400 font-mono">
              {data.summary.delayed_flights} delayed flights
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={85}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={causeColors[entry.name] || '#64748B'} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#0B132B', borderColor: '#1E2E4E', borderRadius: '8px', fontSize: '11px' }}
                  formatter={(val: any, name: any, item: any) => [`${val} flights (${item.payload.percentage}%)`, name]}
                />
                <Legend
                  formatter={(value) => <span className="text-xs text-slate-300">{value}</span>}
                  layout="horizontal"
                  verticalAlign="bottom"
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-2 gap-2 text-[11px] pt-2 border-t border-slate-800">
            {data.causality_breakdown.map((c) => (
              <div key={c.cause} className="flex items-center justify-between bg-[#131F38] px-2.5 py-1.5 rounded-lg">
                <span className="text-slate-300 font-medium">{c.cause}:</span>
                <span className="font-mono font-bold text-cyan-400">{c.percentage}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Delay Duration Histogram (Bar Chart) */}
        <div className="lg:col-span-7 bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-[#1E2E4E]">
            <h3 className="font-bold text-white text-sm">Delay Duration Distribution</h3>
            <span className="text-[10px] text-cyan-400 font-mono">
              Avg Delay: {data.summary.avg_delay_delayed_only} mins
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.duration_distribution} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <XAxis
                  dataKey="range"
                  stroke="#64748B"
                  fontSize={10}
                  interval={0}
                  angle={-15}
                  textAnchor="end"
                />
                <YAxis stroke="#64748B" fontSize={10} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0B132B', borderColor: '#1E2E4E', borderRadius: '8px', fontSize: '11px' }}
                  formatter={(val: any) => [`${val} flights`, 'Frequency']}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {data.duration_distribution.map((entry, index) => (
                    <Cell
                      key={`bar-${index}`}
                      fill={index === 0 ? '#10B981' : index <= 2 ? '#F59E0B' : '#EF4444'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="text-[11px] text-slate-400 flex items-center justify-between bg-[#131F38] p-2 rounded-lg">
            <span>Overall Fleet OTP: <b className="text-emerald-400">{data.summary.on_time_performance_pct}%</b></span>
            <span>Total Schedule Volume: <b className="text-white">{data.summary.total_flights} movements</b></span>
          </div>
        </div>
      </div>

      {/* Airline OTP Performance Ranking Table */}
      <div className="bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-3">
        <div className="flex items-center justify-between pb-2 border-b border-[#1E2E4E]">
          <div className="flex items-center space-x-2">
            <Award className="w-4 h-4 text-cyan-400" />
            <h3 className="font-bold text-white text-sm">Airline On-Time Performance (OTP) Benchmark</h3>
          </div>
          <span className="text-[10px] text-slate-400 font-mono">Ranked by On-Time %</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px] tracking-wider">
                <th className="py-2.5 px-3">Airline</th>
                <th className="py-2.5 px-3">Total Flights</th>
                <th className="py-2.5 px-3">Delayed Flights</th>
                <th className="py-2.5 px-3">Avg Delay</th>
                <th className="py-2.5 px-3">Max Delay</th>
                <th className="py-2.5 px-3">On-Time Performance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {data.airline_performance.map((al, idx) => (
                <tr key={al.airline} className="hover:bg-[#131F38]/60 transition-colors">
                  <td className="py-2.5 px-3 font-semibold text-white flex items-center space-x-2">
                    <span className="w-5 text-slate-500 font-mono text-[10px]">#{idx + 1}</span>
                    <span>{al.airline}</span>
                  </td>
                  <td className="py-2.5 px-3 text-slate-300 font-mono">{al.total_flights}</td>
                  <td className="py-2.5 px-3 text-rose-400 font-mono">{al.delayed_flights}</td>
                  <td className="py-2.5 px-3 text-slate-300 font-mono">{al.avg_delay_mins}m</td>
                  <td className="py-2.5 px-3 text-slate-400 font-mono">{al.max_delay_mins}m</td>
                  <td className="py-2.5 px-3">
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-slate-800 h-2 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            al.otp_percentage >= 85
                              ? 'bg-emerald-400'
                              : al.otp_percentage >= 75
                              ? 'bg-amber-400'
                              : 'bg-rose-400'
                          }`}
                          style={{ width: `${al.otp_percentage}%` }}
                        />
                      </div>
                      <span className="font-mono font-bold text-white text-[11px]">{al.otp_percentage}%</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
