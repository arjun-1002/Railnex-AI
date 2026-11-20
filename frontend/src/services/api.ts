import {
  OverviewMetrics,
  SeverityPredictionInput,
  SeverityPredictionResult,
  MaintenancePriorityItem,
  TrackDeteriorationData,
  StationItem,
  EngineeringStandard,
  CvDefectPredictionResult,
  AssistantChatResult
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

export async function fetchMaintenanceAdvisory(): Promise<any> {
  const res = await fetch(`${API_BASE}/reports/advisory`);
  if (!res.ok) throw new Error(`Failed to load maintenance advisory: ${res.statusText}`);
  return res.json();
}

export async function fetchTrackDeterioration(): Promise<TrackDeteriorationData> {
  const res = await fetch(`${API_BASE}/track/deterioration`);
  if (!res.ok) throw new Error(`Failed to load deterioration: ${res.statusText}`);
  return res.json();
}

export async function simulateTrackDegradation(params: {
  line_segment_id: number;
  baseline_amplitude_mm: number;
  axle_load_tonnes: number;
  traffic_mgt_annual: number;
  deferred_maintenance_days: number;
  monsoon_rainfall_mm: number;
  ballast_condition: string;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/track/simulate-degradation`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  if (!res.ok) throw new Error(`Simulation failed: ${res.statusText}`);
  return res.json();
}

export async function fetchStations(zone: string = 'ALL', limit: number = 200): Promise<StationItem[]> {
  const query = zone && zone !== 'ALL' ? `?zone=${encodeURIComponent(zone)}&limit=${limit}` : `?limit=${limit}`;
  const res = await fetch(`${API_BASE}/network/stations${query}`);
  if (!res.ok) throw new Error(`Failed to load stations: ${res.statusText}`);
  return res.json();
}

export async function searchStations(query: string, limit: number = 25): Promise<StationItem[]> {
  const res = await fetch(`${API_BASE}/network/search?q=${encodeURIComponent(query)}&limit=${limit}`);
  if (!res.ok) throw new Error(`Search failed: ${res.statusText}`);
  return res.json();
}

export async function fetchZones(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/network/zones`);
  if (!res.ok) throw new Error(`Failed to load zones: ${res.statusText}`);
  return res.json();
}

export async function fetchModelEvaluation(): Promise<any> {
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
}): Promise<{ records: any[]; total: number; page: number; page_size: number; total_pages: number }> {
  const query = new URLSearchParams();
  query.set('page', params.page.toString());
  query.set('page_size', params.pageSize.toString());
  if (params.defectType) query.set('defect_type', params.defectType);
  if (params.lineSegment) query.set('line_segment', params.lineSegment.toString());

  const res = await fetch(`${API_BASE}/data/explorer?${query.toString()}`);
  if (!res.ok) throw new Error(`Failed to query explorer: ${res.statusText}`);
  return res.json();
}

// Module 7: Weather Intelligence
export async function fetchWeatherIntelligence(): Promise<any> {
  const res = await fetch(`${API_BASE}/weather/intelligence`);
  if (!res.ok) throw new Error(`Failed to load weather intelligence: ${res.statusText}`);
  return res.json();
}

// Module 9: Computer Vision Defect Recognition
export async function fetchCvSamples(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/cv/samples`);
  if (!res.ok) throw new Error(`Failed to load CV samples: ${res.statusText}`);
  return res.json();
}

export async function predictCvDefect(file: File): Promise<CvDefectPredictionResult> {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/cv/predict`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error(`CV prediction failed: ${res.statusText}`);
  return res.json();
}

// Module 10: Ultrasonic Flaw Detection (USFD)
export async function fetchUsfdFlaws(limit: number = 100): Promise<any[]> {
  const res = await fetch(`${API_BASE}/usfd/flaws?limit=${limit}`);
  if (!res.ok) throw new Error(`Failed to load USFD flaws: ${res.statusText}`);
  return res.json();
}

export async function fetchUsfdStandards(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/usfd/standards`);
  if (!res.ok) throw new Error(`Failed to load USFD standards: ${res.statusText}`);
  return res.json();
}

// Module 13: Safety Accidents
export async function fetchSafetyAccidents(): Promise<any> {
  const res = await fetch(`${API_BASE}/safety/accidents`);
  if (!res.ok) throw new Error(`Failed to load safety accidents: ${res.statusText}`);
  return res.json();
}

// Module 16: AI Maintenance Assistant
export async function sendAssistantChat(query: string, zone?: string): Promise<AssistantChatResult> {
  const res = await fetch(`${API_BASE}/assistant/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, context_zone: zone }),
  });
  if (!res.ok) throw new Error(`Assistant query failed: ${res.statusText}`);
  return res.json();
}

// Module 14: Datasets Manifest & Uploads
export async function fetchDatasetsManifest(): Promise<any> {
  const res = await fetch(`${API_BASE}/datasets/manifest`);
  if (!res.ok) throw new Error(`Failed to load dataset manifest: ${res.statusText}`);
  return res.json();
}

export async function uploadRtiTmsFile(file: File): Promise<any> {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/upload/rti-tms`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Upload failed: ${res.statusText}`);
  }
  return res.json();
}

export async function uploadWeatherFile(file: File): Promise<any> {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/upload/weather`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Upload failed: ${res.statusText}`);
  }
  return res.json();
}
