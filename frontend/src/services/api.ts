import {
  OverviewMetrics,
  SeverityPredictionInput,
  SeverityPredictionResult,
  MaintenancePriorityItem,
  TrackDeteriorationData,
  StationItem,
  ModelBenchmarkSummary,
  EngineeringStandard
} from '../types';

const API_BASE = '/api';

export async function fetchOverviewMetrics(): Promise<OverviewMetrics> {
  const res = await fetch(`${API_BASE}/overview`);
  if (!res.ok) throw new Error(`Failed to load overview: ${res.statusText}`);
  return res.json();
}

export async function predictDefectSeverity(input: SeverityPredictionInput): Promise<SeverityPredictionResult> {
  const res = await fetch(`${API_BASE}/predict/severity`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });
  if (!res.ok) throw new Error(`Prediction failed: ${res.statusText}`);
  return res.json();
}

export async function fetchMaintenancePrioritization(params?: {
  urgency?: string;
  defect_type?: string;
  line_segment?: number;
  limit?: number;
}): Promise<MaintenancePriorityItem[]> {
  const query = new URLSearchParams();
  if (params?.urgency) query.set('urgency', params.urgency);
  if (params?.defect_type) query.set('defect_type', params.defect_type);
  if (params?.line_segment) query.set('line_segment', params.line_segment.toString());
  if (params?.limit) query.set('limit', params.limit.toString());

  const res = await fetch(`${API_BASE}/maintenance/prioritization?${query.toString()}`);
  if (!res.ok) throw new Error(`Failed to load prioritization: ${res.statusText}`);
  return res.json();
}

export async function fetchTrackDeterioration(): Promise<TrackDeteriorationData> {
  const res = await fetch(`${API_BASE}/track/deterioration`);
  if (!res.ok) throw new Error(`Failed to load deterioration: ${res.statusText}`);
  return res.json();
}

export async function fetchStations(zone: string = 'ALL', limit: number = 200): Promise<StationItem[]> {
  const res = await fetch(`${API_BASE}/network/stations?zone=${encodeURIComponent(zone)}&limit=${limit}`);
  if (!res.ok) throw new Error(`Failed to load stations: ${res.statusText}`);
  return res.json();
}

export async function fetchZones(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/network/zones`);
  if (!res.ok) throw new Error(`Failed to load zones: ${res.statusText}`);
  return res.json();
}

export async function fetchWeatherAnalytics(): Promise<any> {
  const res = await fetch(`${API_BASE}/weather/analysis`);
  if (!res.ok) throw new Error(`Failed to load weather: ${res.statusText}`);
  return res.json();
}

export async function fetchModelEvaluation(): Promise<ModelBenchmarkSummary> {
  const res = await fetch(`${API_BASE}/models/evaluation`);
  if (!res.ok) throw new Error(`Failed to load evaluation: ${res.statusText}`);
  return res.json();
}

export async function fetchEngineeringStandards(): Promise<EngineeringStandard[]> {
  const res = await fetch(`${API_BASE}/standards`);
  if (!res.ok) throw new Error(`Failed to load standards: ${res.statusText}`);
  return res.json();
}

export async function queryDataExplorer(params: {
  page: number;
  pageSize: number;
  defectType?: string;
  priority?: string;
  lineSegment?: number;
}): Promise<{ records: any[]; total: number; page: number; total_pages: number }> {
  const query = new URLSearchParams();
  query.set('page', params.page.toString());
  query.set('page_size', params.pageSize.toString());
  if (params.defectType) query.set('defect_type', params.defectType);
  if (params.priority) query.set('priority', params.priority);
  if (params.lineSegment) query.set('line_segment', params.lineSegment.toString());

  const res = await fetch(`${API_BASE}/data/explorer?${query.toString()}`);
  if (!res.ok) throw new Error(`Failed to query explorer: ${res.statusText}`);
  return res.json();
}
