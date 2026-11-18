import React, { useEffect, useState } from 'react';
import { MaintenancePriorityItem } from '../types';
import { fetchMaintenancePrioritization } from '../services/api';
import {
  AlertTriangle,
  ArrowUpDown,
  CheckCircle2,
  Clock,
  Download,
  Filter,
  ListOrdered,
  Search,
  ShieldAlert
} from 'lucide-react';

export const MaintenancePriorityPage: React.FC = () => {
  const [items, setItems] = useState<MaintenancePriorityItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [urgencyFilter, setUrgencyFilter] = useState<string>('ALL');
  const [defectFilter, setDefectFilter] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');

  useEffect(() => {
    loadData();
  }, [urgencyFilter, defectFilter]);

  const loadData = () => {
    setLoading(true);
    fetchMaintenancePrioritization({
      urgency: urgencyFilter,
      defect_type: defectFilter,
      limit: 150
    })
      .then((res) => {
        setItems(res);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  const filteredItems = items.filter((item) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      item.line_segment_id.toString().includes(q) ||
      item.milepost.toString().includes(q) ||
      item.defect_type.toLowerCase().includes(q) ||
      item.priority_tier.toLowerCase().includes(q)
    );
  });

  const exportCSV = () => {
    if (items.length === 0) return;
    const headers = [
      'Record_ID',
      'Line_Segment_ID',
      'Milepost',
      'Defect_Type',
      'Amplitude_Inches',
      'Length_Feet',
      'Predicted_Severity',
      'Priority_Score',
      'Priority_Tier',
      'Action_Recommendation',
      'Inspection_Date'
    ];
    const rows = filteredItems.map((r) => [
      r.record_id,
      r.line_segment_id,
      r.milepost,
      r.defect_type,
      r.defect_amplitude_in,
      r.defect_length_ft,
      r.predicted_severity,
      r.priority_score,
      r.priority_tier,
      `"${r.suggested_action}"`,
      r.inspection_date || ''
    ]);
    const csvContent = [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Railnex_Maintenance_Priority_List_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Title & Guidance Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded text-xs font-bold uppercase bg-blue-100 text-blue-800">
                Decision Support
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                Railway Track Inspection Maintenance Prioritization List
              </h2>
            </div>
            <p className="text-xs sm:text-sm text-slate-600 mt-1">
              Multi-criteria ranking to assist permanent way engineers in optimizing scarce inspection trolleys, tamping machines, and gang deployment.
            </p>
          </div>

          <button
            onClick={exportCSV}
            className="flex items-center px-3.5 py-2 rounded-lg bg-slate-900 text-white text-xs font-semibold hover:bg-slate-800 transition-colors shrink-0 shadow-xs"
          >
            <Download className="w-4 h-4 mr-1.5" />
            Export Prioritized Roster (CSV)
          </button>
        </div>

        {/* Priority Formula Note */}
        <div className="mt-4 pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500">
          <span>
            <strong>Priority Formula:</strong> <code className="bg-slate-100 px-1.5 py-0.5 rounded text-slate-800 font-mono text-[11px]">Score = 40% P(Red Tag) + 35% |Amp Exceedance| + 15% Defect Extent + 10% Speed Exposure</code>
          </span>
          <span className="text-slate-400">Notice: Prioritization ranking serves decision support, not automatic certification.</span>
        </div>
      </div>

      {/* Filter and Control Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-slate-400" />
            <span className="text-xs font-semibold text-slate-700">Urgency Tier:</span>
            <select
              value={urgencyFilter}
              onChange={(e) => setUrgencyFilter(e.target.value)}
              className="text-xs px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="ALL">All Tiers ({items.length})</option>
              <option value="CRITICAL">Critical Review Only</option>
              <option value="HIGH">Critical + High Priority</option>
            </select>
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold text-slate-700">Defect Type:</span>
            <select
              value={defectFilter}
              onChange={(e) => setDefectFilter(e.target.value)}
              className="text-xs px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="ALL">All Types</option>
              <option value="XLEVEL">Cross-Level (XLEVEL)</option>
              <option value="SURFACE">Surface Profile</option>
              <option value="DIP">Track Dip</option>
            </select>
          </div>
        </div>

        <div className="relative w-full md:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search line, milepost, type..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Prioritized Records Table */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs">
        {loading ? (
          <div className="p-12 text-center text-slate-500 text-sm">
            <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
            Ranking track maintenance inspections...
          </div>
        ) : error ? (
          <div className="p-8 text-center text-red-600 text-sm">{error}</div>
        ) : filteredItems.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-sm">
            No track observations matching current filter criteria.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 text-xs">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-3.5 py-3 text-left font-semibold text-slate-700">Rank / ID</th>
                  <th className="px-3.5 py-3 text-left font-semibold text-slate-700">Line Segment</th>
                  <th className="px-3.5 py-3 text-left font-semibold text-slate-700">Milepost</th>
                  <th className="px-3.5 py-3 text-left font-semibold text-slate-700">Defect Channel</th>
                  <th className="px-3.5 py-3 text-right font-semibold text-slate-700">Amplitude</th>
                  <th className="px-3.5 py-3 text-right font-semibold text-slate-700">Extent</th>
                  <th className="px-3.5 py-3 text-center font-semibold text-slate-700">Predicted Severity</th>
                  <th className="px-3.5 py-3 text-center font-semibold text-slate-700">Priority Score</th>
                  <th className="px-3.5 py-3 text-center font-semibold text-slate-700">Urgency Tier</th>
                  <th className="px-3.5 py-3 text-left font-semibold text-slate-700">Recommended Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 bg-white">
                {filteredItems.map((item, idx) => (
                  <tr key={item.record_id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-3.5 py-2.5 font-mono font-bold text-slate-900">
                      #{idx + 1} <span className="text-slate-400 font-normal">({item.record_id})</span>
                    </td>
                    <td className="px-3.5 py-2.5 font-medium text-slate-900">
                      Segment {item.line_segment_id}
                    </td>
                    <td className="px-3.5 py-2.5 font-mono text-slate-700">
                      MP {item.milepost.toFixed(2)}
                    </td>
                    <td className="px-3.5 py-2.5">
                      <span className="font-semibold text-slate-800">{item.defect_type}</span>
                    </td>
                    <td className="px-3.5 py-2.5 text-right font-mono font-bold text-slate-900">
                      {item.defect_amplitude_in.toFixed(2)}"
                    </td>
                    <td className="px-3.5 py-2.5 text-right font-mono text-slate-600">
                      {item.defect_length_ft.toFixed(1)} ft
                    </td>
                    <td className="px-3.5 py-2.5 text-center">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold ${
                        item.predicted_severity.includes('Red')
                          ? 'bg-red-50 text-red-700 border border-red-200'
                          : 'bg-amber-50 text-amber-700 border border-amber-200'
                      }`}>
                        {item.predicted_severity}
                      </span>
                    </td>
                    <td className="px-3.5 py-2.5 text-center">
                      <div className="flex items-center justify-center space-x-1.5">
                        <span className="font-mono font-extrabold text-sm text-slate-900">
                          {item.priority_score.toFixed(1)}
                        </span>
                      </div>
                    </td>
                    <td className="px-3.5 py-2.5 text-center">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider ${
                        item.priority_tier === 'CRITICAL_REVIEW'
                          ? 'bg-red-600 text-white'
                          : item.priority_tier === 'HIGH_PRIORITY'
                          ? 'bg-amber-500 text-white'
                          : 'bg-slate-200 text-slate-700'
                      }`}>
                        {item.priority_tier.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-3.5 py-2.5 text-slate-600 max-w-xs truncate" title={item.suggested_action}>
                      {item.suggested_action}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
