import React from 'react';
import { Plane, Clock, ShieldCheck, Luggage, AlertTriangle, Activity } from 'lucide-react';
import { KPISummary } from '../../types';

interface KPICardsProps {
  kpis: KPISummary | null;
  loading: boolean;
}

export const KPICards: React.FC<KPICardsProps> = ({ kpis, loading }) => {
  if (loading || !kpis) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="bg-[#0E172E] p-4 rounded-xl border border-slate-800 animate-pulse h-24"></div>
        ))}
      </div>
    );
  }

  const cards = [
    {
      title: 'On-Time Performance',
      value: `${kpis.otp_percentage}%`,
      subtitle: 'Target: >85.0%',
      icon: <Activity className="w-4 h-4 text-emerald-400" />,
      color: kpis.otp_percentage >= 85 ? 'text-emerald-400' : 'text-amber-400',
      bgGlow: 'from-emerald-500/10 to-transparent',
    },
    {
      title: 'Average Flight Delay',
      value: `${kpis.avg_delay_mins}m`,
      subtitle: `${kpis.total_flights_monitored} flights tracked`,
      icon: <Plane className="w-4 h-4 text-cyan-400" />,
      color: 'text-cyan-400',
      bgGlow: 'from-cyan-500/10 to-transparent',
    },
    {
      title: 'Avg Turnaround Time',
      value: `${kpis.avg_turnaround_mins}m`,
      subtitle: 'Target SLA: 45m',
      icon: <Clock className="w-4 h-4 text-blue-400" />,
      color: 'text-blue-400',
      bgGlow: 'from-blue-500/10 to-transparent',
    },
    {
      title: 'Security Wait Time',
      value: `${kpis.avg_security_wait_mins}m`,
      subtitle: 'Peak throughput SLA: 15m',
      icon: <ShieldCheck className="w-4 h-4 text-indigo-400" />,
      color: 'text-indigo-400',
      bgGlow: 'from-indigo-500/10 to-transparent',
    },
    {
      title: 'First Bag Delivery',
      value: `${kpis.first_bag_avg_mins}m`,
      subtitle: 'Target SLA: <20m',
      icon: <Luggage className="w-4 h-4 text-purple-400" />,
      color: 'text-purple-400',
      bgGlow: 'from-purple-500/10 to-transparent',
    },
    {
      title: 'Active ML Anomalies',
      value: kpis.active_anomalies_count.toString(),
      subtitle: 'IsolationForest Flagged',
      icon: <AlertTriangle className="w-4 h-4 text-rose-400" />,
      color: kpis.active_anomalies_count > 0 ? 'text-rose-400' : 'text-emerald-400',
      bgGlow: 'from-rose-500/10 to-transparent',
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
      {cards.map((card, idx) => (
        <div
          key={idx}
          className={`bg-gradient-to-b ${card.bgGlow} bg-[#0E172E] p-4 rounded-xl border border-[#1E2E4E] shadow-md space-y-1.5`}
        >
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold text-slate-400 truncate">{card.title}</span>
            <div className="p-1 rounded-md bg-[#131F38] border border-slate-700/60">{card.icon}</div>
          </div>
          <div className={`text-2xl font-black font-mono tracking-tight ${card.color}`}>{card.value}</div>
          <div className="text-[10px] text-slate-400 truncate">{card.subtitle}</div>
        </div>
      ))}
    </div>
  );
};
