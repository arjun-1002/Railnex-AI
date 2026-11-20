import React, { useState } from 'react';
import { TabType } from './types';
import { Header } from './components/Header';
import { ErrorBoundary } from './components/ErrorBoundary';
import { OverviewPage } from './pages/OverviewPage';
import { TrackAnalysisPage } from './pages/TrackAnalysisPage';
import { SeverityPredictionPage } from './pages/SeverityPredictionPage';
import { MaintenancePriorityPage } from './pages/MaintenancePriorityPage';
import { NetworkMapPage } from './pages/NetworkMapPage';
import { DataExplorerPage } from './pages/DataExplorerPage';
import { ModelEvaluationPage } from './pages/ModelEvaluationPage';
import { SettingsPage } from './pages/SettingsPage';
import { CvInspectionPage } from './pages/CvInspectionPage';
import { UsfdAnalysisPage } from './pages/UsfdAnalysisPage';
import { WeatherIntelligencePage } from './pages/WeatherIntelligencePage';
import { AssistantPage } from './pages/AssistantPage';

export function App() {
  const [activeTab, setActiveTab] = useState<TabType>('overview');

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans selection:bg-blue-100 selection:text-blue-900">
      {/* Top Fixed Horizontal Header */}
      <Header activeTab={activeTab} onSelectTab={setActiveTab} />

      {/* Main Content Viewport */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6 pb-12">
        <ErrorBoundary fallbackTitle="Module Viewport Error">
          {activeTab === 'overview' && <OverviewPage />}
          {activeTab === 'severity_prediction' && <SeverityPredictionPage />}
          {activeTab === 'maintenance_priority' && <MaintenancePriorityPage />}
          {activeTab === 'track_analysis' && <TrackAnalysisPage />}
          {activeTab === 'cv_inspection' && <CvInspectionPage />}
          {activeTab === 'usfd_analysis' && <UsfdAnalysisPage />}
          {activeTab === 'weather_intelligence' && <WeatherIntelligencePage />}
          {activeTab === 'network_map' && <NetworkMapPage />}
          {activeTab === 'model_evaluation' && <ModelEvaluationPage />}
          {activeTab === 'ai_assistant' && <AssistantPage />}
          {activeTab === 'data_explorer' && <DataExplorerPage />}
          {activeTab === 'settings' && <SettingsPage />}
        </ErrorBoundary>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-6 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-3">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-slate-900">RAILRAKSHAK AI</span>
            <span>&bull;</span>
            <span>B.Tech CSE (AI & ML) Supervised Learning (INT395) Topic 20</span>
          </div>

          <div className="flex items-center space-x-4">
            <span className="text-slate-400">Indian Railways Decision Support Platform</span>
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
