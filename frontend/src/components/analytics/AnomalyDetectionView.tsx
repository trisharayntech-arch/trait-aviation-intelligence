import React from 'react';
import {
  ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip, ResponsiveContainer, Cell
} from 'recharts';
import { AnomalyData } from '../../types';
import { AlertTriangle, Cpu, CheckCircle2, ShieldAlert } from 'lucide-react';

interface AnomalyDetectionViewProps {
  data: AnomalyData | null;
  loading: boolean;
}

export const AnomalyDetectionView: React.FC<AnomalyDetectionViewProps> = ({ data, loading }) => {
  if (loading || !data) {
    return <div className="text-center py-20 text-slate-400 text-xs">Loading machine learning anomaly model...</div>;
  }

  const normalPoints = data.scatter_points.filter((p) => !p.is_anomaly);
  const anomalyPoints = data.scatter_points.filter((p) => p.is_anomaly);

  return (
    <div className="space-y-6">
      {/* ML Metadata Banner */}
      <div className="bg-[#121E3B] border border-cyan-800/50 p-4 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-3 shadow-lg">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-cyan-950 rounded-xl border border-cyan-700/60">
            <Cpu className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-white text-sm">Scikit-Learn IsolationForest Operational Monitor</span>
              <span className="text-[10px] bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded font-mono">
                Model Active
              </span>
            </div>
            <div className="text-xs text-slate-400 mt-0.5">
              Multi-dimensional outlier detection on turnaround times, delays, and baggage reclaim dwell. Contamination rate: {data.model_metadata.contamination_rate * 100}%.
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-4 text-xs font-mono">
          <div className="bg-[#0B132B] px-3 py-1.5 rounded-lg border border-slate-700">
            <span className="text-slate-400">ML-Detected Anomalies: </span>
            <span className="font-bold text-amber-400">{data.total_anomalies_detected}</span>
          </div>
          <div className="bg-[#0B132B] px-3 py-1.5 rounded-lg border border-slate-700">
            <span className="text-slate-400">Active High-Severity: </span>
            <span className="font-bold text-rose-400">{data.active_anomalies_count}</span>
          </div>
        </div>
      </div>

      {/* Grid: Scatter Plot (Left) + Anomalies Feed (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* ML Scatter Plot */}
        <div className="lg:col-span-6 bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-[#1E2E4E]">
            <h3 className="font-bold text-white text-sm">Operational Envelope: Turnaround vs Delay</h3>
            <span className="text-[10px] text-slate-400 font-mono">Isolation Forest Classification</span>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 10, right: 10, bottom: 20, left: -20 }}>
                <XAxis
                  type="number"
                  dataKey="turnaround_mins"
                  name="Turnaround Duration"
                  unit="m"
                  stroke="#64748B"
                  fontSize={10}
                  label={{ value: 'Turnaround Time (minutes)', position: 'insideBottom', offset: -10, fill: '#94A3B8', fontSize: 10 }}
                />
                <YAxis
                  type="number"
                  dataKey="delay_mins"
                  name="Flight Delay"
                  unit="m"
                  stroke="#64748B"
                  fontSize={10}
                  label={{ value: 'Delay (mins)', angle: -90, position: 'insideLeft', offset: 25, fill: '#94A3B8', fontSize: 10 }}
                />
                <ZAxis type="number" range={[60, 160]} />
                <Tooltip
                  cursor={{ strokeDasharray: '3 3' }}
                  content={({ payload }) => {
                    if (!payload || payload.length === 0) return null;
                    const p = payload[0].payload;
                    return (
                      <div className="bg-[#0B132B] border border-[#1E2E4E] p-2.5 rounded-lg text-xs space-y-1 shadow-lg">
                        <div className="font-bold text-white font-mono">{p.flight_number}</div>
                        <div className="text-slate-300">Turnaround: {p.turnaround_mins} mins</div>
                        <div className="text-slate-300">Delay: {p.delay_mins} mins</div>
                        <div className={`font-semibold ${p.is_anomaly ? 'text-rose-400' : 'text-emerald-400'}`}>
                          {p.is_anomaly ? `Anomaly: ${p.severity}` : 'Normal Operation'}
                        </div>
                      </div>
                    );
                  }}
                />
                <Scatter name="Normal Operations" data={normalPoints} fill="#10B981" fillOpacity={0.6} />
                <Scatter name="Flagged Outliers" data={anomalyPoints} fill="#EF4444" fillOpacity={0.9} />
              </ScatterChart>
            </ResponsiveContainer>
          </div>

          <div className="flex items-center justify-center space-x-6 text-[11px] pt-2 border-t border-slate-800">
            <div className="flex items-center space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
              <span className="text-slate-300">Normal Operational Range</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
              <span className="text-slate-300">IsolationForest Detected Outlier</span>
            </div>
          </div>
        </div>

        {/* Real-time Anomalies Feed */}
        <div className="lg:col-span-6 bg-[#0E172E] rounded-2xl border border-[#1E2E4E] p-5 shadow-xl space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-[#1E2E4E]">
            <h3 className="font-bold text-white text-sm">Active Anomaly Alerts & Root Cause Analysis</h3>
            <span className="text-[10px] text-cyan-400 font-mono">Real-time Feed</span>
          </div>

          <div className="space-y-2.5 max-h-[340px] overflow-y-auto pr-1">
            {data.anomalies.map((a) => (
              <div
                key={a.id}
                className={`p-3 rounded-xl border text-xs space-y-2 transition-all ${
                  a.severity === 'HIGH'
                    ? 'bg-rose-950/20 border-rose-800/60'
                    : 'bg-amber-950/20 border-amber-800/60'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-black font-mono border ${
                        a.severity === 'HIGH'
                          ? 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                          : 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                      }`}
                    >
                      {a.severity}
                    </span>
                    <span className="font-bold text-white">{a.incident_type}</span>
                  </div>
                  <span className="text-[10px] text-slate-400 font-mono">{a.location}</span>
                </div>

                <p className="text-slate-300 text-[11px] leading-relaxed">{a.description}</p>

                <div className="flex items-center justify-between text-[10px] pt-1 border-t border-slate-800 text-slate-400 font-mono">
                  <span>
                    Observed: <b className="text-white">{a.observed_value} mins</b> (Exp: {a.expected_range})
                  </span>
                  <span>IF Score: <b className="text-cyan-400">{a.anomaly_score}</b></span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
