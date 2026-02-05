'use client';

import { useState, useEffect } from 'react';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

interface LayerConfig {
  name: string;
  rag_enabled: boolean;
  knowledge_sources: string[];
  confidence_threshold: number;
  description: string;
}

interface RAGConfig {
  global_rag_enabled: boolean;
  layers: {
    [key: string]: LayerConfig;
  };
}

export default function AdminDashboard() {
  const [apiKey, setApiKey] = useState<string>('');
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [config, setConfig] = useState<RAGConfig | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  // Check if API key is in sessionStorage
  useEffect(() => {
    const savedKey = sessionStorage.getItem('adminApiKey');
    if (savedKey) {
      setApiKey(savedKey);
      setIsAuthenticated(true);
      fetchConfig(savedKey);
    }
  }, []);

  const fetchConfig = async (key: string) => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${BACKEND_URL}/admin/rag/config`, {
        headers: {
          'X-Admin-Key': key
        }
      });

      if (response.status === 401 || response.status === 403) {
        setIsAuthenticated(false);
        sessionStorage.removeItem('adminApiKey');
        setError('Invalid API key');
        return;
      }

      if (!response.ok) {
        throw new Error('Failed to fetch config');
      }

      const data = await response.json();
      setConfig(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch config');
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = () => {
    if (!apiKey.trim()) {
      setError('Please enter API key');
      return;
    }
    sessionStorage.setItem('adminApiKey', apiKey);
    setIsAuthenticated(true);
    fetchConfig(apiKey);
  };

  const handleLogout = () => {
    sessionStorage.removeItem('adminApiKey');
    setIsAuthenticated(false);
    setApiKey('');
    setConfig(null);
  };

  const toggleLayer = async (layerNumber: number, enable: boolean) => {
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      const endpoint = enable ? 'enable' : 'disable';
      const response = await fetch(
        `${BACKEND_URL}/admin/rag/layer/${layerNumber}/${endpoint}`,
        {
          method: 'POST',
          headers: {
            'X-Admin-Key': apiKey
          }
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to ${endpoint} layer ${layerNumber}`);
      }

      setSuccess(`Layer ${layerNumber} ${enable ? 'enabled' : 'disabled'} successfully`);
      fetchConfig(apiKey);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Operation failed');
    } finally {
      setLoading(false);
    }
  };

  const updateThreshold = async (layerNumber: number, threshold: number) => {
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      const response = await fetch(
        `${BACKEND_URL}/admin/rag/layer/${layerNumber}/threshold?threshold=${threshold}`,
        {
          method: 'POST',
          headers: {
            'X-Admin-Key': apiKey
          }
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to update threshold`);
      }

      setSuccess(`Threshold updated for layer ${layerNumber}`);
      fetchConfig(apiKey);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Operation failed');
    } finally {
      setLoading(false);
    }
  };

  const toggleGlobal = async (enabled: boolean) => {
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      const response = await fetch(
        `${BACKEND_URL}/admin/rag/toggle-global?enabled=${enabled}`,
        {
          method: 'POST',
          headers: {
            'X-Admin-Key': apiKey
          }
        }
      );

      if (!response.ok) {
        throw new Error('Failed to toggle global RAG');
      }

      setSuccess(`Global RAG ${enabled ? 'enabled' : 'disabled'}`);
      fetchConfig(apiKey);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Operation failed');
    } finally {
      setLoading(false);
    }
  };

  // Login screen
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Admin Login</h1>
          <p className="text-sm text-gray-600 mb-4">
            Enter your admin API key to access the RAG configuration dashboard.
          </p>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
            placeholder="Admin API Key"
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent mb-4"
          />
          {error && (
            <div className="bg-red-50 text-red-700 px-4 py-2 rounded-md mb-4 text-sm">
              {error}
            </div>
          )}
          <button
            onClick={handleLogin}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition"
          >
            Login
          </button>
          <p className="mt-4 text-xs text-gray-500">
            Default API key for development: <code className="bg-gray-100 px-1 rounded">admin123</code>
          </p>
        </div>
      </div>
    );
  }

  // Main dashboard
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">RAG Admin Dashboard</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Main content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Alerts */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-4">
            {error}
          </div>
        )}
        {success && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-md mb-4">
            {success}
          </div>
        )}

        {loading && (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-2 text-gray-600">Loading...</p>
          </div>
        )}

        {config && !loading && (
          <>
            {/* Global toggle */}
            <div className="bg-white rounded-lg shadow p-6 mb-6">
              <h2 className="text-xl font-semibold mb-4">Global RAG Control</h2>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Global RAG Status</p>
                  <p className="text-sm text-gray-600">
                    {config.global_rag_enabled ? 'RAG is enabled for all layers' : 'RAG is disabled globally'}
                  </p>
                </div>
                <button
                  onClick={() => toggleGlobal(!config.global_rag_enabled)}
                  className={`px-6 py-2 rounded-md font-medium transition ${
                    config.global_rag_enabled
                      ? 'bg-green-600 text-white hover:bg-green-700'
                      : 'bg-red-600 text-white hover:bg-red-700'
                  }`}
                >
                  {config.global_rag_enabled ? 'Enabled' : 'Disabled'}
                </button>
              </div>
            </div>

            {/* Layers */}
            <div className="space-y-4">
              {Object.entries(config.layers).map(([layerKey, layer]) => {
                const layerNumber = parseInt(layerKey.replace('layer_', ''));
                return (
                  <div key={layerKey} className="bg-white rounded-lg shadow p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">
                          Layer {layerNumber}: {layer.name}
                        </h3>
                        <p className="text-sm text-gray-600 mt-1">{layer.description}</p>
                      </div>
                      <button
                        onClick={() => toggleLayer(layerNumber, !layer.rag_enabled)}
                        disabled={layerNumber === 1}
                        className={`px-4 py-2 rounded-md text-sm font-medium transition ${
                          layer.rag_enabled
                            ? 'bg-green-100 text-green-800 hover:bg-green-200'
                            : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                        } ${layerNumber === 1 ? 'opacity-50 cursor-not-allowed' : ''}`}
                      >
                        {layer.rag_enabled ? 'Enabled' : 'Disabled'}
                      </button>
                    </div>

                    {layer.rag_enabled && (
                      <>
                        {/* Knowledge sources */}
                        <div className="mb-4">
                          <p className="text-sm font-medium text-gray-700 mb-2">Knowledge Sources:</p>
                          <div className="flex flex-wrap gap-2">
                            {layer.knowledge_sources.map((source) => (
                              <span
                                key={source}
                                className="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                              >
                                {source}
                              </span>
                            ))}
                          </div>
                        </div>

                        {/* Confidence threshold */}
                        <div>
                          <div className="flex justify-between items-center mb-2">
                            <p className="text-sm font-medium text-gray-700">
                              Confidence Threshold: {layer.confidence_threshold.toFixed(2)}
                            </p>
                          </div>
                          <input
                            type="range"
                            min="0.5"
                            max="1.0"
                            step="0.05"
                            value={layer.confidence_threshold}
                            onChange={(e) => updateThreshold(layerNumber, parseFloat(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                          />
                          <div className="flex justify-between text-xs text-gray-500 mt-1">
                            <span>0.5 (Permissive)</span>
                            <span>1.0 (Strict)</span>
                          </div>
                        </div>
                      </>
                    )}
                  </div>
                );
              })}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
