export type TabType = 
  | 'overview' 
  | 'severity_prediction' 
  | 'maintenance_priority' 
  | 'track_analysis' 
  | 'cv_inspection'
  | 'usfd_analysis'
  | 'weather_intelligence'
  | 'network_map' 
  | 'model_evaluation' 
  | 'ai_assistant'
  | 'data_explorer' 
  | 'settings';

export interface OverviewMetrics {
  summary_cards: {
    total_inspection_records: number;
    monitored_line_segments: number;
    critical_defects_count?: number;
    critical_red_tags?: number;
    planned_yellow_tags?: number;
    active_railway_stations: number;
    operational_zones_tracked?: number;
    railway_zones_tracked?: number;
    operating_divisions?: number;
    model_champion: string;
    champion_f1_score?: number;
    champion_macro_f1?: number;
    champion_critical_recall?: number;
    weather_buckling_alerts?: number;
    weather_flood_alerts?: number;
  };
  severity_distribution: Array<{
    name: string;
    count: number;
    percentage: number;
    color: string;
    code?: number;
  }>;
  multiclass_severity_distribution?: Array<{
    name: string;
    code: number;
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
  cag_derailment_causation?: any[];
  datasets_manifest?: any[];
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

export interface ShapAttribution {
  feature_name: string;
  feature_label: string;
  shap_value: number;
  contribution_direction: 'INCREASES_RISK' | 'REDUCES_RISK';
  importance_pct: number;
}

export interface SeverityPredictionResult {
  predicted_class: string;
  severity_code?: number;
  severity_label: string;
  urgency_level: string;
  confidence_score: number;
  uncertainty_score?: number;
  probabilities: {
    [key: string]: number;
  };
  severity_color?: string;
  contributing_factors: ContributingFactor[];
  standards_comparison: StandardsComparison[];
  shap_attributions?: ShapAttribution[];
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
  priority_tier: string;
  suggested_action: string;
  inspection_date?: string;
  urgency_color?: string;
}

export interface TrackDeteriorationData {
  top_deteriorating_segments: Array<{
    line_segment_id: number;
    total_inspections: number;
    recurring_defects_count: number;
    red_tags?: number;
    red_tag_ratio?: number;
    avg_amplitude: number;
    max_amplitude: number;
    deterioration_trend: string;
    urgency_rank: number;
    monthly_degradation_rate_mm: number;
    projected_days_to_uml: number;
    prognostic_status: string;
    remaining_tonnage_mgt: number;
    last_inspection_date?: string;
  }>;
  longitudinal_sample_segment: {
    line_segment_id: number;
    history?: Array<{
      quarter: string;
      defect_count: number;
      red_count: number;
    }>;
    history_points: Array<{
      inspection_date: string;
      milepost: number;
      amplitude_mm: number;
      defect_type: string;
      severity_tag: string;
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

export interface EngineeringStandard {
  parameter_name: string;
  threshold_value: number;
  measurement_unit: string;
  applicable_speed_or_track_category: string;
  maintenance_classification: string;
  source_document: string;
  page_number?: number;
  document_version_or_publication_date?: string;
}

export interface CvDefectPredictionResult {
  image_filename: string;
  detected_class: 'DEFECTIVE' | 'HEALTHY';
  confidence: number;
  defect_subtype: string;
  annotated_bounding_box?: {
    ymin?: number;
    xmin?: number;
    ymax?: number;
    xmax?: number;
  };
  engineering_recommendation: string;
  disclaimer: string;
}

export interface AssistantChatResult {
  response_text: string;
  referenced_standards: string[];
  suggested_followups: string[];
  timestamp: string;
}
