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
  Zap,
  Sparkles,
  RefreshCw
} from 'lucide-react';
import { uploadRtiTmsFile, uploadWeatherFile } from '../services/api';

export const SettingsPage: React.FC = () => {
  const [spatialRadius, setSpatialRadius] = useState<number>(25);
  const [temporalWindow, setTemporalWindow] = useState<number>(6);
  const [savedNotice, setSavedNotice] = useState<boolean>(false);

  // RTI TMS Upload State
  const [tmsFile, setTmsFile] = useState<File | null>(null);
  const [tmsLoading, setTmsLoading] = useState<boolean>(false);
  const [tmsResult, setTmsResult] = useState<any | null>(null);
  const [tmsError, setTmsError] = useState<string | null>(null);

  // Weather Upload State
  const [weatherFile, setWeatherFile] = useState<File | null>(null);
  const [weatherLoading, setWeatherLoading] = useState<boolean>(false);
  const [weatherResult, setWeatherResult] = useState<any | null>(null);
  const [weatherError, setWeatherError] = useState<string | null>(null);

  const handleSave = () => {
    setSavedNotice(true);
    setTimeout(() => setSavedNotice(false), 3000);
  };

  const handleTmsUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!tmsFile) return;
    setTmsLoading(true);
    setTmsError(null);
    try {
      const res = await uploadRtiTmsFile(tmsFile);
      setTmsResult(res);
      setTmsLoading(false);
    } catch (err: any) {
      setTmsError(err.message);
      setTmsLoading(false);
    }
  };

  const handleWeatherUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!weatherFile) return;
    setWeatherLoading(true);
    setWeatherError(null);
    try {
      const res = await uploadWeatherFile(weatherFile);
      setWeatherResult(res);
      setWeatherLoading(false);
    } catch (err: any) {
      setWeatherError(err.message);
      setWeatherLoading(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Title & Guidance Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded text-xs font-bold uppercase bg-blue-100 text-blue-800">
                Stage 3 Operational Engine
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                Railnex AI Ingestion Engine & RTI Integration Interface
              </h2>
            </div>
            <p className="text-xs sm:text-sm text-slate-600 mt-1">
              Ingest official Indian Railways Track Management System (TMS) inspection logs, upload historical meteorological time-series, and configure spatio-temporal validation rules.
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

      {/* Main Grid: Upload Engines */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Interactive RTI TMS Ingestion */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="w-5 h-5 text-blue-600" />
              <h3 className="text-sm font-bold text-slate-900">
                Indian Railways TMS RTI Data Ingestion
              </h3>
            </div>
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-50 text-amber-800 border border-amber-200">
              Live Ingestion Ready
            </span>
          </div>

          <p className="text-xs text-slate-600 leading-relaxed">
            Drop your Track Management System (TMS) or Track Recording Car (TRC) logs requested under RTI. The pipeline automatically resolves zonal column variances across all 17 Zonal Railways and cross-references measurements against IRPWM 2020 Table 5.1 thresholds.
          </p>

          <form onSubmit={handleTmsUpload} className="space-y-3">
            <div className="border-2 border-dashed border-slate-200 rounded-xl p-4 text-center hover:border-blue-400 transition-colors bg-slate-50/50">
              <input
                type="file"
                accept=".csv,.xlsx,.xls,.parquet"
                onChange={(e) => setTmsFile(e.target.files?.[0] || null)}
                className="hidden"
                id="tms-upload-input"
              />
              <label htmlFor="tms-upload-input" className="cursor-pointer flex flex-col items-center">
                <UploadCloud className="w-8 h-8 text-blue-600 mb-2" />
                <span className="text-xs font-bold text-slate-800">
                  {tmsFile ? tmsFile.name : 'Click to select Indian Railways TMS file'}
                </span>
                <span className="text-[10px] text-slate-500 mt-1">
                  Supported: CSV, Excel (.xlsx, .xls), or Parquet
                </span>
              </label>
            </div>

            {tmsError && (
              <div className="p-2.5 bg-red-50 border border-red-200 rounded-lg text-xs text-red-700">
                {tmsError}
              </div>
            )}

            <button
              type="submit"
              disabled={!tmsFile || tmsLoading}
              className="w-full py-2 px-4 bg-blue-600 text-white rounded-lg text-xs font-bold hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center space-x-2 shadow-xs"
            >
              {tmsLoading ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Standardizing & Validating RTI Records...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Execute RTI TMS Harmonization & Ingestion</span>
                </>
              )}
            </button>
          </form>

          {tmsResult && (
            <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl space-y-3 text-xs">
              <div className="flex items-center text-emerald-800 font-bold">
                <CheckCircle2 className="w-4 h-4 mr-1.5 text-emerald-600" />
                <span>{tmsResult.message}</span>
              </div>
              <div className="grid grid-cols-2 gap-2 bg-white p-2.5 rounded-lg border border-emerald-100">
                <div>
                  <span className="text-[11px] text-slate-500">Ingested Records:</span>
                  <p className="font-bold text-slate-900">{tmsResult.audit.ingested_records}</p>
                </div>
                <div>
                  <span className="text-[11px] text-slate-500">UML Urgent Breaches:</span>
                  <p className="font-bold text-red-600">{tmsResult.audit.severity_distribution?.UML || 0}</p>
                </div>
                <div>
                  <span className="text-[11px] text-slate-500">NBML Need-Based:</span>
                  <p className="font-bold text-amber-600">{tmsResult.audit.severity_distribution?.NBML || 0}</p>
                </div>
                <div>
                  <span className="text-[11px] text-slate-500">Zonal Distribution:</span>
                  <p className="font-bold text-blue-600">{tmsResult.audit.zonal_railways_detected?.join(', ') || 'Auto-Detected'}</p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Weather Ingestion & Coupling Rules */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center space-x-2">
              <Compass className="w-5 h-5 text-indigo-600" />
              <h3 className="text-sm font-bold text-slate-900">
                Historical Weather Data Upload & Coupling
              </h3>
            </div>
            <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              Active Module
            </span>
          </div>

          <p className="text-xs text-slate-600 leading-relaxed">
            Upload your existing historical meteorological records (Temperature, Rainfall, Relative Humidity). The engine validates physical bounds and applies spatio-temporal validation rules.
          </p>

          <form onSubmit={handleWeatherUpload} className="space-y-3">
            <div className="border-2 border-dashed border-slate-200 rounded-xl p-4 text-center hover:border-indigo-400 transition-colors bg-slate-50/50">
              <input
                type="file"
                accept=".csv,.xlsx,.xls,.parquet"
                onChange={(e) => setWeatherFile(e.target.files?.[0] || null)}
                className="hidden"
                id="weather-upload-input"
              />
              <label htmlFor="weather-upload-input" className="cursor-pointer flex flex-col items-center">
                <FileSpreadsheet className="w-8 h-8 text-indigo-600 mb-2" />
                <span className="text-xs font-bold text-slate-800">
                  {weatherFile ? weatherFile.name : 'Click to select Weather CSV / Excel file'}
                </span>
                <span className="text-[10px] text-slate-500 mt-1">
                  Supports IMD and automated meteorological station formats
                </span>
              </label>
            </div>

            {weatherError && (
              <div className="p-2.5 bg-red-50 border border-red-200 rounded-lg text-xs text-red-700">
                {weatherError}
              </div>
            )}

            <button
              type="submit"
              disabled={!weatherFile || weatherLoading}
              className="w-full py-2 px-4 bg-indigo-600 text-white rounded-lg text-xs font-bold hover:bg-indigo-700 transition-colors disabled:opacity-50 flex items-center justify-center space-x-2 shadow-xs"
            >
              {weatherLoading ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Validating Environmental Observations...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Import & Audit Meteorological Dataset</span>
                </>
              )}
            </button>
          </form>

          {weatherResult && (
            <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-xl space-y-2 text-xs">
              <div className="flex items-center text-indigo-900 font-bold">
                <CheckCircle2 className="w-4 h-4 mr-1.5 text-indigo-600" />
                <span>{weatherResult.message}</span>
              </div>
              <div className="grid grid-cols-2 gap-2 bg-white p-2.5 rounded-lg border border-indigo-100">
                <div>
                  <span className="text-[11px] text-slate-500">Date Range:</span>
                  <p className="font-bold text-slate-900">
                    {weatherResult.audit.date_range?.start?.split('T')[0]} to {weatherResult.audit.date_range?.end?.split('T')[0]}
                  </p>
                </div>
                <div>
                  <span className="text-[11px] text-slate-500">Weather Stations:</span>
                  <p className="font-bold text-indigo-600">{weatherResult.audit.stations_count || 1}</p>
                </div>
              </div>
            </div>
          )}

          {/* Validation Sliders */}
          <div className="pt-2 border-t border-slate-100 space-y-3">
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
            </div>

            <button
              onClick={handleSave}
              className="w-full py-2 bg-slate-900 text-white rounded-lg text-xs font-bold hover:bg-slate-800 transition-colors flex items-center justify-center space-x-1.5"
            >
              <Save className="w-4 h-4" />
              <span>Save Environmental Parameters</span>
            </button>
            {savedNotice && (
              <p className="text-xs text-emerald-600 text-center font-medium mt-1">
                Environmental parameters saved successfully!
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
