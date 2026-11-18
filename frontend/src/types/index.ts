export type TabType = 
  | 'overview' 
  | 'track_analysis' 
  | 'severity_prediction' 
  | 'maintenance_priority' 
  | 'network_map' 
  | 'data_explorer' 
  | 'model_evaluation' 
  | 'settings';

export interface OverviewMetrics {
  summary_cards: {
    total_inspection_records: number;
    monitored_line_segments: number;
    critical_red_tags: number;
    planned_yellow_tags: number;
    active_railway_stations: number;
    operational_zones_tracked: number;
    model_champion: string;
    champion_f1_score: number;
  };
  severity_distribution: Array<{
    name: string;
    count: number;
    percentage: number;
    color: string;
  }>;
  defect_type_breakdown: Array<{
    defect_type: string;
    count: number;
    color: string;
  }>;
  inspection_trends: Array<{
    period: string;
    inspections: number;
  }>;
  cag_derailment_causation: Array<{
    cause_category: string;
    specific_cause: string;
    incident_count: number;
    percentage_of_total: number;
    department_responsible: string;
  }>;
  datasets_manifest: Array<{
    dataset_id: string;
    name: string;
    category: string;
    records: number;
    observation_period: string;
    validation_status: string;
    ml_role: string;
  }>;
}

export interface SeverityPredictionInput {
  defect_length_ft: number;
  defect_amplitude_in: number;
  fra_track_class: number;
  freight_speed_limit_mph: number;
  passenger_speed_limit_mph: number;
  defect_type: string;
  curve_spiral_tangent_code: string;
  track_code: string;
  inspection_month: number;
}

export interface ContributingFactor {
  feature: string;
  impact: string;
  description: string;
}

export interface StandardsComparison {
  parameter: string;
  recorded_value: string;
  irpwm_standard: string;
  status: string;
}

export interface SeverityPredictionResult {
  predicted_class: string;
  severity_label: string;
  urgency_level: string;
  confidence_score: number;
  probabilities: {
    Yellow_Tag_Planned: number;
    Red_Tag_Urgent: number;
  };
  contributing_factors: ContributingFactor[];
  standards_comparison: StandardsComparison[];
  suggested_action: string;
  limitations_disclaimer: string;
}

export interface MaintenancePriorityItem {
  record_id: number;
  line_segment_id: number;
  milepost: number;
  defect_type: string;
  defect_length_ft: number;
  defect_amplitude_in: number;
  predicted_severity: string;
  confidence: number;
  priority_score: number;
  priority_tier: 'CRITICAL_REVIEW' | 'HIGH_PRIORITY' | 'SCHEDULED_MONITORING';
  suggested_action: string;
  inspection_date?: string;
}

export interface TrackDeteriorationData {
  top_deteriorating_segments: Array<{
    line_segment_id: number;
    total_inspections: number;
    red_tags: number;
    avg_amplitude: number;
    max_amplitude: number;
    red_tag_ratio: number;
    deterioration_trend: string;
    urgency_rank: number;
  }>;
  longitudinal_sample_segment: {
    line_segment_id: number;
    history: Array<{
      quarter: string;
      defect_count: number;
      avg_amp: number;
      red_count: number;
    }>;
  };
}

export interface StationItem {
  station_code: string;
  station_name: string;
  state?: string;
  zone?: string;
  latitude?: number;
  longitude?: number;
}

export interface ModelBenchmarkSummary {
  experiment_a_real?: {
    experiment: string;
    best_model: string;
    best_weighted_f1: number;
    benchmark_summary: Record<string, {
      model_name: string;
      accuracy: number;
      precision: number;
      recall: number;
      macro_f1: number;
      weighted_f1: number;
      critical_severity_recall: number;
      confusion_matrix: number[][];
      top_feature_importance: Record<string, number>;
    }>;
  };
  experiment_b_synthetic?: {
    experiment: string;
    disclaimer: string;
    best_model: string;
    best_weighted_f1: number;
    benchmark_summary: Record<string, {
      model_name: string;
      accuracy: number;
      macro_f1: number;
      weighted_f1: number;
      critical_severity_recall: number;
      confusion_matrix: number[][];
    }>;
  };
}

export interface EngineeringStandard {
  parameter_name: string;
  threshold_value: number;
  measurement_unit: string;
  applicable_speed_or_track_category: string;
  maintenance_classification: string;
  source_document: string;
  page_number: string;
  document_version_or_publication_date: string;
}
