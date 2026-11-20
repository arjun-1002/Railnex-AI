import React, { useState, useEffect } from 'react';
import { fetchUsfdFlaws, fetchUsfdStandards } from '../services/api';
import { Activity, ShieldAlert, AlertTriangle, CheckCircle, Search, Filter, BookOpen } from 'lucide-react';

export const UsfdAnalysisPage: React.FC = () => {
  const [flaws, setFlaws] = useState<any[]>([]);
  const [standards, setStandards] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedFilter, setSelectedFilter] = useState<string>('ALL');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [flawsData, standardsData] = await Promise.all([
        fetchUsfdFlaws(150),
        fetchUsfdStandards()
      ]);
      setFlaws(flawsData);
      setStandards(standardsData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredFlaws = flaws.filter((item) => {
    const matchesSearch =
      item.usfd_record_id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.flaw_description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.route_section?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesUrgency =
      selectedFilter === 'ALL' || item.severity_classification === selectedFilter;
    return matchesSearch && matchesUrgency;
  });

  return (
    <div className="space-y-6">
      {/* Title Header */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-blue-50 text-blue-700 rounded-lg">
              <Activity className="w-5 h-5" />
            </span>
            <h1 className="text-xl font-bold text-slate-900 tracking-tight">
              Module 10 — RDSO Ultrasonic Flaw Detection (USFD) Analysis
            </h1>
          </div>
          <p className="text-sm text-slate-500 mt-1">
            Standardized ultrasonic testing inspection records and defect classifications governed by the RDSO Manual for Ultrasonic Testing of Rails and Welds.
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-semibold">
          <span className="px-3 py-1.5 rounded-lg bg-red-50 text-red-700 border border-red-200">
            IMR: Immediate Removal (3 Days)
          </span>
          <span className="px-3 py-1.5 rounded-lg bg-amber-50 text-amber-700 border border-amber-200">
            OBS: Fortnightly Observation
          </span>
        </div>
      </div>

      {/* Standards Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <span className="text-xs text-slate-500 font-medium">Active USFD Records</span>
          <div className="text-2xl font-bold text-slate-900 mt-1">{flaws.length}</div>
          <span className="text-[11px] text-blue-600 font-semibold">Corridor Inspection Logs</span>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <span className="text-xs text-slate-500 font-medium">IMR / IMRW Urgent Flaws</span>
          <div className="text-2xl font-bold text-red-600 mt-1">
            {flaws.filter(f => f.severity_classification?.includes('IMR')).length}
          </div>
          <span className="text-[11px] text-red-600 font-semibold">30 km/h Restriction Mandated</span>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <span className="text-xs text-slate-500 font-medium">OBS Flaws (Under Watch)</span>
          <div className="text-2xl font-bold text-amber-600 mt-1">
            {flaws.filter(f => f.severity_classification?.includes('OBS')).length}
          </div>
          <span className="text-[11px] text-amber-600 font-semibold">Fortnightly Testing Cycle</span>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <span className="text-xs text-slate-500 font-medium">Governing Authority</span>
          <div className="text-base font-bold text-slate-900 mt-1">RDSO Lucknow</div>
          <span className="text-[11px] text-slate-500">Ministry of Railways</span>
        </div>
      </div>

      {/* RDSO Defect Classification Standards Reference */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-4">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700 flex items-center">
          <BookOpen className="w-4 h-4 mr-2 text-blue-600" />
          RDSO Ultrasonic Defect Taxonomy (100–800 Series)
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {standards.slice(0, 6).map((std, idx) => (
            <div key={idx} className="p-3 rounded-lg border border-slate-100 bg-slate-50/50 space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-slate-900">Code {std.defect_code}</span>
                <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                  std.severity_classification === 'IMR' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'
                }`}>
                  {std.severity_classification}
                </span>
              </div>
              <div className="text-xs font-semibold text-slate-800">{std.defect_type}</div>
              <div className="text-[11px] text-slate-500">{std.action_required}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Corridor Inspection Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="p-4 border-b border-slate-200 flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div className="relative flex-1 max-w-md">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search by ID, defect type, or corridor..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-xs focus:outline-hidden focus:ring-1 focus:ring-blue-500"
            />
          </div>

          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-slate-400" />
            <span className="text-xs text-slate-500 font-medium">Urgency:</span>
            {['ALL', 'IMR', 'OBS', 'IMRW'].map((f) => (
              <button
                key={f}
                onClick={() => setSelectedFilter(f)}
                className={`px-3 py-1 rounded-md text-xs font-semibold transition-colors ${
                  selectedFilter === f
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {f}
              </button>
            ))}
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider">
              <tr>
                <th className="py-3 px-4">Record ID</th>
                <th className="py-3 px-4">Corridor & Section</th>
                <th className="py-3 px-4">Milepost</th>
                <th className="py-3 px-4">Flaw Classification</th>
                <th className="py-3 px-4">Depth (mm)</th>
                <th className="py-3 px-4">Echo (dB)</th>
                <th className="py-3 px-4">Urgency</th>
                <th className="py-3 px-4">Est. Days to Critical</th>
                <th className="py-3 px-4">Mandated Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {filteredFlaws.map((row, idx) => {
                const isImr = row.severity_classification?.includes('IMR');
                return (
                  <tr key={idx} className="hover:bg-slate-50/70 transition-colors">
                    <td className="py-3 px-4 font-mono font-bold text-slate-900">{row.usfd_record_id}</td>
                    <td className="py-3 px-4">
                      <div className="font-semibold">{row.route_section}</div>
                      <div className="text-[10px] text-slate-400">{row.railway_zone} / {row.division}</div>
                    </td>
                    <td className="py-3 px-4 font-mono">{row.milepost_km} km</td>
                    <td className="py-3 px-4">
                      <span className="font-medium text-slate-800">{row.flaw_description}</span>
                      <span className="text-[10px] text-slate-400 block font-mono">Code {row.flaw_code} ({row.flaw_location})</span>
                    </td>
                    <td className="py-3 px-4 font-mono font-semibold">{row.flaw_depth_mm} mm</td>
                    <td className="py-3 px-4 font-mono">{row.echo_amplitude_db} dB</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded font-bold text-[10px] ${
                        isImr ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'
                      }`}>
                        {row.severity_classification}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono font-bold text-slate-900">
                      {row.est_days_to_critical} days
                    </td>
                    <td className="py-3 px-4 text-slate-600 max-w-xs truncate" title={row.action_mandate}>
                      {row.action_mandate}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
