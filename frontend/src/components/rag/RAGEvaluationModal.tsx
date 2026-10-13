'use client';
import React, { useEffect, useState } from 'react';
import { RAGEvaluationMetrics } from '@/lib/types/rag';
import { RAGEngine } from '@/lib/rag/ragEngine';
import { X, Award, CheckCircle2, ShieldAlert, Cpu, Database, Activity, RefreshCw } from 'lucide-react';

interface RAGEvaluationModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const RAGEvaluationModal: React.FC<RAGEvaluationModalProps> = ({ isOpen, onClose }) => {
  const [metrics, setMetrics] = useState<RAGEvaluationMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchMetrics = async () => {
    setLoading(true);
    try {
      const ragEngine = RAGEngine.getInstance();
      const data = ragEngine.getEvaluator().getMetrics();
      setMetrics(data);
    } catch (e) {
      console.error('Failed to load metrics', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchMetrics();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-in fade-in duration-200">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-5xl max-h-[92vh] flex flex-col overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200 bg-slate-900 text-white flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-blue-600 rounded-lg text-white">
              <Award className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold px-2 py-0.5 rounded bg-blue-800 text-blue-200 uppercase tracking-wider">
                  Audit & Benchmark Console
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 font-semibold flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3" /> 0% Hallucination Policy
                </span>
              </div>
              <h2 className="text-base font-bold text-white mt-1">Multi-RAG Grounding & Evaluation Benchmark</h2>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={fetchMetrics}
              className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
              title="Refresh Metrics"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={onClose}
              className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {loading || !metrics ? (
            <div className="py-20 text-center text-slate-500 flex flex-col items-center">
              <RefreshCw className="w-8 h-8 animate-spin text-blue-600 mb-2" />
              <p className="text-sm">Calculating grounded RAG evaluation metrics across 15 hospital roles...</p>
            </div>
          ) : (
            <>
              {/* Primary 4 Benchmark Cards */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                  <div className="flex items-center justify-between text-xs text-slate-500 font-medium">
                    <span>Retrieval Accuracy</span>
                    <Database className="w-4 h-4 text-blue-600" />
                  </div>
                  <div className="text-3xl font-extrabold text-slate-900 mt-2">{metrics.retrievalAccuracy}%</div>
                  <div className="text-xs text-emerald-600 mt-1 font-semibold">Precision@K: {metrics.precisionAtK} | Recall: {metrics.recallAtK}</div>
                </div>

                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                  <div className="flex items-center justify-between text-xs text-slate-500 font-medium">
                    <span>Faithfulness Score</span>
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  </div>
                  <div className="text-3xl font-extrabold text-emerald-600 mt-2">{metrics.faithfulnessScore}%</div>
                  <div className="text-xs text-slate-500 mt-1 font-medium">Zero unsupported claims in hospital clinical testbed</div>
                </div>

                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                  <div className="flex items-center justify-between text-xs text-slate-500 font-medium">
                    <span>Hallucination Rate</span>
                    <ShieldAlert className="w-4 h-4 text-emerald-600" />
                  </div>
                  <div className="text-3xl font-extrabold text-emerald-700 mt-2">{metrics.hallucinationRate}%</div>
                  <div className="text-xs text-slate-500 mt-1 font-medium">Strict "Not in approved docs" fallback enforced</div>
                </div>

                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                  <div className="flex items-center justify-between text-xs text-slate-500 font-medium">
                    <span>Average Latency</span>
                    <Cpu className="w-4 h-4 text-purple-600" />
                  </div>
                  <div className="text-3xl font-extrabold text-slate-900 mt-2">{metrics.averageLatencyMs}ms</div>
                  <div className="text-xs text-slate-500 mt-1 font-medium">BM25 + Vector Cosine + RRF Hybrid Pipeline</div>
                </div>
              </div>

              {/* Secondary Metrics Strip */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-blue-50/70 border border-blue-100 rounded-xl text-xs text-slate-700">
                <div>
                  <span className="text-slate-500 block">MRR (Mean Reciprocal Rank):</span>
                  <span className="font-bold text-slate-900 text-sm">{metrics.mrr}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Answer Relevance:</span>
                  <span className="font-bold text-slate-900 text-sm">{metrics.answerRelevance}%</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Citation Accuracy:</span>
                  <span className="font-bold text-slate-900 text-sm">{metrics.citationAccuracy}%</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Total Audited Queries:</span>
                  <span className="font-bold text-slate-900 text-sm">{metrics.totalQueriesEvaluated}</span>
                </div>
              </div>

              {/* Breakdown tables */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Top Categories */}
                <div className="bg-white border border-slate-200 rounded-xl p-5">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-1.5">
                    <Activity className="w-4 h-4 text-blue-600" /> Top Queried Document Categories
                  </h3>
                  <div className="space-y-2.5">
                    {metrics.topQueriedCategories.map((cat, i) => (
                      <div key={i} className="flex items-center justify-between text-xs">
                        <span className="text-slate-700 font-medium truncate max-w-[260px]">{cat.category}</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-slate-100 rounded-full h-2 overflow-hidden">
                            <div
                              className="bg-blue-600 h-full rounded-full"
                              style={{ width: `${Math.min(100, (cat.count / 100) * 100)}%` }}
                            />
                          </div>
                          <span className="font-mono text-slate-500 font-semibold">{cat.count}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Most Retrieved Documents */}
                <div className="bg-white border border-slate-200 rounded-xl p-5">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-1.5">
                    <Database className="w-4 h-4 text-emerald-600" /> Most Retrieved SOP Documents
                  </h3>
                  <div className="space-y-2.5">
                    {metrics.mostRetrievedDocuments.map((doc, i) => (
                      <div key={i} className="flex items-center justify-between text-xs">
                        <span className="text-slate-700 font-medium truncate max-w-[260px]">{doc.title}</span>
                        <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200 font-mono font-bold">
                          {doc.count} hits
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Role Isolation Distribution */}
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-600 mb-3">
                  Query Volume Distribution by Role (RBAC Sandboxed)
                </h4>
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-3">
                  {Object.entries(metrics.queriesPerRole).map(([role, count]) => (
                    <div key={role} className="bg-white border border-slate-200 p-2.5 rounded-lg text-center">
                      <div className="text-[10px] font-bold text-slate-500 truncate">{role}</div>
                      <div className="text-lg font-bold text-slate-900 mt-0.5">{count}</div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 flex items-center justify-between text-xs text-slate-500">
          <span>RAG Evaluation Protocol: Grounded Reciprocal Rank Fusion + Strict Context Injection</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors font-medium"
          >
            Close Evaluation Console
          </button>
        </div>
      </div>
    </div>
  );
};
