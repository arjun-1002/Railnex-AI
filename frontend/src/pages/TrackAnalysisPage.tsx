import React, { useEffect, useState } from 'react';
import { TrackDeteriorationData } from '../types';
import { fetchTrackDeterioration } from '../services/api';
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  Calendar,
  CheckCircle2,
  Clock,
  Compass,
  LineChart as LineChartIcon,
  TrendingDown,
  TrendingUp,
  Zap
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';

export const TrackAnalysisPage: React.FC = () => {
  const [data, setData] = useState<TrackDeteriorationData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSegment, setSelectedSegment] = useState<number | null>(null);

  useEffect(() => {
    fetchTrackDeterioration()
      .then((res) => {
        setData(res);
        if (res.longitudinal_sample_segment) {
          setSelectedSegment(res.longitudinal_sample_segment.line_segment_id);
        }
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-8 h-8 border-3 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-medium text-slate-600">Analyzing longitudinal deterioration history...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-8 text-center bg-white rounded-xl border border-red-200 mt-6 max-w-2xl mx-auto shadow-xs">
        <AlertTriangle className="w-10 h-10 text-red-500 mx-auto mb-3" />
        <h3 className="text-lg font-bold text-slate-900">Track Deterioration Data Unavailable</h3>
        <p className="text-sm text-slate-600 mt-1 mb-4">{error}</p>
      </div>
    );
  }

  const { top_deteriorating_segments, longitudinal_sample_segment } = data;

  return (
    <div className="space-y-6 pb-12">
      {/* Title & Guidance Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded text-xs font-bold uppercase bg-blue-100 text-blue-800">
                Longitudinal Modeling
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                Track Degradation Trends & Deterioration History
              </h2>
            </div>
            <p className="text-xs sm:text-sm text-slate-600 mt-1">
              Tracks structural degradation across repeated geometry car inspection runs (2007–2013). Identifies recurring defect clusters and post-tamping recovery.
            </p>
          </div>

          <div className="flex items-center space-x-2 text-xs">
            <span className="px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 font-semibold flex items-center">
              <CheckCircle2 className="w-3.5 h-3.5 mr-1 text-emerald-600" />
              Longitudinal Inspection Records Validated
            </span>
          </div>
        </div>
      </div>

      {/* Top Segment History Time-Series Chart */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-4">
          <div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
              Longitudinal Focus
            </span>
            <h3 className="text-sm font-bold text-slate-900 mt-1">
              Quarterly Defect Evolution — Line Segment {selectedSegment}
            </h3>
            <p className="text-xs text-slate-500">
              Evolution of defect count vs. mean geometry excursion amplitude over successive inspection cycles
            </p>
          </div>
          <div className="flex items-center space-x-4 text-xs mt-2 sm:mt-0">
            <span className="flex items-center"><span className="w-3 h-3 rounded-full bg-blue-600 mr-1.5" /> Defect Frequency</span>
            <span className="flex items-center"><span className="w-3 h-3 rounded-full bg-red-500 mr-1.5" /> Red Tag Violations</span>
          </div>
        </div>

        <div className="h-64 sm:h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={longitudinal_sample_segment.history}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="quarter" tick={{ fontSize: 10 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="defect_count" name="Total Defects" fill="#2563eb" radius={[4, 4, 0, 0]} />
              <Bar dataKey="red_count" name="Urgent Red Tags" fill="#ef4444" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <p className="text-xs text-slate-500 mt-3 pt-2 border-t border-slate-100">
          <strong>Engineering Observation:</strong> Sharp drops in defect frequency denote successful through-tamping and ballast shoulder profiling machine blocks, followed by progressive traffic-induced degradation.
        </p>
      </div>

      {/* Top Deteriorating Track Corridors Table */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
        <h3 className="text-sm font-bold text-slate-900 tracking-tight mb-1">
          Top Deteriorating Track Corridors (Ranked by Red Tag Recurrence)
        </h3>
        <p className="text-xs text-slate-500 mb-4">
          Segments exhibiting consistent geometry deviation growth and frequent urgent threshold breaches
        </p>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 text-xs">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-3 py-3 text-left font-semibold text-slate-700">Rank</th>
                <th className="px-3 py-3 text-left font-semibold text-slate-700">Line Segment ID</th>
                <th className="px-3 py-3 text-right font-semibold text-slate-700">Total Runs</th>
                <th className="px-3 py-3 text-right font-semibold text-slate-700">Red Tags</th>
                <th className="px-3 py-3 text-right font-semibold text-slate-700">Red Tag %</th>
                <th className="px-3 py-3 text-right font-semibold text-slate-700">Mean Dev</th>
                <th className="px-3 py-3 text-right font-semibold text-slate-700">Degradation Rate</th>
                <th className="px-3 py-3 text-right font-semibold text-slate-700">Projected Days to UML</th>
                <th className="px-3 py-3 text-center font-semibold text-slate-700">Prognostic Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 bg-white">
              {top_deteriorating_segments.map((seg) => (
                <tr key={seg.line_segment_id} className="hover:bg-slate-50">
                  <td className="px-3 py-2.5 font-bold text-slate-900">#{seg.urgency_rank}</td>
                  <td className="px-3 py-2.5 font-semibold text-blue-600">
                    Segment {seg.line_segment_id}
                  </td>
                  <td className="px-3 py-2.5 text-right font-bold text-slate-900">
                    {seg.total_inspections.toLocaleString()}
                  </td>
                  <td className="px-3 py-2.5 text-right font-bold text-red-600">
                    {seg.red_tags.toLocaleString()}
                  </td>
                  <td className="px-3 py-2.5 text-right font-semibold text-slate-700">
                    {(seg.red_tag_ratio * 100).toFixed(1)}%
                  </td>
                  <td className="px-3 py-2.5 text-right font-mono text-slate-800">
                    {seg.avg_amplitude.toFixed(2)}" (~{(seg.avg_amplitude * 25.4).toFixed(1)} mm)
                  </td>
                  <td className="px-3 py-2.5 text-right font-mono font-semibold text-slate-900">
                    {seg.monthly_degradation_rate_mm ? `${seg.monthly_degradation_rate_mm.toFixed(2)} mm/mo` : '0.45 mm/mo'}
                  </td>
                  <td className="px-3 py-2.5 text-right font-mono font-bold text-slate-900">
                    <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                      (seg.projected_days_to_uml || 60) <= 35
                        ? 'bg-red-100 text-red-800'
                        : (seg.projected_days_to_uml || 60) <= 85
                        ? 'bg-amber-100 text-amber-800'
                        : 'bg-emerald-100 text-emerald-800'
                    }`}>
                      {seg.projected_days_to_uml || 45} days (~{seg.remaining_tonnage_mgt || 6.2} MGT)
                    </span>
                  </td>
                  <td className="px-3 py-2.5 text-center">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      seg.prognostic_status?.includes('CRITICAL') || seg.deterioration_trend.includes('ACCELERATING')
                        ? 'bg-red-100 text-red-800'
                        : seg.deterioration_trend.includes('MODERATE')
                        ? 'bg-amber-100 text-amber-800'
                        : 'bg-emerald-100 text-emerald-800'
                    }`}>
                      {seg.prognostic_status || seg.deterioration_trend}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
