import React, { useState } from 'react';
import { SeverityPredictionInput, SeverityPredictionResult } from '../types';
import { predictDefectSeverity } from '../services/api';
import {
  AlertCircle,
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  Gauge,
  Info,
  Layers,
  RotateCcw,
  ShieldAlert,
  Sparkles,
  Zap,
  Activity
} from 'lucide-react';

export const SeverityPredictionPage: React.FC = () => {
  const [form, setForm] = useState<SeverityPredictionInput>({
    defect_length_ft: 18.0,
    defect_amplitude_in: 1.65,
    fra_track_class: 4,
    freight_speed_limit_mph: 40.0,
    passenger_speed_limit_mph: 60.0,
    defect_type: 'XLEVEL',
    curve_spiral_tangent_code: 'C',
    track_code: '0',
    inspection_month: 6
  });

  const [result, setResult] = useState<SeverityPredictionResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const presets = [
    {
      name: 'Class 3 Critical: Curve Cross-Level UML',
      description: 'Severe cross-level variance on curve track requiring urgent speed restriction',
      badge: 'Critical (Red)',
      color: 'border-red-300 bg-red-50/50',
      values: {
        defect_length_ft: 22.0,
        defect_amplitude_in: 1.85,
        fra_track_class: 4,
        freight_speed_limit_mph: 45.0,
        passenger_speed_limit_mph: 65.0,
        defect_type: 'XLEVEL',
        curve_spiral_tangent_code: 'C',
        track_code: '0',
        inspection_month: 7
      }
    },
    {
      name: 'Class 2 Major: High-Speed Joint Dip',
      description: 'Accelerating foundation dip requiring priority machine tamping',
      badge: 'Major (Orange)',
      color: 'border-orange-300 bg-orange-50/50',
      values: {
        defect_length_ft: 15.0,
        defect_amplitude_in: 1.45,
        fra_track_class: 5,
        freight_speed_limit_mph: 50.0,
        passenger_speed_limit_mph: 80.0,
        defect_type: 'DIP',
        curve_spiral_tangent_code: 'S',
        track_code: '1',
        inspection_month: 10
      }
    },
    {
      name: 'Class 1 Minor: Tangent Surface Wear',
      description: 'Moderate longitudinal unevenness within scheduled tamping tolerance',
      badge: 'Minor (Yellow)',
      color: 'border-amber-300 bg-amber-50/50',
      values: {
        defect_length_ft: 12.0,
        defect_amplitude_in: 1.15,
        fra_track_class: 3,
        freight_speed_limit_mph: 30.0,
        passenger_speed_limit_mph: 40.0,
        defect_type: 'SURFACE',
        curve_spiral_tangent_code: 'T',
        track_code: '0',
        inspection_month: 3
      }
    },
    {
      name: 'Class 0 Normal: Routine Baseline Track',
      description: 'Small micro-deviation well within allowable maintenance thresholds',
      badge: 'Normal (Green)',
      color: 'border-emerald-300 bg-emerald-50/50',
      values: {
        defect_length_ft: 6.0,
        defect_amplitude_in: 0.60,
        fra_track_class: 4,
        freight_speed_limit_mph: 40.0,
        passenger_speed_limit_mph: 60.0,
        defect_type: 'SURFACE',
        curve_spiral_tangent_code: 'T',
        track_code: '0',
        inspection_month: 5
      }
    }
  ];

  const handlePredict = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await predictDefectSeverity(form);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  const applyPreset = (presetValues: SeverityPredictionInput) => {
    setForm(presetValues);
    setResult(null);
  };

  return (
    <div className="space-y-6">
      {/* Title Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded text-xs font-bold uppercase bg-blue-100 text-blue-800">
                INT395 Topic 20
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                Module 4 & 5 — AI Multiclass Defect Severity Classification & TreeSHAP
              </h2>
            </div>
            <p className="text-xs sm:text-sm text-slate-600 mt-1">
              Evaluates track geometry anomalies into 4 statutory severity tiers: Class 0 Normal (Green), Class 1 Minor (Yellow), Class 2 Major (Orange), and Class 3 Critical (Red).
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <span className="inline-flex items-center px-3 py-1 rounded-md text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              Champion: LightGBM (99.49% Macro-F1)
            </span>
          </div>
        </div>

        {/* Preset Strip */}
        <div className="mt-4 pt-3 border-t border-slate-100">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-600 uppercase tracking-wider">
              Quick Corridor Inspection Presets:
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
            {presets.map((p, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => applyPreset(p.values)}
                className={`text-left p-2.5 rounded-lg border text-xs transition-all hover:shadow-xs ${p.color}`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-slate-900 truncate">{p.name}</span>
                </div>
                <p className="text-[11px] text-slate-600 line-clamp-1">{p.description}</p>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Grid: Form Left, Output Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Form: Inspection Input */}
        <div className="lg:col-span-5 bg-white rounded-xl border border-slate-200 p-5 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
              <Gauge className="w-4 h-4 text-blue-600" />
              <span>Inspection Geometry Parameters</span>
            </h3>
            <button
              type="button"
              onClick={() => {
                setForm({
                  defect_length_ft: 18.0,
                  defect_amplitude_in: 1.65,
                  fra_track_class: 4,
                  freight_speed_limit_mph: 40.0,
                  passenger_speed_limit_mph: 60.0,
                  defect_type: 'XLEVEL',
                  curve_spiral_tangent_code: 'T',
                  track_code: '0',
                  inspection_month: 6
                });
                setResult(null);
              }}
              className="text-xs text-slate-500 hover:text-slate-800 flex items-center"
            >
              <RotateCcw className="w-3 h-3 mr-1" /> Reset
            </button>
          </div>

          <form onSubmit={handlePredict} className="space-y-4">
            {/* Defect Geometry Type */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Defect Geometry Type
              </label>
              <div className="grid grid-cols-3 gap-2">
                {['XLEVEL', 'SURFACE', 'DIP'].map((type) => (
                  <button
                    key={type}
                    type="button"
                    onClick={() => setForm({ ...form, defect_type: type })}
                    className={`py-1.5 px-3 rounded-lg text-xs font-semibold border transition-all ${
                      form.defect_type === type
                        ? 'bg-blue-600 text-white border-blue-600 shadow-xs'
                        : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                    }`}
                  >
                    {type === 'XLEVEL' ? 'Cross-Level' : type === 'SURFACE' ? 'Surface Profile' : 'Track Dip'}
                  </button>
                ))}
              </div>
            </div>

            {/* Amplitude & Length */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Defect Amplitude (inches)
                </label>
                <input
                  type="number"
                  step="0.05"
                  value={form.defect_amplitude_in}
                  onChange={(e) => setForm({ ...form, defect_amplitude_in: parseFloat(e.target.value) || 0 })}
                  className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 focus:outline-hidden focus:ring-1 focus:ring-blue-500"
                  required
                />
                <span className="text-[10px] text-slate-400 mt-0.5 block">
                  ~{(Math.abs(form.defect_amplitude_in) * 25.4).toFixed(1)} mm deviation
                </span>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Defect Length (feet)
                </label>
                <input
                  type="number"
                  step="0.5"
                  min="0.5"
                  value={form.defect_length_ft}
                  onChange={(e) => setForm({ ...form, defect_length_ft: parseFloat(e.target.value) || 1 })}
                  className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 focus:outline-hidden focus:ring-1 focus:ring-blue-500"
                  required
                />
                <span className="text-[10px] text-slate-400 mt-0.5 block">
                  ~{(form.defect_length_ft * 0.3048).toFixed(1)} meters longitudinal
                </span>
              </div>
            </div>

            {/* Alignment Code & Class */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Track Alignment Type
                </label>
                <select
                  value={form.curve_spiral_tangent_code}
                  onChange={(e) => setForm({ ...form, curve_spiral_tangent_code: e.target.value })}
                  className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 focus:outline-hidden focus:ring-1 focus:ring-blue-500 bg-white"
                >
                  <option value="T">Tangent (Straight Track)</option>
                  <option value="C">Curve Track (Super-elevation)</option>
                  <option value="S">Spiral (Transition Curve)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Track Class (FRA / IRPWM)
                </label>
                <select
                  value={form.fra_track_class}
                  onChange={(e) => setForm({ ...form, fra_track_class: parseInt(e.target.value) || 4 })}
                  className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 focus:outline-hidden focus:ring-1 focus:ring-blue-500 bg-white"
                >
                  <option value={1}>Class 1 (Freight ≤ 10 mph)</option>
                  <option value={2}>Class 2 (Freight ≤ 25 mph)</option>
                  <option value={3}>Class 3 (Freight ≤ 40 mph)</option>
                  <option value={4}>Class 4 (Freight ≤ 60 mph, Pass ≤ 80 mph)</option>
                  <option value={5}>Class 5 (Pass ≤ 90+ mph / High Speed)</option>
                </select>
              </div>
            </div>

            {/* Speed Limits */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Freight Speed (mph)
                </label>
                <input
                  type="number"
                  value={form.freight_speed_limit_mph}
                  onChange={(e) => setForm({ ...form, freight_speed_limit_mph: parseFloat(e.target.value) || 0 })}
                  className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 focus:outline-hidden focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Passenger Speed (mph)
                </label>
                <input
                  type="number"
                  value={form.passenger_speed_limit_mph}
                  onChange={(e) => setForm({ ...form, passenger_speed_limit_mph: parseFloat(e.target.value) || 0 })}
                  className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 focus:outline-hidden focus:ring-1 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 px-4 bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white font-semibold rounded-lg text-sm flex items-center justify-center space-x-2 transition-all shadow-xs"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                  <span>Computing Multiclass Inference...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-amber-400" />
                  <span>Classify Defect Severity</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Right Output: Detailed 4-Class Output & TreeSHAP */}
        <div className="lg:col-span-7 space-y-4">
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-xl flex items-start space-x-3 text-red-800 text-sm">
              <AlertCircle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
              <div>
                <h4 className="font-bold">Inference Error</h4>
                <p className="text-xs mt-0.5">{error}</p>
              </div>
            </div>
          )}

          {!result && !loading && (
            <div className="bg-white rounded-xl border border-slate-200 p-8 text-center shadow-xs flex flex-col items-center justify-center min-h-[420px]">
              <div className="w-12 h-12 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center mb-3">
                <Gauge className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-slate-900">Awaiting Track Inspection Parameters</h3>
              <p className="text-xs sm:text-sm text-slate-500 max-w-md mt-1 mb-4">
                Enter geometry car measurements on the left or click a preset to classify whether the anomaly is Normal (Green), Minor (Yellow), Major (Orange), or Critical (Red).
              </p>
              <button
                onClick={() => handlePredict()}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg text-xs font-semibold hover:bg-blue-700 transition-colors"
              >
                Run Default Inference
              </button>
            </div>
          )}

          {result && (
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs space-y-5">
              {/* Result Banner */}
              <div
                className="p-4 rounded-xl border flex items-start justify-between"
                style={{
                  backgroundColor: result.severity_code === 3 ? '#fef2f2' : (result.severity_code === 2 ? '#fff7ed' : (result.severity_code === 1 ? '#fefce8' : '#f0fdf4')),
                  borderColor: result.severity_code === 3 ? '#fecaca' : (result.severity_code === 2 ? '#ffedd5' : (result.severity_code === 1 ? '#fef08a' : '#bbf7d0')),
                }}
              >
                <div className="flex items-start space-x-3">
                  {result.severity_code === 3 ? (
                    <ShieldAlert className="w-7 h-7 text-red-600 shrink-0 mt-0.5" />
                  ) : (
                    <CheckCircle2 className="w-7 h-7 shrink-0 mt-0.5" style={{ color: result.severity_color || '#10b981' }} />
                  )}
                  <div>
                    <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-white/80 border">
                      {result.urgency_level}
                    </span>
                    <h3 className="text-base font-bold mt-1 text-slate-900">{result.severity_label}</h3>
                    <p className="text-xs mt-1 text-slate-700">{result.suggested_action}</p>
                  </div>
                </div>

                <div className="text-right shrink-0 ml-4">
                  <span className="text-2xl font-black text-slate-900">{Math.round(result.confidence_score * 100)}%</span>
                  <span className="text-[10px] block font-semibold text-slate-500 uppercase">Confidence</span>
                  {result.uncertainty_score !== undefined && (
                    <span className="text-[9px] text-slate-400 font-mono block">Uncertainty: {result.uncertainty_score}</span>
                  )}
                </div>
              </div>

              {/* 4-Class Calibrated Probabilities */}
              <div>
                <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                  Calibrated 4-Class Probabilities (INT395 Architecture)
                </h4>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {[
                    { label: "Class 0 Normal", key: "Normal_Class_0", color: "#10b981", bg: "bg-emerald-500" },
                    { label: "Class 1 Minor", key: "Minor_Class_1", color: "#f59e0b", bg: "bg-amber-500" },
                    { label: "Class 2 Major", key: "Major_Class_2", color: "#f97316", bg: "bg-orange-500" },
                    { label: "Class 3 Critical", key: "Critical_Class_3", color: "#ef4444", bg: "bg-red-600" },
                  ].map((cls, cidx) => {
                    const prob = result.probabilities[cls.key] || 0;
                    return (
                      <div key={cidx} className="p-2.5 rounded-lg border border-slate-100 bg-slate-50 space-y-1">
                        <div className="flex justify-between text-[11px] font-semibold text-slate-700">
                          <span>{cls.label}</span>
                          <span className="font-bold">{(prob * 100).toFixed(1)}%</span>
                        </div>
                        <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                          <div className={`h-full ${cls.bg}`} style={{ width: `${prob * 100}%` }} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* TreeSHAP Feature Attribution */}
              {result.shap_attributions && result.shap_attributions.length > 0 && (
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center space-x-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-blue-600" />
                      <span>Native TreeSHAP Game-Theoretic Feature Attributions</span>
                    </h4>
                    <span className="text-[10px] text-slate-500 font-mono">Shapley Additive Contributions</span>
                  </div>
                  <div className="space-y-2 bg-slate-50 p-3 rounded-xl border border-slate-200">
                    {result.shap_attributions.map((attr, idx) => (
                      <div key={idx} className="text-xs">
                        <div className="flex justify-between items-center mb-1">
                          <span className="font-medium text-slate-800">{attr.feature_label}</span>
                          <div className="flex items-center space-x-2 font-mono">
                            <span className={attr.contribution_direction === 'INCREASES_RISK' ? 'text-red-600 font-bold' : 'text-emerald-600 font-bold'}>
                              {attr.contribution_direction === 'INCREASES_RISK' ? '+' : '-'}{Math.abs(attr.shap_value).toFixed(3)}
                            </span>
                            <span className="text-slate-400">({attr.importance_pct}%)</span>
                          </div>
                        </div>
                        <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden flex">
                          <div
                            className={`h-full ${attr.contribution_direction === 'INCREASES_RISK' ? 'bg-red-500' : 'bg-emerald-500'}`}
                            style={{ width: `${attr.importance_pct}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Standards Comparison */}
              <div>
                <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                  IRPWM 2020 Statutory Standards Benchmarking
                </h4>
                <div className="space-y-2">
                  {result.standards_comparison.map((std, idx) => (
                    <div key={idx} className="p-2.5 rounded-lg border border-slate-200 bg-slate-50 text-xs flex items-center justify-between">
                      <div>
                        <span className="font-bold text-slate-900">{std.parameter}</span>
                        <div className="text-[11px] text-slate-500">{std.irpwm_standard}</div>
                      </div>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        std.status.includes('EXCEEDS') ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-700'
                      }`}>
                        {std.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
