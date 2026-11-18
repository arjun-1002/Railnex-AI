import React, { useState } from 'react';
import { TabType } from './types';
import { Header } from './components/Header';
import { OverviewPage } from './pages/OverviewPage';
import { TrackAnalysisPage } from './pages/TrackAnalysisPage';
import { SeverityPredictionPage } from './pages/SeverityPredictionPage';
import { MaintenancePriorityPage } from './pages/MaintenancePriorityPage';
import { NetworkMapPage } from './pages/NetworkMapPage';
import { DataExplorerPage } from './pages/DataExplorerPage';
import { ModelEvaluationPage } from './pages/ModelEvaluationPage';
import { SettingsPage } from './pages/SettingsPage';

export function App() {
  const [activeTab, setActiveTab] = useState<TabType>('overview');

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans selection:bg-blue-100 selection:text-blue-900">
      {/* Top Fixed Horizontal Header */}
      <Header activeTab={activeTab} onSelectTab={setActiveTab} />

      {/* Main Content Viewport */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        {activeTab === 'overview' && <OverviewPage />}
        {activeTab === 'track_analysis' && <TrackAnalysisPage />}
        {activeTab === 'severity_prediction' && <SeverityPredictionPage />}
        {activeTab === 'maintenance_priority' && <MaintenancePriorityPage />}
        {activeTab === 'network_map' && <NetworkMapPage />}
        {activeTab === 'data_explorer' && <DataExplorerPage />}
        {activeTab === 'model_evaluation' && <ModelEvaluationPage />}
        {activeTab === 'settings' && <SettingsPage />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-6 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-3">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-slate-900">RAILNEX AI</span>
            <span>&bull;</span>
            <span>Railway Track Defect Severity Classification & Maintenance Prioritization System</span>
          </div>

          <div className="flex items-center space-x-4">
            <span className="text-slate-400">Academic Research Decision Support</span>
            <span>&bull;</span>
            <a
              href="https://github.com/arjun-1002/Railnex-AI.git"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              GitHub: arjun-1002/Railnex-AI
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
