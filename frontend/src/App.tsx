import React, { useState } from 'react';
import { Header } from './components/Header';
import { AirportAIModule } from './components/airport-ai/AirportAIModule';
import { AnalyticsModule } from './components/analytics/AnalyticsModule';
import { api } from './services/api';
import { ShieldAlert, CheckCircle2 } from 'lucide-react';

export const App: React.FC = () => {
  const [activeModule, setActiveModule] = useState<'airport-ai' | 'analytics'>('airport-ai');
  const [language, setLanguage] = useState<string>('en');
  const [isReseeding, setIsReseeding] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const handleReseed = async () => {
    setIsReseeding(true);
    try {
      await api.reseedDatabase();
      setToastMessage('Database reseeded successfully with fresh synthetic demonstration data.');
      setTimeout(() => {
        setToastMessage(null);
        window.location.reload();
      }, 1500);
    } catch (err) {
      setToastMessage('Failed to reseed database. Check backend connection.');
      setTimeout(() => setToastMessage(null), 3000);
    } finally {
      setIsReseeding(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#070D1E] text-slate-100 flex flex-col font-sans">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-[#121E3B] border border-cyan-500/50 text-white px-4 py-3 rounded-xl shadow-2xl flex items-center space-x-2.5 text-xs animate-bounce">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Persistent Global Header */}
      <Header
        activeModule={activeModule}
        setActiveModule={setActiveModule}
        language={language}
        setLanguage={setLanguage}
        onReseed={handleReseed}
        isReseeding={isReseeding}
      />

      {/* Main Module Content */}
      <main className="flex-1 pb-12">
        {activeModule === 'airport-ai' ? (
          <AirportAIModule language={language} />
        ) : (
          <AnalyticsModule />
        )}
      </main>

      {/* Global Footer */}
      <footer className="bg-[#0B132B] border-t border-[#1C2D4A] py-6 px-4 sm:px-6 lg:px-8 mt-auto text-xs text-slate-400">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-white">TRAIT Aviation Intelligence</span>
            <span>•</span>
            <span>TRAIT Innovation Platform</span>
            <span>•</span>
            <span className="text-cyan-400 font-mono">v2.0.0 Local Production</span>
          </div>
          <div className="flex items-center space-x-2 text-amber-400/90 bg-amber-950/40 px-3 py-1 rounded-lg border border-amber-800/40 text-[11px]">
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>SYNTHETIC DEMONSTRATION DATA ONLY • ZERO PAID API COST</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
