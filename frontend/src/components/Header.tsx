import React from 'react';
import { TabType } from '../types';
import {
  Activity,
  AlertTriangle,
  BarChart3,
  Bot,
  Camera,
  CloudRain,
  Compass,
  Database,
  Layers,
  ListOrdered,
  Settings,
  ShieldCheck,
  TrendingDown
} from 'lucide-react';

interface HeaderProps {
  activeTab: TabType;
  onSelectTab: (tab: TabType) => void;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, onSelectTab }) => {
  const navItems: Array<{ id: TabType; label: string; icon: React.ReactNode }> = [
    { id: 'overview', label: 'Dashboard', icon: <BarChart3 className="w-4 h-4 mr-1.5" /> },
    { id: 'severity_prediction', label: 'AI Severity (4-Class)', icon: <AlertTriangle className="w-4 h-4 mr-1.5" /> },
    { id: 'maintenance_priority', label: 'Maintenance Priority', icon: <ListOrdered className="w-4 h-4 mr-1.5" /> },
    { id: 'track_analysis', label: 'Track Health & What-If', icon: <TrendingDown className="w-4 h-4 mr-1.5" /> },
    { id: 'cv_inspection', label: 'CV Defect Vision', icon: <Camera className="w-4 h-4 mr-1.5" /> },
    { id: 'usfd_analysis', label: 'USFD Flaw Analysis', icon: <Activity className="w-4 h-4 mr-1.5" /> },
    { id: 'weather_intelligence', label: 'Weather & Buckling', icon: <CloudRain className="w-4 h-4 mr-1.5" /> },
    { id: 'network_map', label: 'GIS Network Map', icon: <Compass className="w-4 h-4 mr-1.5" /> },
    { id: 'model_evaluation', label: 'Model Benchmarks', icon: <Layers className="w-4 h-4 mr-1.5" /> },
    { id: 'ai_assistant', label: 'AI Assistant', icon: <Bot className="w-4 h-4 mr-1.5" /> },
    { id: 'data_explorer', label: 'Data Explorer', icon: <Database className="w-4 h-4 mr-1.5" /> },
    { id: 'settings', label: 'Ingestion & Config', icon: <Settings className="w-4 h-4 mr-1.5" /> },
  ];

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-xs">
      {/* Top Brand Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-lg bg-blue-700 flex items-center justify-center text-white font-bold text-lg shadow-sm">
              🛡️
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xl font-bold tracking-tight text-slate-900">RAILRAKSHAK AI</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 font-semibold border border-blue-200">
                  INT395 Topic 20
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium">
                Intelligent Railway Track Defect Classification & Predictive Maintenance System
              </p>
            </div>
          </div>

          {/* Operational Status Badges */}
          <div className="hidden lg:flex items-center space-x-3 text-xs">
            <div className="flex items-center px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 font-medium">
              <ShieldCheck className="w-3.5 h-3.5 mr-1 text-emerald-600" />
              <span>13 Datasets Integrated (150k+ Records)</span>
            </div>
            <div className="flex items-center px-2.5 py-1 rounded-md bg-blue-50 text-blue-800 border border-blue-200 font-medium">
              <Activity className="w-3.5 h-3.5 mr-1 text-blue-600" />
              <span>Champion: LightGBM (Macro-F1: 99.5%)</span>
            </div>
            <div className="flex items-center px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 border border-slate-200 font-medium">
              <span>IRPWM 2020 & RDSO USFD Aligned</span>
            </div>
          </div>
        </div>

        {/* Horizontal Navigation Bar */}
        <nav className="flex space-x-1 overflow-x-auto py-1 scrollbar-none border-t border-slate-100">
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectTab(item.id)}
                className={`flex items-center px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors whitespace-nowrap ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                {item.icon}
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
};
