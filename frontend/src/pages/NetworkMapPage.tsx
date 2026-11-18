import React, { useEffect, useState } from 'react';
import { StationItem } from '../types';
import { fetchStations, fetchZones } from '../services/api';
import {
  Compass,
  Database,
  Filter,
  Info,
  Layers,
  MapPin,
  Search,
  Train
} from 'lucide-react';

export const NetworkMapPage: React.FC = () => {
  const [stations, setStations] = useState<StationItem[]>([]);
  const [zones, setZones] = useState<any[]>([]);
  const [selectedZone, setSelectedZone] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedStation, setSelectedStation] = useState<StationItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadData();
  }, [selectedZone]);

  const loadData = () => {
    setLoading(true);
    Promise.all([fetchStations(selectedZone, 300), fetchZones()])
      .then(([stns, zns]) => {
        setStations(stns);
        setZones(zns);
        if (stns.length > 0 && !selectedStation) {
          setSelectedStation(stns[0]);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  };

  const filteredStations = stations.filter((s) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      s.station_code.toLowerCase().includes(q) ||
      s.station_name.toLowerCase().includes(q) ||
      (s.state && s.state.toLowerCase().includes(q))
    );
  });

  // Calculate SVG projection coordinates for Indian bounding box:
  // Lon: 68E to 98E -> X: 0 to 100%
  // Lat: 36N to 8N -> Y: 0 to 100%
  const projectCoords = (lon?: number, lat?: number) => {
    if (!lon || !lat) return { x: 50, y: 50 };
    const minLon = 68.0, maxLon = 97.0;
    const minLat = 8.0, maxLat = 37.0;
    const x = ((lon - minLon) / (maxLon - minLon)) * 100;
    const y = ((maxLat - lat) / (maxLat - minLat)) * 100;
    return { x: Math.max(2, Math.min(98, x)), y: Math.max(2, Math.min(98, y)) };
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Title & Guidance Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded text-xs font-bold uppercase bg-blue-100 text-blue-800">
                Spatial GIS Layer
              </span>
              <h2 className="text-lg font-bold text-slate-900">
                Indian Railways Network Geography & Station Infrastructure
              </h2>
            </div>
            <p className="text-xs sm:text-sm text-slate-600 mt-1">
              Geographic reference layout mapping 8,989 operational railway stations and 5,208 route corridors across all 17 Zonal Railways.
            </p>
          </div>

          <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200 text-xs text-slate-600 flex items-center space-x-2">
            <Info className="w-4 h-4 text-slate-400 shrink-0" />
            <span>Strict Verification: Defect locations are plotted only when verified GPS tags are present.</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Side: Interactive Geographic Map Canvas */}
        <div className="lg:col-span-8 bg-white rounded-xl border border-slate-200 p-5 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-2">
            <div className="flex items-center space-x-2">
              <Compass className="w-4 h-4 text-blue-600" />
              <h3 className="text-sm font-bold text-slate-900">
                Network Geographic Visualization (Subcontinent Projection)
              </h3>
            </div>
            <span className="text-xs text-slate-500 font-mono">
              Rendering {filteredStations.length} stations
            </span>
          </div>

          {/* SVG Map Container */}
          <div className="relative w-full h-[480px] bg-slate-900/95 rounded-xl overflow-hidden border border-slate-800 shadow-inner my-2 flex items-center justify-center">
            {/* Background Map Grid */}
            <div className="absolute inset-0 bg-[radial-gradient(#334155_1px,transparent_1px)] [background-size:16px_16px] opacity-40"></div>

            {/* Latitude/Longitude Guidelines */}
            <div className="absolute top-2 left-3 text-[10px] font-mono text-slate-500">
              37°N / 68°E (Jammu & Kashmir / Punjab / West)
            </div>
            <div className="absolute bottom-2 right-3 text-[10px] font-mono text-slate-500">
              8°N / 97°E (Kanyakumari / Assam / East)
            </div>

            {/* Render Station Coordinates as Interactive Nodes */}
            <svg className="w-full h-full absolute inset-0">
              {filteredStations.map((stn, idx) => {
                const pos = projectCoords(stn.longitude, stn.latitude);
                const isSelected = selectedStation?.station_code === stn.station_code;
                return (
                  <circle
                    key={stn.station_code || idx}
                    cx={`${pos.x}%`}
                    cy={`${pos.y}%`}
                    r={isSelected ? 6 : 2.5}
                    className={`cursor-pointer transition-all ${
                      isSelected
                        ? 'fill-amber-400 stroke-white stroke-2 drop-shadow-md'
                        : 'fill-blue-400/80 hover:fill-amber-300 hover:r-4'
                    }`}
                    onClick={() => setSelectedStation(stn)}
                  >
                    <title>{`${stn.station_name} (${stn.station_code}) - ${stn.zone || 'IR'}`}</title>
                  </circle>
                );
              })}
            </svg>

            {/* Overlay Station Details Tooltip */}
            {selectedStation && (
              <div className="absolute bottom-4 left-4 bg-slate-800/90 backdrop-blur-xs border border-slate-700 text-white rounded-lg p-3 max-w-xs shadow-lg text-xs pointer-events-none">
                <div className="flex items-center space-x-1.5 text-amber-400 font-bold">
                  <Train className="w-3.5 h-3.5" />
                  <span>{selectedStation.station_name}</span>
                  <span className="font-mono text-slate-300">({selectedStation.station_code})</span>
                </div>
                <div className="text-[11px] text-slate-300 mt-1 space-y-0.5">
                  <p>Zone: <strong className="text-white">{selectedStation.zone || 'N/A'}</strong></p>
                  <p>State: <strong className="text-white">{selectedStation.state || 'N/A'}</strong></p>
                  <p className="font-mono text-[10px] text-slate-400">
                    GPS: {selectedStation.latitude?.toFixed(4)}°N, {selectedStation.longitude?.toFixed(4)}°E
                  </p>
                </div>
              </div>
            )}
          </div>

          <div className="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-100">
            <span>Projection: Equirectangular India WGS-84</span>
            <span className="text-slate-400">Attribution: © OpenStreetMap contributors & DataMeet Community</span>
          </div>
        </div>

        {/* Right Side: Stations Roster & Zone Filter */}
        <div className="lg:col-span-4 bg-white rounded-xl border border-slate-200 p-5 shadow-xs flex flex-col justify-between space-y-4">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
              <h3 className="text-sm font-bold text-slate-900">Station Inspector</h3>
              <span className="text-xs font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700">
                {selectedZone === 'ALL' ? 'All 17 Zones' : `${selectedZone} Zone`}
              </span>
            </div>

            {/* Zone Selector */}
            <div className="mb-3">
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Filter by Railway Zone
              </label>
              <select
                value={selectedZone}
                onChange={(e) => setSelectedZone(e.target.value)}
                className="w-full px-3 py-1.5 text-xs rounded-lg border border-slate-200 bg-white font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="ALL">All Zonal Railways</option>
                {zones.map((z) => (
                  <option key={z.zone_code} value={z.zone_code}>
                    {z.zone_code} — {z.zone_name}
                  </option>
                ))}
              </select>
            </div>

            {/* Search Box */}
            <div className="relative mb-3">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Search station name or code..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 text-xs rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Station List */}
            <div className="h-72 overflow-y-auto space-y-1 pr-1 border border-slate-100 rounded-lg p-1">
              {filteredStations.map((stn) => {
                const isSelected = selectedStation?.station_code === stn.station_code;
                return (
                  <button
                    key={stn.station_code}
                    type="button"
                    onClick={() => setSelectedStation(stn)}
                    className={`w-full text-left p-2 rounded-lg text-xs transition-colors flex items-center justify-between ${
                      isSelected
                        ? 'bg-blue-50 border border-blue-200 text-blue-900 font-bold'
                        : 'hover:bg-slate-50 text-slate-700'
                    }`}
                  >
                    <div>
                      <div className="font-semibold text-slate-900">{stn.station_name}</div>
                      <div className="text-[10px] text-slate-400">{stn.state || 'India'}</div>
                    </div>
                    <span className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 font-bold">
                      {stn.station_code}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Selected Station Details Card */}
          {selectedStation && (
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-1.5">
              <div className="flex justify-between items-center">
                <span className="font-bold text-slate-900">{selectedStation.station_name}</span>
                <span className="font-mono text-xs px-2 py-0.5 rounded bg-blue-600 text-white font-bold">
                  {selectedStation.station_code}
                </span>
              </div>
              <p className="text-slate-600">
                Zone: <strong>{selectedStation.zone || 'Unclassified'}</strong> | State: <strong>{selectedStation.state}</strong>
              </p>
              <p className="font-mono text-[11px] text-slate-500">
                Latitude: {selectedStation.latitude?.toFixed(4)} | Longitude: {selectedStation.longitude?.toFixed(4)}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
