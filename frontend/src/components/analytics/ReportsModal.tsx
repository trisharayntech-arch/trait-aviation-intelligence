import React, { useState, useRef } from 'react';
import { Download, Upload, FileText, FileSpreadsheet, Code2, X, ShieldAlert, CheckCircle2, AlertCircle } from 'lucide-react';
import { api } from '../../services/api';

interface ReportsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUploadSuccess?: () => void;
}

export const ReportsModal: React.FC<ReportsModalProps> = ({ isOpen, onClose, onUploadSuccess }) => {
  const [activeTab, setActiveTab] = useState<'export' | 'import'>('export');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const reports = [
    {
      title: 'Operational Flights Dataset (CSV)',
      desc: 'Complete schedule of 125+ flights with scheduled vs actual times, terminals, gates, delays, and reasons.',
      icon: <FileSpreadsheet className="w-5 h-5 text-emerald-400" />,
      url: api.getFlightsCsvUrl(),
      format: 'CSV (Tabular)',
      type: 'flights',
    },
    {
      title: 'Baggage Operations & Carousels (CSV)',
      desc: 'Baggage claim throughput across all active carousels, first-bag and last-bag delivery SLA metrics.',
      icon: <FileSpreadsheet className="w-5 h-5 text-cyan-400" />,
      url: api.getBaggageCsvUrl(),
      format: 'CSV (Tabular)',
      type: 'baggage',
    },
    {
      title: 'Executive Operational Digest (Text / MD)',
      desc: 'Formatted high-level summary with KPIs, delay breakdown, Isolation Forest anomalies, and resource advice.',
      icon: <FileText className="w-5 h-5 text-blue-400" />,
      url: api.getDigestUrl(),
      format: 'Plaintext / Markdown',
      type: 'digest',
    },
    {
      title: 'Full Operational State Audit (JSON)',
      desc: 'Machine-readable snapshot including all models, forecast intervals, active anomalies, and facility matrices.',
      icon: <Code2 className="w-5 h-5 text-purple-400" />,
      url: api.getJsonUrl(),
      format: 'JSON (Raw API)',
      type: 'json',
    },
  ];

  const handleDownload = (url: string) => {
    window.open(url, '_blank');
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setUploadMessage(null);
      setUploadError(null);
    }
  };

  const handleUploadSubmit = async () => {
    if (!selectedFile) return;
    setIsUploading(true);
    setUploadMessage(null);
    setUploadError(null);

    try {
      const res = await api.uploadFlightsCsv(selectedFile);
      setUploadMessage(`Success: Imported ${res.rows_imported} flight records from ${res.filename}.`);
      setSelectedFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      if (onUploadSuccess) onUploadSuccess();
    } catch (err: any) {
      setUploadError(err.message || 'Failed to import CSV file. Please verify columns.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
      <div className="bg-[#0E172E] border border-[#1E2E4E] rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden space-y-4">
        {/* Header */}
        <div className="bg-[#121E3B] px-6 py-4 border-b border-[#1E2E4E] flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-1 bg-[#090F20] p-1 rounded-xl border border-slate-700/80">
              <button
                onClick={() => setActiveTab('export')}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeTab === 'export'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                <Download className="w-3.5 h-3.5" />
                <span>Export Reports</span>
              </button>
              <button
                onClick={() => setActiveTab('import')}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeTab === 'import'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                <Upload className="w-3.5 h-3.5" />
                <span>Import Schedule (CSV)</span>
              </button>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Disclaimer */}
        <div className="px-6">
          <div className="bg-amber-950/30 border border-amber-800/40 p-3 rounded-xl flex items-center space-x-2.5 text-xs text-amber-300">
            <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0" />
            <span>
              All imported & downloaded operational datasets are processed under <b>SYNTHETIC DEMONSTRATION DATA</b> rules.
            </span>
          </div>
        </div>

        {/* Tab 1: Export Reports */}
        {activeTab === 'export' && (
          <div className="px-6 space-y-3 pb-6 max-h-[440px] overflow-y-auto">
            {reports.map((rep) => (
              <div
                key={rep.type}
                className="bg-[#121E3B] border border-[#22355A] hover:border-cyan-600/50 p-4 rounded-xl flex items-center justify-between gap-4 transition-all"
              >
                <div className="flex items-start space-x-3">
                  <div className="p-2 rounded-lg bg-[#0B132B] border border-slate-700/60 shrink-0 mt-0.5">
                    {rep.icon}
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <h4 className="font-bold text-white text-sm">{rep.title}</h4>
                      <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">
                        {rep.format}
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 mt-0.5">{rep.desc}</p>
                  </div>
                </div>

                <button
                  onClick={() => handleDownload(rep.url)}
                  className="shrink-0 flex items-center space-x-1.5 bg-blue-600 hover:bg-blue-500 text-white px-3 py-2 rounded-lg text-xs font-semibold shadow-sm transition-colors"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download</span>
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Tab 2: Import CSV Schedule */}
        {activeTab === 'import' && (
          <div className="px-6 space-y-4 pb-6">
            <div className="bg-[#121E3B] border border-[#22355A] rounded-xl p-5 space-y-3">
              <h4 className="font-bold text-white text-sm flex items-center space-x-2">
                <FileSpreadsheet className="w-4 h-4 text-cyan-400" />
                <span>Upload Flights Schedule (.csv)</span>
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Upload a CSV file with flight schedules. Required columns: <code className="text-cyan-300 font-mono">flight_number, airline, origin, destination, scheduled_time, terminal, gate</code>. Optional: <code className="text-slate-300 font-mono">status, delay_minutes, delay_reason, checkin_desks, baggage_carousel</code>.
              </p>

              <div className="pt-2">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".csv"
                  onChange={handleFileChange}
                  className="block w-full text-xs text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-500 cursor-pointer"
                />
              </div>

              {selectedFile && (
                <div className="text-xs text-slate-300 bg-[#0B132B] p-2.5 rounded-lg flex items-center justify-between border border-slate-700">
                  <span className="truncate">Selected: <b>{selectedFile.name}</b> ({(selectedFile.size / 1024).toFixed(1)} KB)</span>
                  <button
                    onClick={handleUploadSubmit}
                    disabled={isUploading}
                    className="ml-3 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg font-semibold shrink-0 disabled:opacity-50 transition-colors flex items-center space-x-1"
                  >
                    <Upload className="w-3.5 h-3.5" />
                    <span>{isUploading ? 'Importing...' : 'Upload & Ingest'}</span>
                  </button>
                </div>
              )}

              {uploadMessage && (
                <div className="p-3 bg-emerald-950/40 border border-emerald-800/60 rounded-xl text-xs text-emerald-300 flex items-center space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>{uploadMessage}</span>
                </div>
              )}

              {uploadError && (
                <div className="p-3 bg-rose-950/40 border border-rose-800/60 rounded-xl text-xs text-rose-300 flex items-center space-x-2">
                  <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
                  <span>{uploadError}</span>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
