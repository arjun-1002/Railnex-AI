import React, { useState } from 'react';
import {
  AlertCircle,
  CheckCircle2,
  Clock,
  Compass,
  Database,
  ExternalLink,
  FileSpreadsheet,
  FileText,
  GitBranch,
  Info,
  Layers,
  Lock,
  Save,
  ShieldCheck,
  UploadCloud,
  Zap
} from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [rtiStatus] = useState<string>('SUBMITTED_AWAITING_RECORDS');
  const [spatialRadius, setSpatialRadius] = useState<number>(25);
  const [temporalWindow, setTemporalWindow] = useState<number>(6);
  const [savedNotice, setSavedNotice] = useState<boolean>(false);

  const handleSave = () => {
    setSavedNotice(true);
    setTimeout(() => setSavedNotice(false), 3000);
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Title & Guidance Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded text-xs font-bold uppercase bg-blue-100 text-blue-800">
                System Administration
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                Railnex AI Pipeline Configuration & RTI Integration Status
              </h2>
            </div>
            <p className="text-xs sm:text-sm text-slate-600 mt-1">
              Manage Indian Railways Track Management System (TMS) RTI ingestion hooks, weather coupling parameters, and system governance.
            </p>
          </div>

          <a
            href="https://github.com/arjun-1002/Railnex-AI.git"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center px-3.5 py-2 rounded-lg bg-slate-900 text-white text-xs font-semibold hover:bg-slate-800 transition-colors shrink-0 shadow-xs"
          >
            <GitBranch className="w-4 h-4 mr-1.5" />
            GitHub Repository
            <ExternalLink className="w-3.5 h-3.5 ml-1.5" />
          </a>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: RTI TMS Integration Pipeline */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="w-5 h-5 text-blue-600" />
              <h3 className="text-sm font-bold text-slate-900">
                Indian Railways TMS RTI Data Pipeline
              </h3>
            </div>
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-50 text-amber-800 border border-amber-200">
              RTI Active Application
            </span>
          </div>

          <div className="text-xs text-slate-600 leading-relaxed space-y-2">
            <p>
              A formal application under the Right to Information (RTI) Act has been submitted requesting anonymized Track Management System (TMS) inspection and Track Recording Car (TRC) logs covering 2020–2025 across Zonal Railways.
            </p>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-1.5">
              <div className="flex justify-between">
                <span className="font-semibold text-slate-700">Target Records:</span>
                <span className="font-mono text-slate-900">TMS TRC Runs & Peak Exceedance Tables</span>
              </div>
              <div className="flex justify-between">
                <span className="font-semibold text-slate-700">Parser Module:</span>
                <span className="font-mono text-blue-600">scripts/rti_pipeline.py</span>
              </div>
              <div className="flex justify-between">
                <span className="font-semibold text-slate-700">Supported Formats:</span>
                <span className="font-mono text-slate-900">CSV, XLSX, XLS, Parquet</span>
              </div>
              <div className="flex justify-between">
                <span className="font-semibold text-slate-700">Zonal Mapping:</span>
                <span className="text-emerald-700 font-semibold">All 17 Zonal Railways + 68 Divisions</span>
              </div>
            </div>
          </div>

          {/* Standards Compliance Note */}
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg text-xs text-blue-900 space-y-1">
            <div className="flex items-center font-bold">
              <CheckCircle2 className="w-4 h-4 mr-1 text-blue-600" />
              IRPWM 2020 Auto-Harmonization Active
            </div>
            <p className="text-[11px] text-blue-800">
              Incoming geometry values will automatically be cross-referenced against the 40 verified threshold rules in <code className="bg-white/80 px-1 py-0.5 rounded font-mono">irpwm_geometry_thresholds.csv</code> for standard classification (UML, NBML, PML).
            </p>
          </div>
        </div>

        {/* Right Column: Environmental Coupling & Weather Settings */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center space-x-2">
              <Compass className="w-5 h-5 text-indigo-600" />
              <h3 className="text-sm font-bold text-slate-900">
                Weather Data Coupling Controls
              </h3>
            </div>
            <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              Module Ready
            </span>
          </div>

          <p className="text-xs text-slate-600 leading-relaxed">
            Configure spatio-temporal validation rules. Railnex AI enforces strict decoupling: weather data is never merged with track defect records unless spatial proximity and temporal concurrence are mathematically satisfied.
          </p>

          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Maximum Spatial Coupling Radius</span>
                <span className="font-mono text-blue-600">{spatialRadius} km</span>
              </div>
              <input
                type="range"
                min="5"
                max="50"
                step="5"
                value={spatialRadius}
                onChange={(e) => setSpatialRadius(parseInt(e.target.value))}
                className="w-full accent-blue-600 cursor-pointer"
              />
              <span className="text-[10px] text-slate-400">
                Track segments outside this radius from an IMD weather station ignore environmental joins.
              </span>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Temporal Concurrence Window</span>
                <span className="font-mono text-blue-600">&plusmn;{temporalWindow} hours</span>
              </div>
              <input
                type="range"
                min="1"
                max="24"
                step="1"
                value={temporalWindow}
                onChange={(e) => setTemporalWindow(parseInt(e.target.value))}
                className="w-full accent-blue-600 cursor-pointer"
              />
              <span className="text-[10px] text-slate-400">
                Maximum time lag allowed between weather observation and track geometry inspection run.
              </span>
            </div>
          </div>

          <div className="pt-2">
            <button
              onClick={handleSave}
              className="w-full py-2 bg-slate-900 text-white rounded-lg text-xs font-bold hover:bg-slate-800 transition-colors flex items-center justify-center space-x-1.5"
            >
              <Save className="w-4 h-4" />
              <span>Save Environmental Parameters</span>
            </button>
            {savedNotice && (
              <p className="text-xs text-emerald-600 text-center font-medium mt-1">
                Configuration updated successfully!
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Research & Safety Governance Notice */}
      <div className="bg-slate-50 rounded-xl border border-slate-200 p-5 shadow-xs text-xs text-slate-600 space-y-2">
        <h4 className="font-bold text-slate-900 flex items-center">
          <Info className="w-4 h-4 mr-1.5 text-slate-500" />
          Statutory Compliance & Research Prototype Disclaimer
        </h4>
        <p className="leading-relaxed">
          Railnex AI is developed as an academic machine learning research and decision-support prototype. It is explicitly designed not to replace official Indian Railways inspection protocols, statutory Commissioner of Railway Safety (CRS) inquiries, or permanent way rules laid down in the Indian Railways Permanent Way Manual (IRPWM).
        </p>
        <p className="leading-relaxed">
          The software does not declare track sections officially safe or certified. It provides probabilistic severity estimation, transparent feature attribution, and prioritized review lists to assist qualified railway engineers in evidence-based maintenance planning.
        </p>
      </div>
    </div>
  );
};
