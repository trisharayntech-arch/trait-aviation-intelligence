export interface NavigationStep {
  step_number: number;
  instruction: string;
  distance_meters: number;
  estimated_minutes: number;
  landmark?: string;
}

export interface FlightGuidance {
  flight_number: string;
  airline: string;
  status: string;
  terminal: string;
  gate: string;
  checkin_desks: string;
  baggage_carousel: string;
  scheduled_time: string;
  estimated_time: string;
  delay_minutes: number;
  delay_reason: string;
  navigation_steps: NavigationStep[];
  quick_tips: string[];
}

export interface Facility {
  id: number;
  terminal: string;
  category: string;
  name: string;
  location_desc: string;
  level: string;
  walking_time_mins: number;
  wheelchair_accessible: boolean;
  opening_hours: string;
  amenities?: string;
}

export interface FAQItem {
  id: number;
  topic: string;
  category: string;
  question: string;
  answer: string;
  keywords: string;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
  language?: string;
  flightGuidance?: FlightGuidance | null;
  facilities?: Facility[];
  confidence?: number;
}

export interface KPISummary {
  otp_percentage: number;
  avg_delay_mins: number;
  avg_turnaround_mins: number;
  avg_security_wait_mins: number;
  first_bag_avg_mins: number;
  mishandled_bag_rate_per_1000: number;
  active_anomalies_count: number;
  total_flights_monitored: number;
  synthetic_disclaimer: string;
}

export interface DelayCausality {
  cause: string;
  flight_count: number;
  percentage: number;
}

export interface AirlineStat {
  airline: string;
  total_flights: number;
  delayed_flights: number;
  otp_percentage: number;
  avg_delay_mins: number;
  max_delay_mins: number;
}

export interface TerminalStat {
  terminal: string;
  total_flights: number;
  delayed_flights: number;
  avg_delay_mins: number;
  otp_percentage: number;
}

export interface DelayDistribution {
  range: string;
  count: number;
}

export interface DelayAnalysisData {
  summary: {
    total_flights: number;
    delayed_flights: number;
    on_time_performance_pct: number;
    avg_delay_all_flights: number;
    avg_delay_delayed_only: number;
  };
  causality_breakdown: DelayCausality[];
  airline_performance: AirlineStat[];
  terminal_performance: TerminalStat[];
  duration_distribution: DelayDistribution[];
  synthetic_disclaimer: string;
}

export interface PassengerTrendPoint {
  timestamp: string;
  hour_label: string;
  total_inbound: number;
  total_outbound: number;
  total_passengers: number;
  avg_security_wait_mins: number;
  avg_capacity_pct: number;
}

export interface CarouselStat {
  carousel_id: string;
  terminal: string;
  flights_handled: number;
  total_bags: number;
  avg_last_bag_mins: number;
  status: string;
}

export interface PassengerBaggageData {
  passenger_trend: PassengerTrendPoint[];
  terminal_utilization: any[];
  baggage_summary: {
    total_bags: number;
    processed_bags: number;
    mishandled_bags: number;
    mishandled_rate_per_1000: number;
    avg_first_bag_mins: number;
    avg_last_bag_mins: number;
    avg_dwell_time_mins: number;
    sla_compliance_pct: number;
  };
  carousel_breakdown: CarouselStat[];
  synthetic_disclaimer: string;
}

export interface AnomalyItem {
  id: number;
  timestamp: string;
  incident_type: string;
  flight_number?: string;
  airline?: string;
  location: string;
  metric_name: string;
  observed_value: number;
  expected_range: string;
  anomaly_score: number;
  severity: 'HIGH' | 'MEDIUM' | 'LOW';
  description: string;
  status: string;
}

export interface ScatterPoint {
  flight_number: string;
  turnaround_mins: number;
  delay_mins: number;
  passengers: number;
  is_anomaly: boolean;
  severity: 'HIGH' | 'MEDIUM' | 'NORMAL';
}

export interface AnomalyData {
  active_anomalies_count: number;
  total_anomalies_detected: number;
  anomalies: AnomalyItem[];
  scatter_points: ScatterPoint[];
  model_metadata: {
    algorithm: string;
    features_used: string[];
    contamination_rate: number;
  };
  synthetic_disclaimer: string;
}

export interface ForecastPoint {
  timestamp: string;
  hour_label: string;
  actual?: number | null;
  predicted?: number | null;
  lower_bound?: number | null;
  upper_bound?: number | null;
  type: 'Historical' | 'Forecast';
}

export interface ForecastData {
  metric: string;
  unit: string;
  model_name: string;
  confidence_level: string;
  points: ForecastPoint[];
  insights: {
    forecast_peak_hour: string;
    forecast_peak_volume: number;
    forecast_trough_hour: string;
    forecast_trough_volume: number;
    recommended_staffing_action: string;
    baggage_staffing_action?: string;
    gate_allocation_action?: string;
  };

  synthetic_disclaimer: string;
}
