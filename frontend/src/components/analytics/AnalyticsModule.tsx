import React, { useState, useEffect } from 'react';
import { KPICards } from './KPICards';
import { DelayAnalysisView } from './DelayAnalysisView';
import { PassengerBaggageView } from './PassengerBaggageView';
import { AnomalyDetectionView } from './AnomalyDetectionView';
import { ForecastingView } from './ForecastingView';
import { ReportsModal } from './ReportsModal';
import { KPISummary, DelayAnalysisData, PassengerBaggageData, AnomalyData, ForecastData } from '../../types';
import { api } from '../../services/api';
import { Plane, Users, AlertTriangle, TrendingUp, Download, RefreshCw } from 'lucide-react';

export const AnalyticsModule: React.FC = () => {
  const [subTab, setSubTab] = useState<'delays' | 'pax-bag' | 'anomalies' | 'forecast'>('delays');
  const [isReportsOpen, setIsReportsOpen] = useState(false);

  const [kpis, setKpis] = useState<KPISummary | null>(null);
  const [delays, setDelays] = useState<DelayAnalysisData | null>(null);
  const [paxBag, setPaxBag] = useState<PassengerBaggageData | null>(null);
  const [anomalies, setAnomalies] = useState<AnomalyData | null>(null);
  const [forecast, setForecast] = useState<ForecastData | null>(null);

  const [loading, setLoading] = useState(true);

  const loadAllData = async () => {
    setLoading(true);
    try {
      const [kpiRes, delayRes, pbRes, anomRes, foreRes] = await Promise.all([
        api.getKpis(),
        api.getDelayAnalysis(),
        api.getPassengerBaggage(),
        api.getAnomalies(),
        api.getForecast(),
      ]);
      setKpis(kpiRes);
      setDelays(delayRes);
      setPaxBag(pbRes);
      setAnomalies(anomRes);
      setForecast(foreRes);
    } catch (err) {
      console.error('Failed to load analytics data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      {/* Module Title Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-[#141B3B] via-[#0E172E] to-[#1F183E] p-5 rounded-2xl border border-[#1E2E4E] shadow-lg">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl font-black text-white tracking-tight">TRAIT Aviation Analytics</h1>
            <span className="bg-purple-600/30 text-purple-300 text-xs px-2.5 py-0.5 rounded-full font-semibold border border-purple-500/40">
              Module 2: Operations Intelligence
            </span>
          </div>
          <p className="text-xs text-slate-300 mt-1 max-w-2xl">
            Real-time flight OTP tracking, baggage turnaround dwell metrics, Scikit-Learn IsolationForest anomaly detection, and Statsmodels time-series forecasting.
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center space-x-3 shrink-0">
          <button
            onClick={() => setIsReportsOpen(true)}
            className="flex items-center space-x-1.5 bg-blue-600 hover:bg-blue-500 text-white px-3.5 py-2 rounded-xl text-xs font-semibold shadow-md shadow-blue-500/20 transition-all"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Reports</span>
          </button>
          <button
            onClick={loadAllData}
            title="Refresh operational metrics"
            className="p-2 rounded-xl bg-[#121E3B] hover:bg-[#1A2A50] border border-slate-700 text-slate-300 hover:text-white transition-colors"
          >
            <RefreshCw className={`w-4 h-4 text-cyan-400 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* Executive Operational KPI Ribbon */}
      <KPICards kpis={kpis} loading={loading} />

      {/* Analytics Sub-tabs Navigation */}
      <div className="flex items-center justify-between border-b border-[#1E2E4E] pb-3">
        <div className="flex items-center space-x-2 overflow-x-auto no-scrollbar">
          <button
            onClick={() => setSubTab('delays')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0 ${
              subTab === 'delays'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'text-slate-400 hover:text-white hover:bg-[#121E3B]'
            }`}
          >
            <Plane className="w-3.5 h-3.5" />
            <span>Flight Delays & OTP</span>
          </button>

          <button
            onClick={() => setSubTab('pax-bag')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0 ${
              subTab === 'pax-bag'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'text-slate-400 hover:text-white hover:bg-[#121E3B]'
            }`}
          >
            <Users className="w-3.5 h-3.5" />
            <span>Passenger & Baggage Flow</span>
          </button>

          <button
            onClick={() => setSubTab('anomalies')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0 ${
              subTab === 'anomalies'
                ? 'bg-purple-600 text-white shadow-md shadow-purple-500/20'
                : 'text-slate-400 hover:text-white hover:bg-[#121E3B]'
            }`}
          >
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>ML Anomaly Detection</span>
            {anomalies && anomalies.active_anomalies_count > 0 && (
              <span className="bg-rose-500 text-white text-[10px] px-1.5 py-0.2 rounded-full font-mono font-bold">
                {anomalies.active_anomalies_count}
              </span>
            )}
          </button>

          <button
            onClick={() => setSubTab('forecast')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0 ${
              subTab === 'forecast'
                ? 'bg-cyan-600 text-white shadow-md shadow-cyan-500/20'
                : 'text-slate-400 hover:text-white hover:bg-[#121E3B]'
            }`}
          >
            <TrendingUp className="w-3.5 h-3.5" />
            <span>Predictive Forecasting</span>
          </button>
        </div>
      </div>

      {/* Tab Panels */}
      {subTab === 'delays' && <DelayAnalysisView data={delays} loading={loading} />}
      {subTab === 'pax-bag' && <PassengerBaggageView data={paxBag} loading={loading} />}
      {subTab === 'anomalies' && <AnomalyDetectionView data={anomalies} loading={loading} />}
      {subTab === 'forecast' && <ForecastingView data={forecast} loading={loading} />}

      {/* Reports Export Modal */}
      <ReportsModal isOpen={isReportsOpen} onClose={() => setIsReportsOpen(false)} />
    </div>
  );
};
