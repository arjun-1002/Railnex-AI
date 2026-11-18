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
  Zap
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
      name: 'Severe Curve Cross-Level Exceedance',
      description: 'Dangerous cross-level variance on curve track requiring urgent speed restriction',
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
      name: 'Planned Surface Profile Wear',
      description: 'Moderate longitudinal unevenness within scheduled tamping tolerance',
      values: {
        defect_length_ft: 12.0,
        defect_amplitude_in: 0.85,
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
      name: 'High-Speed Track Dip Anomaly',
      description: 'Dip perturbation on high-speed passenger mainline corridor',
      values: {
        defect_length_ft: 15.0,
        defect_amplitude_in: -1.45,
        fra_track_class: 5,
        freight_speed_limit_mph: 50.0,
        passenger_speed_limit_mph: 80.0,
        defect_type: 'DIP',
        curve_spiral_tangent_code: 'S',
        track_code: '1',
        inspection_month: 10
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
    <div className="space-y-6 pb-12">
      {/* Page Title & Context Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded text-xs font-bold uppercase bg-blue-100 text-blue-800">
                Machine Learning Inference
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                Supervised Track Defect Severity Classification
              </h2>
            </div>
            <p className="text-xs sm:text-sm text-slate-600 mt-1">
              Evaluates track geometry inspection parameters using our trained XGBoost champion model. Estimates safety risk against IRPWM 2020 / FRA maintenance tolerances.
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-500 font-medium">Quick Presets:</span>
            {presets.map((preset, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => applyPreset(preset.values)}
                className="px-2.5 py-1 text-xs font-medium rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700 transition-colors"
                title={preset.description}
              >
                {preset.name.split(' ')[0]} {preset.name.split(' ')[1]}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Form: Parameter Inputs */}
        <div className="lg:col-span-5 bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
            <h3 className="text-sm font-bold text-slate-900">Inspection Measurements Input</h3>
            <button
              type="button"
              onClick={() => {
                setForm({
                  defect_length_ft: 15.0,
                  defect_amplitude_in: 1.0,
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
            {/* Defect Type & Track Geometry Channel */}
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
                  className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                  className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
                <span className="text-[10px] text-slate-400 mt-0.5 block">
                  ~{(form.defect_length_ft * 0.3048).toFixed(1)} meters longitudinal
                </span>
              </div>
            </div>

            {/* Track Alignment Code & FRA Class */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Track Alignment Type
                </label>
                <select
                  value={form.curve_spiral_tangent_code}
                  onChange={(e) => setForm({ ...form, curve_spiral_tangent_code: e.target.value })}
                  className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
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
                  className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                >
                  <option value={1}>Class 1 (Freight &le; 10 mph)</option>
                  <option value={2}>Class 2 (Freight &le; 25 mph)</option>
                  <option value={3}>Class 3 (Freight &le; 40 mph)</option>
                  <option value={4}>Class 4 (Freight &le; 60 mph, Pass &le; 80 mph)</option>
                  <option value={5}>Class 5 (Pass &le; 90+ mph / High Speed)</option>
                </select>
              </div>
            </div>

            {/* Operating Speeds */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Freight Speed (mph)
                </label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={form.freight_speed_limit_mph}
                  onChange={(e) => setForm({ ...form, freight_speed_limit_mph: parseFloat(e.target.value) || 0 })}
                  className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Passenger Speed (mph)
                </label>
                <input
                  type="number"
                  min="0"
                  max="140"
                  value={form.passenger_speed_limit_mph}
                  onChange={(e) => setForm({ ...form, passenger_speed_limit_mph: parseFloat(e.target.value) || 0 })}
                  className="w-full px-3 py-1.5 text-sm rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 px-4 bg-slate-900 text-white rounded-lg font-semibold text-sm hover:bg-slate-800 transition-all flex items-center justify-center space-x-2 shadow-xs disabled:opacity-50"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                  <span>Computing Severity Inference...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-amber-400" />
                  <span>Evaluate Track Defect Severity</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Right Output: Detailed Prediction & Contributing Evidence */}
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
                Enter geometry car measurements on the left or select a preset to evaluate whether the anomaly requires immediate emergency speed restrictions or routine planned maintenance.
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
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs space-y-5 animate-in fade-in duration-200">
              {/* Result Banner */}
              <div className={`p-4 rounded-xl border flex items-start justify-between ${
                result.predicted_class === 'RED'
                  ? 'bg-red-50/80 border-red-200 text-red-900'
                  : 'bg-amber-50/80 border-amber-200 text-amber-900'
              }`}>
                <div className="flex items-start space-x-3">
                  {result.predicted_class === 'RED' ? (
                    <ShieldAlert className="w-7 h-7 text-red-600 shrink-0 mt-0.5" />
                  ) : (
                    <CheckCircle2 className="w-7 h-7 text-amber-600 shrink-0 mt-0.5" />
                  )}
                  <div>
                    <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-white/80 border">
                      {result.urgency_level}
                    </span>
                    <h3 className="text-base font-bold mt-1">{result.severity_label}</h3>
                    <p className="text-xs mt-1 text-slate-700">{result.suggested_action}</p>
                  </div>
                </div>

                <div className="text-right shrink-0 ml-4">
                  <span className="text-2xl font-black">{Math.round(result.confidence_score * 100)}%</span>
                  <span className="text-[10px] block font-semibold text-slate-500 uppercase">Model Confidence</span>
                </div>
              </div>

              {/* Calibrated Probability Breakdown */}
              <div>
                <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                  Calibrated Class Probabilities
                </h4>
                <div className="space-y-1.5">
                  <div>
                    <div className="flex justify-between text-xs font-medium mb-1">
                      <span className="text-amber-800">Yellow Tag — Planned Maintenance (PML / NBML)</span>
                      <span className="font-bold">{(result.probabilities.Yellow_Tag_Planned * 100).toFixed(1)}%</span>
                    </div>
                    <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-amber-500 transition-all duration-500"
                        style={{ width: `${result.probabilities.Yellow_Tag_Planned * 100}%` }}
                      />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-xs font-medium mb-1">
                      <span className="text-red-800">Red Tag — Urgent Action Required (FRA Exceedance / UML)</span>
                      <span className="font-bold">{(result.probabilities.Red_Tag_Urgent * 100).toFixed(1)}%</span>
                    </div>
                    <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-red-600 transition-all duration-500"
                        style={{ width: `${result.probabilities.Red_Tag_Urgent * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Explainable Contributing Factors */}
              <div>
                <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                  Important Contributing Factors
                </h4>
                <div className="space-y-2">
                  {result.contributing_factors.map((factor, idx) => (
                    <div key={idx} className="p-2.5 rounded-lg bg-slate-50 border border-slate-100 text-xs flex items-start justify-between">
                      <div>
                        <span className="font-bold text-slate-900">{factor.feature}: </span>
                        <span className="text-slate-600">{factor.description}</span>
                      </div>
                      <span className="ml-2 font-mono text-[10px] font-bold px-1.5 py-0.5 rounded bg-slate-200 text-slate-800 shrink-0">
                        {factor.impact}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Comparison with Indian Railways IRPWM Standards */}
              <div>
                <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                  IRPWM 2020 Threshold Benchmarking
                </h4>
                <div className="border border-slate-200 rounded-lg overflow-hidden text-xs">
                  <table className="min-w-full divide-y divide-slate-100">
                    <thead className="bg-slate-50 font-semibold text-slate-700">
                      <tr>
                        <th className="px-3 py-1.5 text-left">Parameter</th>
                        <th className="px-3 py-1.5 text-left">Inspection Value</th>
                        <th className="px-3 py-1.5 text-left">IRPWM 2020 Standard</th>
                        <th className="px-3 py-1.5 text-right">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 bg-white">
                      {result.standards_comparison.map((row, idx) => (
                        <tr key={idx}>
                          <td className="px-3 py-1.5 font-medium text-slate-900">{row.parameter}</td>
                          <td className="px-3 py-1.5 text-slate-700 font-mono">{row.recorded_value}</td>
                          <td className="px-3 py-1.5 text-slate-600">{row.irpwm_standard}</td>
                          <td className="px-3 py-1.5 text-right">
                            <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                              row.status.includes('EXCEEDS')
                                ? 'bg-red-100 text-red-800'
                                : 'bg-emerald-100 text-emerald-800'
                            }`}>
                              {row.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Legal / Engineering Limitations Disclaimer */}
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-[11px] text-slate-500 leading-relaxed flex items-start space-x-2">
                <Info className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
                <span>{result.limitations_disclaimer}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
