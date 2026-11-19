import React, { useEffect, useState } from 'react';
import { TrackDeteriorationData } from '../types';
import { fetchTrackDeterioration, simulateTrackDegradation } from '../services/api';
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
  Zap,
  Sliders,
  CloudRain,
  ShieldAlert,
  Sparkles
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
  Legend,
  ReferenceLine
} from 'recharts';

export const TrackAnalysisPage: React.FC = () => {
  const [data, setData] = useState<TrackDeteriorationData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSegment, setSelectedSegment] = useState<number | null>(null);

  // What-If Simulation State
  const [simAxleLoad, setSimAxleLoad] = useState<number>(22.82);
  const [simTrafficMgt, setSimTrafficMgt] = useState<number>(35.0);
  const [simDeferredDays, setSimDeferredDays] = useState<number>(0);
  const [simMonsoonRain, setSimMonsoonRain] = useState<number>(0);
  const [simBallast, setSimBallast] = useState<string>('MODERATE');
  const [simResult, setSimResult] = useState<any | null>(null);

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

  useEffect(() => {
    simulateTrackDegradation({
      line_segment_id: selectedSegment || 10103100,
      baseline_amplitude_mm: 8.5,
      axle_load_tonnes: simAxleLoad,
      traffic_mgt_annual: simTrafficMgt,
      deferred_maintenance_days: simDeferredDays,
      monsoon_rainfall_mm: simMonsoonRain,
      ballast_condition: simBallast
    })
      .then((res) => setSimResult(res))
      .catch((err) => console.error(err));
  }, [selectedSegment, simAxleLoad, simTrafficMgt, simDeferredDays, simMonsoonRain, simBallast]);

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

      {/* Interactive What-If Operational Sensitivity & Climate Resilience Sandbox */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-100 gap-2">
          <div className="flex items-center space-x-2">
            <Sliders className="w-5 h-5 text-blue-600" />
            <div>
              <h3 className="text-sm font-bold text-slate-900">
                Interactive What-If Operational Sensitivity & Climate Resilience Sandbox
              </h3>
              <p className="text-xs text-slate-500">
                Simulate how heavy axle loads, deferred tamping intervals, and extreme monsoon precipitation alter track degradation velocity
              </p>
            </div>
          </div>
          <span className="px-2.5 py-1 rounded text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-200 self-start sm:self-auto">
            Dynamic Prognostic Sandbox
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left Column: Interactive Controls */}
          <div className="lg:col-span-5 space-y-4 bg-slate-50/70 p-4 rounded-xl border border-slate-200 text-xs">
            {/* Axle Load Slider */}
            <div>
              <div className="flex justify-between font-semibold text-slate-800 mb-1">
                <span>Axle Load (Broad Gauge)</span>
                <span className="font-mono text-blue-600 font-bold">{simAxleLoad.toFixed(2)} Tonnes</span>
              </div>
              <input
                type="range"
                min="20.0"
                max="25.0"
                step="0.25"
                value={simAxleLoad}
                onChange={(e) => setSimAxleLoad(parseFloat(e.target.value))}
                className="w-full accent-blue-600 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
                <span>20.0t (Standard)</span>
                <span>22.82t (Indian Railways Std)</span>
                <span>25.0t (Heavy Haul)</span>
              </div>
            </div>

            {/* Annual Traffic Density Slider */}
            <div>
              <div className="flex justify-between font-semibold text-slate-800 mb-1">
                <span>Annual Traffic Density</span>
                <span className="font-mono text-blue-600 font-bold">{simTrafficMgt} MGT / year</span>
              </div>
              <input
                type="range"
                min="15"
                max="60"
                step="5"
                value={simTrafficMgt}
                onChange={(e) => setSimTrafficMgt(parseInt(e.target.value))}
                className="w-full accent-blue-600 cursor-pointer"
              />
              <span className="text-[10px] text-slate-400">Million Gross Tonnes carried over the segment annually</span>
            </div>

            {/* Deferred Tamping Delay Slider */}
            <div>
              <div className="flex justify-between font-semibold text-slate-800 mb-1">
                <span>Deferred Maintenance Delay</span>
                <span className={`font-mono font-bold ${simDeferredDays > 0 ? 'text-amber-600' : 'text-slate-600'}`}>
                  +{simDeferredDays} Days
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="120"
                step="15"
                value={simDeferredDays}
                onChange={(e) => setSimDeferredDays(parseInt(e.target.value))}
                className="w-full accent-amber-600 cursor-pointer"
              />
              <span className="text-[10px] text-slate-400">Simulate effect of deferring scheduled mechanized tamping window</span>
            </div>

            {/* Monsoon Rainfall Slider */}
            <div>
              <div className="flex justify-between font-semibold text-slate-800 mb-1">
                <span>Monsoon Precipitation (48h Cumulative)</span>
                <span className={`font-mono font-bold ${simMonsoonRain > 0 ? 'text-indigo-600' : 'text-slate-600'}`}>
                  {simMonsoonRain} mm
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="300"
                step="25"
                value={simMonsoonRain}
                onChange={(e) => setSimMonsoonRain(parseInt(e.target.value))}
                className="w-full accent-indigo-600 cursor-pointer"
              />
              <span className="text-[10px] text-slate-400">Heavy rainfall saturates ballast formation, accelerating settlement</span>
            </div>

            {/* Ballast Condition Selector */}
            <div>
              <label className="block font-semibold text-slate-800 mb-1">Ballast Cushion & Formation State</label>
              <select
                value={simBallast}
                onChange={(e) => setSimBallast(e.target.value)}
                className="w-full px-3 py-1.5 rounded-lg border border-slate-200 bg-white font-medium text-xs focus:ring-2 focus:ring-blue-500"
              >
                <option value="EXCELLENT">Excellent (Fresh ballast cushion &gt; 350 mm)</option>
                <option value="GOOD">Good (Standard 300 mm cushion)</option>
                <option value="MODERATE">Moderate (Partial fouling / cleanable)</option>
                <option value="DEGRADED">Degraded (Caked ballast / poor drainage)</option>
              </select>
            </div>
          </div>

          {/* Right Column: Dynamic KPIs & Projected Curve */}
          <div className="lg:col-span-7 space-y-4">
            {simResult && (
              <>
                {/* Simulation KPI Summary Cards */}
                <div className="grid grid-cols-3 gap-3">
                  <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                    <span className="text-[11px] text-slate-500 block">Simulated Rate</span>
                    <p className="text-base font-extrabold text-slate-900 mt-0.5">
                      {simResult.degradation_metrics.simulated_rate_mm_per_month} <span className="text-xs font-normal text-slate-500">mm/mo</span>
                    </p>
                    <span className={`text-[10px] font-bold ${simResult.degradation_metrics.degradation_acceleration_pct > 0 ? 'text-red-600' : 'text-emerald-600'}`}>
                      {simResult.degradation_metrics.degradation_acceleration_pct > 0 ? `+${simResult.degradation_metrics.degradation_acceleration_pct}%` : 'Baseline'}
                    </span>
                  </div>

                  <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                    <span className="text-[11px] text-slate-500 block">Days to UML</span>
                    <p className="text-base font-extrabold text-slate-900 mt-0.5">
                      {simResult.degradation_metrics.projected_days_to_uml} <span className="text-xs font-normal text-slate-500">days</span>
                    </p>
                    <span className={`px-1.5 py-0.2 rounded text-[10px] font-bold ${
                      simResult.degradation_metrics.projected_days_to_uml <= 14 ? 'bg-red-100 text-red-800' :
                      simResult.degradation_metrics.projected_days_to_uml <= 45 ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'
                    }`}>
                      {simResult.advisory.urgency_tier.replace('_', ' ')}
                    </span>
                  </div>

                  <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl">
                    <span className="text-[11px] text-slate-500 block">Mandated Speed</span>
                    <p className="text-base font-extrabold text-blue-700 mt-0.5">
                      {simResult.advisory.mandated_speed_restriction_kmph} <span className="text-xs font-normal text-slate-500">km/h</span>
                    </p>
                    <span className="text-[10px] text-slate-500">Caution order limit</span>
                  </div>
                </div>

                {/* Advisory Directive Banner */}
                <div className={`p-3 rounded-xl border text-xs flex items-start space-x-2.5 ${
                  simResult.degradation_metrics.projected_days_to_uml <= 14
                    ? 'bg-red-50 border-red-200 text-red-900'
                    : simResult.degradation_metrics.projected_days_to_uml <= 45
                    ? 'bg-amber-50 border-amber-200 text-amber-900'
                    : 'bg-blue-50 border-blue-200 text-blue-900'
                }`}>
                  <ShieldAlert className="w-4 h-4 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold block">Operational Directive:</span>
                    <p className="text-[11px] mt-0.5">{simResult.advisory.action_directive}</p>
                  </div>
                </div>

                {/* 12-Month Projected Deterioration Trajectory */}
                <div className="h-60 border border-slate-100 rounded-xl p-2 bg-slate-50/50">
                  <div className="text-[11px] font-bold text-slate-700 mb-1 px-2 flex justify-between">
                    <span>12-Month Track Geometry Trajectory Comparison</span>
                    <span className="text-[10px] font-mono text-slate-400">IRPWM Table 5.1 Benchmarking</span>
                  </div>
                  <ResponsiveContainer width="100%" height="88%">
                    <LineChart data={simResult.projection_timeline}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                      <XAxis dataKey="month" tick={{ fontSize: 10 }} />
                      <YAxis tick={{ fontSize: 10 }} domain={[6, 20]} unit="mm" />
                      <Tooltip />
                      <Legend wrapperStyle={{ fontSize: '11px' }} />
                      <ReferenceLine y={12.0} stroke="#ef4444" strokeDasharray="4 4" label={{ value: 'UML (12.0 mm)', fill: '#ef4444', fontSize: 10 }} />
                      <ReferenceLine y={8.0} stroke="#f59e0b" strokeDasharray="4 4" label={{ value: 'NBML (8.0 mm)', fill: '#f59e0b', fontSize: 10 }} />
                      <Line type="monotone" dataKey="baseline_trajectory_mm" name="Baseline Degradation" stroke="#2563eb" strokeWidth={2} dot={{ r: 2 }} />
                      <Line type="monotone" dataKey="simulated_trajectory_mm" name="Simulated Scenario" stroke="#dc2626" strokeWidth={2.5} dot={{ r: 2 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </>
            )}
          </div>
        </div>
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
