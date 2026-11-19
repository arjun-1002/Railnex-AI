import React, { useEffect, useState } from 'react';
import { MaintenancePriorityItem } from '../types';
import { fetchMaintenancePrioritization, fetchMaintenanceAdvisory } from '../services/api';
import {
  AlertTriangle,
  ArrowUpDown,
  CheckCircle2,
  Clock,
  Download,
  Filter,
  ListOrdered,
  Search,
  ShieldAlert,
  FileText,
  Printer,
  X
} from 'lucide-react';

export const MaintenancePriorityPage: React.FC = () => {
  const [items, setItems] = useState<MaintenancePriorityItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Advisory Modal State
  const [advisoryModal, setAdvisoryModal] = useState<boolean>(false);
  const [advisoryData, setAdvisoryData] = useState<any | null>(null);
  const [advisoryLoading, setAdvisoryLoading] = useState<boolean>(false);

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

  const handleOpenAdvisory = async () => {
    setAdvisoryLoading(true);
    setAdvisoryModal(true);
    try {
      const data = await fetchMaintenanceAdvisory();
      setAdvisoryData(data);
      setAdvisoryLoading(false);
    } catch (err: any) {
      console.error(err);
      setAdvisoryLoading(false);
    }
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

          <div className="flex items-center space-x-2">
            <button
              onClick={handleOpenAdvisory}
              className="flex items-center px-3.5 py-2 rounded-lg bg-red-600 text-white text-xs font-semibold hover:bg-red-700 transition-colors shrink-0 shadow-xs"
            >
              <FileText className="w-4 h-4 mr-1.5" />
              Official P-Way Advisory (IRPWM 2020)
            </button>
            <button
              onClick={exportCSV}
              className="flex items-center px-3.5 py-2 rounded-lg bg-slate-900 text-white text-xs font-semibold hover:bg-slate-800 transition-colors shrink-0 shadow-xs"
            >
              <Download className="w-4 h-4 mr-1.5" />
              Export Prioritized Roster (CSV)
            </button>
          </div>
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

      {/* Official Indian Railways Maintenance Advisory Modal */}
      {advisoryModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto shadow-2xl border border-slate-200">
            {/* Modal Header */}
            <div className="sticky top-0 bg-slate-900 text-white px-6 py-4 flex items-center justify-between z-10">
              <div className="flex items-center space-x-2">
                <FileText className="w-5 h-5 text-amber-400" />
                <h3 className="font-bold text-sm">Official Track Maintenance Advisory Sheet (IRPWM Form)</h3>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => window.print()}
                  className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg flex items-center space-x-1.5 transition-colors"
                >
                  <Printer className="w-3.5 h-3.5" />
                  <span>Print Advisory</span>
                </button>
                <button
                  onClick={() => setAdvisoryModal(false)}
                  className="p-1 text-slate-400 hover:text-white rounded-lg transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Modal Content / Printable Document */}
            {advisoryLoading ? (
              <div className="p-12 text-center text-slate-500 text-sm">
                Generating official advisory documentation...
              </div>
            ) : advisoryData ? (
              <div className="p-8 space-y-6 text-slate-800 text-xs">
                {/* Official Letterhead */}
                <div className="text-center border-b-2 border-slate-900 pb-4">
                  <h1 className="text-base font-extrabold tracking-wider uppercase text-slate-900">
                    INDIAN RAILWAYS — CIVIL ENGINEERING DEPARTMENT
                  </h1>
                  <h2 className="text-xs font-bold text-slate-700 uppercase mt-0.5">
                    {advisoryData.issuing_authority}
                  </h2>
                  <div className="flex justify-between items-center mt-3 text-[11px] font-mono text-slate-600">
                    <span>Advisory Ref: <strong>{advisoryData.advisory_ref}</strong></span>
                    <span>Date: <strong>{advisoryData.date_generated}</strong></span>
                  </div>
                </div>

                {/* Statutory Reference */}
                <div className="p-3 bg-red-50 border-l-4 border-red-600 text-[11px] text-red-900 space-y-1">
                  <p className="font-bold">STATUTORY MANDATE: {advisoryData.statutory_mandate}</p>
                  <p className="text-slate-700">{advisoryData.executive_summary}</p>
                </div>

                {/* Target Addressed Officials */}
                <div>
                  <h4 className="font-bold uppercase tracking-wider text-slate-700 text-[11px] mb-1">
                    Addressed To:
                  </h4>
                  <ul className="list-disc pl-5 space-y-0.5 text-[11px] text-slate-600">
                    {advisoryData.target_officials?.map((officer: string, idx: number) => (
                      <li key={idx}>{officer}</li>
                    ))}
                  </ul>
                </div>

                {/* Critical Exceedances Schedule */}
                <div>
                  <h4 className="font-bold uppercase tracking-wider text-slate-900 text-xs mb-2">
                    Schedule of Safety-Critical Urgent Maintenance Limit (UML) Exceedances:
                  </h4>
                  <div className="border border-slate-300 rounded-lg overflow-hidden">
                    <table className="min-w-full divide-y divide-slate-200 text-xs">
                      <thead className="bg-slate-100 font-bold text-slate-800">
                        <tr>
                          <th className="px-3 py-2 text-left">Segment</th>
                          <th className="px-3 py-2 text-left">Location / MP</th>
                          <th className="px-3 py-2 text-left">Defect Channel</th>
                          <th className="px-3 py-2 text-right">Deviation</th>
                          <th className="px-3 py-2 text-right">Priority Score</th>
                          <th className="px-3 py-2 text-left">Mandated Action Directive</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-200">
                        {advisoryData.critical_exceedances?.slice(0, 8).map((exc: any, idx: number) => (
                          <tr key={idx} className="hover:bg-slate-50">
                            <td className="px-3 py-2 font-bold text-slate-900">Seg {exc.line_segment_id}</td>
                            <td className="px-3 py-2 font-mono">MP {exc.milepost}</td>
                            <td className="px-3 py-2 font-semibold text-blue-700">{exc.defect_type}</td>
                            <td className="px-3 py-2 text-right font-mono text-red-700 font-bold">
                              {(exc.defect_amplitude_in * 25.4).toFixed(1)} mm ({exc.defect_amplitude_in}")
                            </td>
                            <td className="px-3 py-2 text-right font-bold">{exc.priority_score.toFixed(1)}</td>
                            <td className="px-3 py-2 text-slate-700">{exc.suggested_action}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Tamping Machine Allocation */}
                <div>
                  <h4 className="font-bold uppercase tracking-wider text-slate-900 text-xs mb-2">
                    Mechanized Track Machine Allocation Schedule:
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {advisoryData.tamping_allocation?.map((tamp: any, idx: number) => (
                      <div key={idx} className="p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-1">
                        <span className="font-bold text-slate-900 block">{tamp.machine_type}</span>
                        <div className="text-[11px] text-slate-600 flex justify-between">
                          <span>Section:</span>
                          <span className="font-semibold text-slate-800">{tamp.target_section}</span>
                        </div>
                        <div className="text-[11px] text-slate-600 flex justify-between">
                          <span>Block Window:</span>
                          <span className="font-semibold text-blue-700">{tamp.shift}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Official Sign-Off Block */}
                <div className="pt-6 border-t border-slate-300 grid grid-cols-3 gap-6 text-center text-[11px]">
                  <div>
                    <p className="text-slate-400 italic mb-6">[System Generated Digital Signature]</p>
                    <p className="font-bold text-slate-900">{advisoryData.signoff_block?.prepared_by}</p>
                    <p className="text-slate-500">Autonomous Decision-Support Layer</p>
                  </div>
                  <div>
                    <div className="h-6 mb-6 border-b border-dashed border-slate-400"></div>
                    <p className="font-bold text-slate-900">{advisoryData.signoff_block?.verified_by}</p>
                    <p className="text-slate-500">Permanent Way Section In-Charge</p>
                  </div>
                  <div>
                    <div className="h-6 mb-6 border-b border-dashed border-slate-400"></div>
                    <p className="font-bold text-slate-900">{advisoryData.signoff_block?.approved_by}</p>
                    <p className="text-slate-500">Divisional Railway Administration</p>
                  </div>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
};
