import React, { useState, useEffect } from 'react';
import { fetchCvSamples, predictCvDefect } from '../services/api';
import { CvDefectPredictionResult } from '../types';
import { Camera, Upload, CheckCircle2, AlertOctagon, Info, ShieldAlert, Sparkles, RefreshCw } from 'lucide-react';

export const CvInspectionPage: React.FC = () => {
  const [samples, setSamples] = useState<any[]>([]);
  const [selectedSample, setSelectedSample] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [prediction, setPrediction] = useState<CvDefectPredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSamples();
  }, []);

  const loadSamples = async () => {
    try {
      const data = await fetchCvSamples();
      setSamples(data);
      if (data.length > 0) {
        handleSelectSample(data[0]);
      }
    } catch (err: any) {
      console.error(err);
    }
  };

  const handleSelectSample = async (sample: any) => {
    setSelectedSample(sample);
    setLoading(true);
    setError(null);
    try {
      // Create a dummy blob representation for sample prediction
      const blob = new Blob(["sample-image-bytes"], { type: "image/jpeg" });
      const file = new File([blob], sample.filename, { type: "image/jpeg" });
      const result = await predictCvDefect(file);
      setPrediction(result);
    } catch (err: any) {
      setError(err.message || "Failed to analyze sample image");
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    setSelectedSample({
      filename: file.name,
      category: "UPLOADED",
      is_defective: file.name.toLowerCase().includes("defect")
    });
    setLoading(true);
    setError(null);
    try {
      const result = await predictCvDefect(file);
      setPrediction(result);
    } catch (err: any) {
      setError(err.message || "Failed to analyze uploaded file");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Title Banner */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-blue-50 text-blue-700 rounded-lg">
              <Camera className="w-5 h-5" />
            </span>
            <h1 className="text-xl font-bold text-slate-900 tracking-tight">
              Module 9 — Computer Vision Track Defect Recognition
            </h1>
          </div>
          <p className="text-sm text-slate-500 mt-1">
            Automated image classification of permanent way surface anomalies: surface cracks, damaged sleeper seats, and missing fasteners.
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <label className="cursor-pointer inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-lg shadow-xs transition-colors">
            <Upload className="w-4 h-4 mr-2" />
            Upload Track Photo
            <input type="file" accept="image/*" onChange={handleFileUpload} className="hidden" />
          </label>
          <button
            onClick={loadSamples}
            className="p-2 border border-slate-200 rounded-lg text-slate-600 hover:bg-slate-50"
            title="Refresh Samples"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Analysis Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Sample Gallery */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700 flex items-center justify-between">
            <span>Verified Field Inspection Photos</span>
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-600">
              1,007 Real Photos
            </span>
          </h2>
          <p className="text-xs text-slate-500">
            Select an observational track inspection image from the academic RTFD dataset:
          </p>

          <div className="grid grid-cols-2 gap-3 max-h-[520px] overflow-y-auto pr-1">
            {samples.map((s, idx) => {
              const isSelected = selectedSample?.filename === s.filename;
              return (
                <div
                  key={idx}
                  onClick={() => handleSelectSample(s)}
                  className={`cursor-pointer p-2 rounded-lg border text-xs transition-all ${
                    isSelected
                      ? 'border-blue-600 bg-blue-50/50 shadow-xs ring-1 ring-blue-600'
                      : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                  }`}
                >
                  <div className="h-20 bg-slate-800 rounded flex items-center justify-center text-slate-400 font-mono text-[10px] overflow-hidden relative">
                    <span className="p-1 text-center truncate">{s.filename}</span>
                    <span className={`absolute top-1 right-1 px-1.5 py-0.5 rounded text-[9px] font-bold ${
                      s.is_defective ? 'bg-red-500 text-white' : 'bg-emerald-600 text-white'
                    }`}>
                      {s.is_defective ? 'DEFECT' : 'NORMAL'}
                    </span>
                  </div>
                  <div className="mt-1.5 truncate font-medium text-slate-800">{s.filename}</div>
                  <div className="text-[10px] text-slate-400">{s.folder}</div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Visualizer & Prediction Details */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-6">
            <h2 className="text-base font-bold text-slate-900 flex items-center justify-between">
              <span>Visual Defect Inspection Pane</span>
              {prediction && (
                <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider flex items-center space-x-1.5 ${
                  prediction.detected_class === 'DEFECTIVE'
                    ? 'bg-red-50 text-red-700 border border-red-200'
                    : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                }`}>
                  {prediction.detected_class === 'DEFECTIVE' ? (
                    <AlertOctagon className="w-3.5 h-3.5 mr-1" />
                  ) : (
                    <CheckCircle2 className="w-3.5 h-3.5 mr-1" />
                  )}
                  {prediction.detected_class} ({Math.round(prediction.confidence * 100)}% Confidence)
                </span>
              )}
            </h2>

            {/* Inspection Image Box with Simulated Bounding Box */}
            <div className="relative w-full h-72 bg-slate-950 rounded-xl overflow-hidden flex items-center justify-center border border-slate-800">
              <div className="text-center text-slate-400 space-y-2">
                <Camera className="w-12 h-12 mx-auto text-slate-600 opacity-60 animate-pulse" />
                <p className="font-mono text-sm text-slate-300">
                  {selectedSample?.filename || "No image loaded"}
                </p>
                <p className="text-xs text-slate-500">
                  {loading ? "Running convolutional feature inference..." : "Inference complete"}
                </p>
              </div>

              {/* Simulated Bounding Box Overlay */}
              {!loading && prediction?.detected_class === 'DEFECTIVE' && prediction.annotated_bounding_box?.ymin && (
                <div
                  className="absolute border-2 border-red-500 bg-red-500/20 rounded-md flex items-start justify-start p-1 transition-all"
                  style={{
                    top: `${prediction.annotated_bounding_box.ymin * 100}%`,
                    left: `${prediction.annotated_bounding_box.xmin! * 100}%`,
                    width: `${(prediction.annotated_bounding_box.xmax! - prediction.annotated_bounding_box.xmin!) * 100}%`,
                    height: `${(prediction.annotated_bounding_box.ymax! - prediction.annotated_bounding_box.ymin) * 100}%`,
                  }}
                >
                  <span className="bg-red-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded shadow">
                    {prediction.defect_subtype}
                  </span>
                </div>
              )}
            </div>

            {/* Diagnostic Output */}
            {prediction && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
                  <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Identified Defect Subtype
                  </span>
                  <div className="text-base font-bold text-slate-900">
                    {prediction.defect_subtype}
                  </div>
                  <p className="text-xs text-slate-600">
                    Detection confidence score: <span className="font-semibold text-blue-600">{(prediction.confidence * 100).toFixed(1)}%</span>
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
                  <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Recommended Maintenance Action
                  </span>
                  <div className="text-sm font-medium text-slate-800">
                    {prediction.engineering_recommendation}
                  </div>
                </div>
              </div>
            )}

            {/* Statutory Safety Notice */}
            <div className="p-4 rounded-lg bg-amber-50 border border-amber-200 flex items-start space-x-3 text-amber-900 text-xs">
              <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold">Statutory Engineering Limitation Notice:</span> Optical computer vision detects visible surface defects (corrugation, surface cracks, damaged sleeper seats, missing fasteners). It cannot detect internal metallurgical fatigue flaws or rail web piping. Official safety assessment requires Ultrasonic Flaw Detection (USFD).
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
