import {
  FlightGuidance, Facility, FAQItem, KPISummary,
  DelayAnalysisData, PassengerBaggageData, AnomalyData, ForecastData
} from '../types';

const API_BASE = '/api';

export const api = {
  // Health
  checkHealth: async () => {
    const res = await fetch(`${API_BASE}/health`);
    return res.json();
  },

  // Reseed synthetic DB
  reseedDatabase: async () => {
    const res = await fetch(`${API_BASE}/reseed`, { method: 'POST' });
    return res.json();
  },

  // Module 1: AirportAI
  sendChatMessage: async (query: string, language: string = 'en', flightNumber?: string) => {
    const res = await fetch(`${API_BASE}/airport-ai/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, language, flight_number: flightNumber }),
    });
    if (!res.ok) throw new Error('Failed to process message');
    return res.json();
  },

  getFlightGuidance: async (flightNumber: string, lang: string = 'en'): Promise<{ guidance: FlightGuidance }> => {
    const res = await fetch(`${API_BASE}/airport-ai/flight/${encodeURIComponent(flightNumber)}?lang=${lang}`);
    if (!res.ok) throw new Error(`Flight ${flightNumber} not found`);
    return res.json();
  },

  getFacilities: async (terminal?: string, category?: string): Promise<{ facilities: Facility[] }> => {
    let url = `${API_BASE}/airport-ai/terminals?`;
    if (terminal) url += `terminal=${encodeURIComponent(terminal)}&`;
    if (category) url += `category=${encodeURIComponent(category)}&`;
    const res = await fetch(url);
    return res.json();
  },

  getFaqs: async (lang: string = 'en'): Promise<{ faqs: FAQItem[] }> => {
    const res = await fetch(`${API_BASE}/airport-ai/faqs?lang=${lang}`);
    return res.json();
  },

  // Module 2: Aviation Analytics
  getKpis: async (): Promise<KPISummary> => {
    const res = await fetch(`${API_BASE}/analytics/kpis`);
    return res.json();
  },

  getDelayAnalysis: async (): Promise<DelayAnalysisData> => {
    const res = await fetch(`${API_BASE}/analytics/delays`);
    return res.json();
  },

  getPassengerBaggage: async (): Promise<PassengerBaggageData> => {
    const res = await fetch(`${API_BASE}/analytics/passenger-baggage`);
    return res.json();
  },

  getAnomalies: async (): Promise<AnomalyData> => {
    const res = await fetch(`${API_BASE}/analytics/anomalies`);
    return res.json();
  },

  getForecast: async (): Promise<ForecastData> => {
    const res = await fetch(`${API_BASE}/analytics/forecast`);
    return res.json();
  },

  // Download URLs
  getFlightsCsvUrl: () => `${API_BASE}/analytics/export/flights`,
  getBaggageCsvUrl: () => `${API_BASE}/analytics/export/baggage`,
  getDigestUrl: () => `${API_BASE}/analytics/export/digest`,
  getJsonUrl: () => `${API_BASE}/analytics/export/json`,

  // CSV Upload
  uploadFlightsCsv: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/analytics/upload/flights-csv`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
      throw new Error(err.detail || 'CSV upload failed');
    }
    return res.json();
  },
};

