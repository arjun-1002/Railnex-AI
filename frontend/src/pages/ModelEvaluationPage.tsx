import React, { useEffect, useState } from 'react';
import { fetchModelEvaluation } from '../services/api';
import {
  AlertTriangle,
  BarChart2,
  CheckCircle2,
  Layers,
  ShieldCheck,
  Award,
  Clock,
  Crosshair,
  TrendingUp
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from 'recharts';

export const ModelEvaluationPage: React.FC = () => {
  const [data, setData] = useState<any | null>(null);
  const [activeTab, setActiveTab] = useState<'INT395' | 'A' | 'B'>('INT395');
  const [selectedModel, setSelectedModel] = useState<string>('LightGBM');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchModelEvaluation()
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-8 h-8 border-3 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-medium text-slate-600">Loading machine learning benchmark metrics...</p>
        </div>
      </div>
    );
  }

  const multiclassModels = data.multiclass_7_models_benchmark?.models || {};
  const expA = data.experiment_a_real?.benchmark_summary || {};
  const expB = data.experiment_b_synthetic?.benchmark_summary || {};

  const activeModelDetails = multiclassModels[selectedModel] || multiclassModels['LightGBM'] || null;

  // Chart data comparing Macro-F1 across the 7 models
  const comparisonBarData = Object.entries(multiclassModels).map(([name, m]: [string, any]) => ({
    name: name.replace(" Champion", "").replace(" Classifier", ""),
    macro_f1: Math.round(m.macro_f1 * 1000) / 10,
    critical_recall: Math.round(m.critical_recall * 1000) / 10,
    accuracy: Math.round(m.accuracy * 1000) / 10
  })).sort((a, b) => b.macro_f1 - a.macro_f1);

  return (
    <div className="space-y-6 pb-12">
      {/* Title & Guidance Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded text-xs font-bold uppercase bg-blue-100 text-blue-800">
                INT395 Topic 20
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                Module 15 — Supervised Machine Learning Benchmark Dashboard
              </h2>
            </div>
            <p className="text-xs sm:text-sm text-slate-600 mt-1">
              Comprehensive academic evaluation of 7 classifiers on 23,847 real geometry records using strict chronological out-of-time testing (split boundary: 2012-01-01).
            </p>
          </div>

          {/* Tab Switcher */}
          <div className="flex rounded-lg border border-slate-200 bg-slate-100 p-1 shrink-0">
            <button
              onClick={() => setActiveTab('INT395')}
              className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all ${
                activeTab === 'INT395'
                  ? 'bg-white text-blue-600 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              INT395 7-Model Benchmark
            </button>
            <button
              onClick={() => setActiveTab('A')}
              className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all ${
                activeTab === 'A'
                  ? 'bg-white text-blue-600 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Experiment A (Binary Real)
            </button>
            <button
              onClick={() => setActiveTab('B')}
              className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all ${
                activeTab === 'B'
                  ? 'bg-white text-blue-600 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Experiment B (Synthetic Leakage)
            </button>
          </div>
        </div>

        {/* Banner Context */}
        <div className="mt-4 pt-3 border-t border-slate-100 text-xs">
          {activeTab === 'INT395' && (
            <div className="flex items-center space-x-2 text-blue-800 bg-blue-50 px-3 py-2 rounded-lg border border-blue-200">
              <Award className="w-4 h-4 text-blue-600 shrink-0" />
              <span>
                <strong>Academic Primary Metric:</strong> <strong>Macro-F1</strong> evaluates unweighted balance across all 4 severity tiers (Normal, Minor, Major, Critical). LightGBM achieves Champion status with <strong>99.49% Macro-F1</strong> and <strong>99.52% Critical (Class 3) Recall</strong> (missing only 2 out of 417 critical defects).
              </span>
            </div>
          )}
          {activeTab === 'A' && (
            <div className="flex items-center space-x-2 text-emerald-800 bg-emerald-50 px-3 py-2 rounded-lg border border-emerald-200">
              <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
              <span>
                <strong>Experiment A Protocol:</strong> 17,283 records (2007–2011) training set vs 6,564 records (2012–2013) out-of-time test set.
              </span>
            </div>
          )}
          {activeTab === 'B' && (
            <div className="flex items-center space-x-2 text-amber-800 bg-amber-50 px-3 py-2 rounded-lg border border-amber-200">
              <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
              <span>
                <strong>Target Leakage Audit:</strong> Demonstrates that synthetic benchmarks with post-hoc risk indices artificially boast 100% accuracy ($r = 0.887$). Pruning leakage features drops accuracy to 70.52%.
              </span>
            </div>
          )}
        </div>
      </div>

      {/* INT395 7-Model Benchmark View */}
      {activeTab === 'INT395' && (
        <div className="space-y-6">
          {/* 7-Model Table */}
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900 tracking-tight mb-1">
              Comparative Multi-Algorithm Performance Matrix (7 Competing Models)
            </h3>
            <p className="text-xs text-slate-500 mb-4">
              Sorted by Primary Evaluation Metric (Macro-F1). Click any model to inspect its 4x4 Confusion Matrix.
            </p>

            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200 text-xs">
                <thead className="bg-slate-50 text-slate-700 font-semibold">
                  <tr>
                    <th className="px-3.5 py-3 text-left">Algorithm</th>
                    <th className="px-3.5 py-3 text-right">Accuracy</th>
                    <th className="px-3.5 py-3 text-right text-blue-600 font-bold">Macro-F1 (PRIMARY)</th>
                    <th className="px-3.5 py-3 text-right">Weighted-F1</th>
                    <th className="px-3.5 py-3 text-right text-red-600 font-bold">Critical (Class 3) Recall</th>
                    <th className="px-3.5 py-3 text-right">Critical False Negatives</th>
                    <th className="px-3.5 py-3 text-right">ROC-AUC (OVR)</th>
                    <th className="px-3.5 py-3 text-right">Fit Time</th>
                    <th className="px-3.5 py-3 text-center">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 bg-white">
                  {Object.entries(multiclassModels).map(([name, m]: [string, any]) => {
                    const isSelected = selectedModel === name;
                    const isChampion = name.includes('LightGBM');
                    return (
                      <tr
                        key={name}
                        onClick={() => setSelectedModel(name)}
                        className={`cursor-pointer transition-colors ${
                          isSelected ? 'bg-blue-50/70 font-medium' : 'hover:bg-slate-50'
                        }`}
                      >
                        <td className="px-3.5 py-3 font-semibold text-slate-900 flex items-center space-x-2">
                          <span>{name}</span>
                          {isChampion && (
                            <span className="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 text-[10px] font-bold">
                              CHAMPION
                            </span>
                          )}
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono font-bold text-slate-900">
                          {(m.accuracy * 100).toFixed(2)}%
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono font-bold text-blue-600">
                          {(m.macro_f1 * 100).toFixed(2)}%
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono text-slate-700">
                          {(m.weighted_f1 * 100).toFixed(2)}%
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono font-extrabold text-red-600">
                          {(m.critical_recall * 100).toFixed(2)}%
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono text-slate-700">
                          {m.critical_false_negatives} / {m.critical_total}
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono text-slate-700">
                          {m.roc_auc_ovr ? m.roc_auc_ovr.toFixed(4) : "N/A"}
                        </td>
                        <td className="px-3.5 py-3 text-right font-mono text-slate-500">
                          {m.fit_time_seconds}s
                        </td>
                        <td className="px-3.5 py-3 text-center">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            isChampion ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600'
                          }`}>
                            {isChampion ? 'CHAMPION' : 'BENCHMARK'}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Confusion Matrix & Macro-F1 Bar Chart */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Macro-F1 Comparison Chart */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
              <h4 className="text-sm font-bold text-slate-900 mb-1">
                Macro-F1 vs Critical Recall Comparison (7 Models)
              </h4>
              <p className="text-xs text-slate-500 mb-4">
                Primary INT395 academic metric across all 7 evaluated architectures
              </p>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={comparisonBarData} margin={{ top: 10, right: 10, left: -10, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                    <XAxis dataKey="name" tick={{ fontSize: 10 }} interval={0} angle={-20} textAnchor="end" />
                    <YAxis domain={[80, 100]} tick={{ fontSize: 10 }} />
                    <Tooltip />
                    <Bar dataKey="macro_f1" name="Macro-F1 (%)" fill="#2563eb" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="critical_recall" name="Critical Recall (%)" fill="#ef4444" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Selected Model 4x4 Confusion Matrix */}
            {activeModelDetails && (
              <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-sm font-bold text-slate-900">
                      Confusion Matrix: {selectedModel}
                    </h4>
                    <p className="text-xs text-slate-500">
                      Out-of-time evaluation test partition (6,564 records)
                    </p>
                  </div>
                  <span className="text-xs font-mono font-bold px-2.5 py-1 rounded bg-blue-50 text-blue-700">
                    Macro-F1: {(activeModelDetails.macro_f1 * 100).toFixed(2)}%
                  </span>
                </div>

                <div className="overflow-x-auto">
                  <table className="min-w-full text-center text-xs font-mono">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-500">
                        <th className="py-2 text-left font-sans">Actual \ Predicted</th>
                        <th className="py-2 bg-emerald-50 text-emerald-800">Normal (0)</th>
                        <th className="py-2 bg-amber-50 text-amber-800">Minor (1)</th>
                        <th className="py-2 bg-orange-50 text-orange-800">Major (2)</th>
                        <th className="py-2 bg-red-50 text-red-800">Critical (3)</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {activeModelDetails.confusion_matrix.map((row: number[], ridx: number) => {
                        const labels = ["Normal (0)", "Minor (1)", "Major (2)", "Critical (3)"];
                        return (
                          <tr key={ridx} className="hover:bg-slate-50">
                            <td className="py-2 text-left font-sans font-semibold text-slate-700">{labels[ridx]}</td>
                            {row.map((val: number, cidx: number) => {
                              const isDiagonal = ridx === cidx;
                              return (
                                <td key={cidx} className={`py-2 ${
                                  isDiagonal ? 'font-extrabold text-blue-700 bg-blue-50/50' : (val > 0 && ridx === 3 ? 'font-bold text-red-600 bg-red-50' : 'text-slate-500')
                                }`}>
                                  {val}
                                </td>
                              );
                            })}
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>

                <div className="text-[11px] text-slate-500 flex items-center justify-between pt-2 border-t border-slate-100">
                  <span>Critical False Negatives: <strong className="text-red-600">{activeModelDetails.critical_false_negatives}</strong> / {activeModelDetails.critical_total}</span>
                  <span>Fit Duration: <strong>{activeModelDetails.fit_time_seconds}s</strong></span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Experiment A & B Views */}
      {activeTab !== 'INT395' && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
          <h3 className="text-sm font-bold text-slate-900 mb-2">
            Historical Binary Experiments (Experiment {activeTab})
          </h3>
          <p className="text-xs text-slate-600">
            {activeTab === 'A'
              ? "Observational geometry car defect classification benchmark (RED vs YELLOW) achieving 99.1% F1."
              : "Demonstration of target leakage in Hugging Face dataset (risk_score correlation r = 0.887)."}
          </p>
        </div>
      )}
    </div>
  );
};
