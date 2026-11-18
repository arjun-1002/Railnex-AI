import React, { useEffect, useState } from 'react';
import { queryDataExplorer } from '../services/api';
import {
  ChevronLeft,
  ChevronRight,
  Database,
  Download,
  Filter,
  Layers,
  Search,
  ShieldCheck
} from 'lucide-react';

export const DataExplorerPage: React.FC = () => {
  const [records, setRecords] = useState<any[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [page, setPage] = useState<number>(1);
  const [pageSize] = useState<number>(50);
  const [loading, setLoading] = useState<boolean>(true);

  // Filters
  const [defectType, setDefectType] = useState<string>('');
  const [priorityTag, setPriorityTag] = useState<string>('');
  const [lineSegment, setLineSegment] = useState<string>('');

  useEffect(() => {
    loadData();
  }, [page, defectType, priorityTag, lineSegment]);

  const loadData = () => {
    setLoading(true);
    queryDataExplorer({
      page,
      pageSize,
      defectType: defectType || undefined,
      priority: priorityTag || undefined,
      lineSegment: lineSegment ? parseInt(lineSegment) : undefined
    })
      .then((res) => {
        setRecords(res.records);
        setTotal(res.total);
        setTotalPages(res.total_pages);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  };

  const handleExportPage = () => {
    if (records.length === 0) return;
    const headers = Object.keys(records[0]);
    const csvRows = [
      headers.join(','),
      ...records.map((r) => headers.map((h) => JSON.stringify(r[h] ?? '')).join(','))
    ].join('\n');
    const blob = new Blob([csvRows], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Railnex_Inspection_Records_Page_${page}.csv`;
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
                Data Repository
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                Railway Track Inspection Data Explorer & Quality Audit
              </h2>
            </div>
            <p className="text-xs sm:text-sm text-slate-600 mt-1">
              Browse, filter, and inspect verified real track geometry records (INFORMS 2015). Total verified dataset size: 23,847 rows.
            </p>
          </div>

          <button
            onClick={handleExportPage}
            className="flex items-center px-3.5 py-2 rounded-lg bg-slate-900 text-white text-xs font-semibold hover:bg-slate-800 transition-colors shrink-0 shadow-xs"
          >
            <Download className="w-4 h-4 mr-1.5" />
            Export Filtered Page (CSV)
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center space-x-2 text-xs">
            <span className="font-semibold text-slate-700">Defect Channel:</span>
            <select
              value={defectType}
              onChange={(e) => {
                setDefectType(e.target.value);
                setPage(1);
              }}
              className="px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Types</option>
              <option value="XLEVEL">XLEVEL (Cross-Level)</option>
              <option value="SURFACE">SURFACE (Profile)</option>
              <option value="DIP">DIP (Dip Defect)</option>
            </select>
          </div>

          <div className="flex items-center space-x-2 text-xs">
            <span className="font-semibold text-slate-700">Priority Tag:</span>
            <select
              value={priorityTag}
              onChange={(e) => {
                setPriorityTag(e.target.value);
                setPage(1);
              }}
              className="px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Priorities</option>
              <option value="RED">RED (Urgent Action Required)</option>
              <option value="YEL">YEL (Scheduled Maintenance)</option>
            </select>
          </div>

          <div className="flex items-center space-x-2 text-xs">
            <span className="font-semibold text-slate-700">Line Segment:</span>
            <input
              type="number"
              placeholder="e.g. 1"
              value={lineSegment}
              onChange={(e) => {
                setLineSegment(e.target.value);
                setPage(1);
              }}
              className="w-24 px-2.5 py-1.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 text-xs"
            />
          </div>
        </div>

        <div className="text-xs text-slate-500 font-mono">
          Showing {records.length} of {total.toLocaleString()} records (Page {page} of {totalPages})
        </div>
      </div>

      {/* Records Table */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs">
        {loading ? (
          <div className="p-12 text-center text-slate-500 text-sm">
            <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
            Loading inspection records...
          </div>
        ) : records.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-sm">
            No inspection observations matching current filter parameters.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 text-xs">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-3 py-2.5 text-left font-semibold text-slate-700">Defect ID</th>
                  <th className="px-3 py-2.5 text-left font-semibold text-slate-700">Line Segment</th>
                  <th className="px-3 py-2.5 text-left font-semibold text-slate-700">Milepost</th>
                  <th className="px-3 py-2.5 text-left font-semibold text-slate-700">Defect Type</th>
                  <th className="px-3 py-2.5 text-right font-semibold text-slate-700">Amplitude (in)</th>
                  <th className="px-3 py-2.5 text-right font-semibold text-slate-700">Length (ft)</th>
                  <th className="px-3 py-2.5 text-center font-semibold text-slate-700">FRA Class</th>
                  <th className="px-3 py-2.5 text-right font-semibold text-slate-700">Freight Spd</th>
                  <th className="px-3 py-2.5 text-right font-semibold text-slate-700">Pass Spd</th>
                  <th className="px-3 py-2.5 text-center font-semibold text-slate-700">Tag / Priority</th>
                  <th className="px-3 py-2.5 text-left font-semibold text-slate-700">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 bg-white">
                {records.map((r) => (
                  <tr key={r.defect_id} className="hover:bg-slate-50">
                    <td className="px-3 py-2 font-mono font-bold text-slate-900">{r.defect_id}</td>
                    <td className="px-3 py-2 font-medium text-slate-900">Segment {r.line_segment_id}</td>
                    <td className="px-3 py-2 font-mono text-slate-700">{r.milepost.toFixed(3)}</td>
                    <td className="px-3 py-2 font-semibold text-slate-800">{r.defect_type}</td>
                    <td className="px-3 py-2 text-right font-mono font-bold text-slate-900">
                      {r.defect_amplitude_in.toFixed(2)}"
                    </td>
                    <td className="px-3 py-2 text-right font-mono text-slate-600">{r.defect_length_ft.toFixed(1)}</td>
                    <td className="px-3 py-2 text-center font-mono">Class {r.fra_track_class}</td>
                    <td className="px-3 py-2 text-right font-mono">{r.freight_speed_limit_mph} mph</td>
                    <td className="px-3 py-2 text-right font-mono">{r.passenger_speed_limit_mph} mph</td>
                    <td className="px-3 py-2 text-center">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold ${
                        r.defect_priority_tag === 'RED'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-amber-100 text-amber-800'
                      }`}>
                        {r.defect_priority_tag === 'RED' ? 'RED TAG (UML)' : 'YELLOW TAG (PML)'}
                      </span>
                    </td>
                    <td className="px-3 py-2 font-mono text-slate-600">{r.inspection_date || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination Bar */}
        <div className="px-4 py-3 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1 || loading}
            className="flex items-center px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-700 bg-white hover:bg-slate-100 disabled:opacity-40"
          >
            <ChevronLeft className="w-3.5 h-3.5 mr-1" /> Previous
          </button>

          <span className="text-xs text-slate-600 font-medium">
            Page <strong className="text-slate-900">{page}</strong> of <strong className="text-slate-900">{totalPages}</strong>
          </span>

          <button
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page === totalPages || loading}
            className="flex items-center px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-700 bg-white hover:bg-slate-100 disabled:opacity-40"
          >
            Next <ChevronRight className="w-3.5 h-3.5 ml-1" />
          </button>
        </div>
      </div>
    </div>
  );
};
