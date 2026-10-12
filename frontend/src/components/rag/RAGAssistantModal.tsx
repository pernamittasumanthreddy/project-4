'use client';
import React, { useState, useRef, useEffect } from 'react';
import { UserProfile } from '@/lib/types/roles';
import { ROLE_CONFIGS } from '@/lib/data/roleConfigs';
import { RAGQueryResult, Citation, HospitalDocument } from '@/lib/types/rag';
import { DocumentViewerModal } from './DocumentViewerModal';
import { HOSPITAL_DOCUMENTS } from '@/lib/data/hospitalDocuments';
import { 
  X, Send, Sparkles, BookOpen, ShieldCheck, CheckCircle2, 
  ExternalLink, ThumbsUp, ThumbsDown, Clock, AlertTriangle, 
  Bot, RefreshCw, FileText, ChevronRight, Copy, Check 
} from 'lucide-react';

interface RAGAssistantModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentUser: UserProfile;
}

interface MessageHistoryItem {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
  result?: RAGQueryResult;
  originalQuery?: string;
}

export const RAGAssistantModal: React.FC<RAGAssistantModalProps> = ({ isOpen, onClose, currentUser }) => {
  const roleConfig = ROLE_CONFIGS[currentUser.role] || ROLE_CONFIGS['DOCTOR'];
  const [messages, setMessages] = useState<MessageHistoryItem[]>([]);
  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [selectedDocToView, setSelectedDocToView] = useState<HospitalDocument | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize role-specific welcome message when opened
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: 'msg-welcome',
          sender: 'assistant',
          text: `Welcome, ${currentUser.name}. I am your dedicated **${roleConfig.ragTitle}**.\n\nI provide strictly verified answers grounded in CityCare's approved clinical protocols, departmental SOPs, formulary guidelines, and administrative policies authorized for **${currentUser.department}**.\n\n*Clinical Safety Guardrail: I do not autonomously diagnose patients or prescribe medications.*`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    }
  }, [currentUser, roleConfig, messages.length]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (queryText?: string) => {
    const query = (queryText || inputQuery).trim();
    if (!query || loading) return;

    const userMsg: MessageHistoryItem = {
      id: `usr-${Date.now()}`,
      sender: 'user',
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      originalQuery: query
    };

    setMessages(prev => [...prev, userMsg]);
    setInputQuery('');
    setLoading(true);

    try {
      const res = await fetch('/api/rag/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: query,
          role: currentUser.role,
          userId: currentUser.id
        })
      });

      const data: RAGQueryResult = await res.json();

      const assistantMsg: MessageHistoryItem = {
        id: `asst-${Date.now()}`,
        sender: 'assistant',
        text: data.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        result: data,
        originalQuery: query
      };

      setMessages(prev => [...prev, assistantMsg]);
    } catch (e) {
      setMessages(prev => [
        ...prev,
        {
          id: `asst-err-${Date.now()}`,
          sender: 'assistant',
          text: "I couldn't find this information in the hospital's approved documents.",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          originalQuery: query
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleRegenerate = (originalQuery?: string) => {
    if (originalQuery) {
      handleSend(originalQuery);
    }
  };

  const handleViewSource = (citation: Citation) => {
    const doc = HOSPITAL_DOCUMENTS.find(d => d.id === citation.documentId);
    if (doc) {
      setSelectedDocToView(doc);
    } else {
      setSelectedDocToView({
        id: citation.documentId,
        title: citation.documentTitle,
        category: citation.category,
        department: currentUser.department,
        version: citation.version,
        effectiveDate: citation.lastUpdated,
        lastUpdated: citation.lastUpdated,
        confidentiality: 'INTERNAL',
        roleAccess: [currentUser.role],
        fileType: 'PDF',
        fileSize: '1.4 MB',
        sourceUri: `/documents/${citation.documentId.toLowerCase()}.pdf`,
        isArchived: false,
        content: citation.snippet,
        sections: [
          {
            heading: citation.section,
            page: citation.pageNumber || 1,
            text: citation.snippet
          }
        ]
      });
    }
  };

  if (!isOpen) return null;

  return (
    <>
      <div className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-xs flex justify-end animate-in fade-in duration-200">
        <div className="w-full max-w-2xl bg-white h-full shadow-2xl flex flex-col border-l border-slate-200 animate-in slide-in-from-right duration-300 text-slate-800">
          
          {/* Header */}
          <div className="p-4 border-b border-slate-200 bg-slate-900 text-white flex items-start justify-between shrink-0">
            <div className="flex items-start gap-3">
              <div className="p-2.5 bg-blue-600 rounded-lg text-white mt-0.5 shadow-2xs">
                <Bot className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 uppercase tracking-wider border border-blue-400/30">
                    CityCare Knowledge Assistant
                  </span>
                  <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                    {currentUser.department}
                  </span>
                </div>
                <h2 className="text-sm font-bold text-white mt-1 leading-snug">
                  {roleConfig.ragTitle}
                </h2>
                <p className="text-[11px] text-slate-400 mt-0.5">
                  Logged in as <strong className="text-slate-200">{currentUser.name}</strong> ({roleConfig.displayName})
                </p>
              </div>
            </div>

            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
              title="Close RAG Assistant"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Scope Banner */}
          <div className="px-4 py-2 bg-slate-50 border-b border-slate-200 flex items-center justify-between text-xs shrink-0">
            <div className="flex items-center gap-2 text-slate-700 font-medium truncate max-w-md">
              <BookOpen className="w-3.5 h-3.5 text-blue-600 shrink-0" />
              <span className="truncate"><strong>Authorized Scope:</strong> {roleConfig.knowledgeScopeDescription}</span>
            </div>
            <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold shrink-0">
              RBAC Verified
            </span>
          </div>

          {/* Messages Feed */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50/50">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
              >
                {msg.sender === 'user' ? (
                  <div className="bg-blue-600 text-white rounded-xl rounded-tr-xs px-3.5 py-2.5 max-w-[85%] text-xs shadow-2xs">
                    <p className="leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                    <span className="text-[10px] text-blue-200 block text-right mt-1 font-mono">{msg.timestamp}</span>
                  </div>
                ) : (
                  <div className="bg-white border border-slate-200 rounded-xl rounded-tl-xs p-4 max-w-[95%] shadow-2xs space-y-3">
                    
                    {/* Grounding Header Badge */}
                    <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                      <div className="flex items-center gap-1.5 text-emerald-700 font-semibold text-xs">
                        <ShieldCheck className="w-4 h-4 text-emerald-600" />
                        <span>Based on CityCare Approved Documents</span>
                      </div>
                      {msg.result && (
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                          msg.result.confidenceLevel === 'High' ? 'bg-emerald-50 text-emerald-800 border-emerald-200' :
                          msg.result.confidenceLevel === 'Moderate' ? 'bg-amber-50 text-amber-800 border-amber-200' : 'bg-slate-100 text-slate-700 border-slate-200'
                        }`}>
                          {Math.round(msg.result.confidenceScore * 100)}% Grounded ({msg.result.confidenceLevel})
                        </span>
                      )}
                    </div>

                    {/* Grounded Answer Content */}
                    <div className="text-xs text-slate-800 leading-relaxed whitespace-pre-line">
                      {msg.text}
                    </div>

                    {/* Safety Notice if needed */}
                    {msg.result?.safetyNotice && (
                      <div className="p-2.5 bg-amber-50 border border-amber-200 rounded-lg flex items-start gap-2 text-xs text-amber-900">
                        <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                        <div>
                          <strong>Clinical Advisory Notice:</strong>
                          <p className="mt-0.5 text-[11px]">{msg.result.safetyNotice}</p>
                        </div>
                      </div>
                    )}

                    {/* Grounded Sources & Citations */}
                    {msg.result?.citations && msg.result.citations.length > 0 && (
                      <div className="mt-3 pt-2.5 border-t border-slate-100 space-y-2">
                        <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                          <FileText className="w-3.5 h-3.5 text-blue-600" /> Grounded Source Documents ({msg.result.citations.length})
                        </p>
                        <div className="space-y-1.5">
                          {msg.result.citations.map((cite, idx) => (
                            <div
                              key={idx}
                              className="bg-slate-50 hover:bg-blue-50/50 border border-slate-200 rounded-lg p-2.5 transition-colors text-xs flex items-start justify-between gap-3"
                            >
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2">
                                  <span className="font-semibold text-slate-900 truncate">
                                    📄 {cite.documentTitle}
                                  </span>
                                  <span className="text-[10px] bg-slate-200 text-slate-700 px-1.5 py-0.2 rounded font-mono">
                                    {cite.version}
                                  </span>
                                </div>
                                <div className="text-slate-500 text-[11px] mt-0.5">
                                  Section: <span className="font-medium text-slate-700">&quot;{cite.section}&quot;</span> • Page {cite.pageNumber || 1} • Updated {cite.lastUpdated}
                                </div>
                                <p className="text-slate-600 italic text-[11px] mt-1 bg-white p-1.5 rounded border border-slate-100 truncate">
                                  &quot;{cite.snippet}&quot;
                                </p>
                              </div>

                              <button
                                onClick={() => handleViewSource(cite)}
                                className="px-2 py-1 bg-white border border-slate-200 rounded text-blue-700 hover:text-blue-900 hover:bg-slate-50 font-semibold flex items-center gap-1 text-[11px] shrink-0 shadow-2xs transition-colors"
                              >
                                View Doc <ExternalLink className="w-3 h-3" />
                              </button>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Action Bar: Copy, Regenerate, Feedback */}
                    <div className="flex items-center justify-between pt-2 border-t border-slate-100 text-[11px] text-slate-400">
                      <div className="flex items-center gap-2">
                        <span className="font-mono">{msg.timestamp}</span>
                        {msg.result && <span>• {msg.result.totalLatencyMs}ms</span>}
                      </div>

                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleCopy(msg.id, msg.text)}
                          className="flex items-center gap-1 text-slate-500 hover:text-blue-700 transition-colors"
                          title="Copy Answer"
                        >
                          {copiedId === msg.id ? (
                            <>
                              <Check className="w-3 h-3 text-emerald-600" />
                              <span className="text-emerald-600 font-semibold">Copied</span>
                            </>
                          ) : (
                            <>
                              <Copy className="w-3 h-3" />
                              <span>Copy</span>
                            </>
                          )}
                        </button>

                        {msg.originalQuery && (
                          <button
                            onClick={() => handleRegenerate(msg.originalQuery)}
                            className="flex items-center gap-1 text-slate-500 hover:text-blue-700 transition-colors"
                            title="Regenerate Grounded Query"
                          >
                            <RefreshCw className="w-3 h-3" />
                            <span>Regenerate</span>
                          </button>
                        )}

                        <div className="flex items-center gap-1 pl-2 border-l border-slate-200">
                          <button
                            onClick={() => alert('Feedback logged: Answer Verified Accurate')}
                            className="p-1 hover:text-emerald-600 rounded transition-colors"
                            title="Helpful / Grounded"
                          >
                            <ThumbsUp className="w-3 h-3" />
                          </button>
                          <button
                            onClick={() => alert('Feedback logged: Flagged for Document Review')}
                            className="p-1 hover:text-rose-600 rounded transition-colors"
                            title="Inaccurate / Missing Documentation"
                          >
                            <ThumbsDown className="w-3 h-3" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex items-center gap-2 p-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-600 max-w-sm shadow-2xs">
                <RefreshCw className="w-4 h-4 animate-spin text-blue-600" />
                <span>Searching authorized documents & synthesizing response...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Suggested Role Queries */}
          <div className="p-3 bg-slate-50 border-t border-slate-200 shrink-0">
            <p className="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1.5 flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-amber-500" /> Suggested for {roleConfig.displayName}:
            </p>
            <div className="flex flex-wrap gap-1.5 max-h-20 overflow-y-auto">
              {roleConfig.suggestedQuestions.map((q, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSend(q)}
                  disabled={loading}
                  className="text-left text-xs bg-white hover:bg-blue-50 text-slate-700 hover:text-blue-700 border border-slate-200 rounded-md px-2 py-1 transition-colors truncate max-w-full font-medium"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>

          {/* Input Footer */}
          <div className="p-3.5 bg-white border-t border-slate-200 shrink-0">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="flex items-center gap-2"
            >
              <input
                type="text"
                value={inputQuery}
                onChange={(e) => setInputQuery(e.target.value)}
                placeholder={`Ask ${roleConfig.ragTitle}...`}
                disabled={loading}
                className="flex-1 px-3.5 py-2 bg-slate-50 border border-slate-300 rounded-lg text-xs focus:outline-hidden focus:ring-2 focus:ring-blue-600 focus:bg-white transition-all text-slate-900 placeholder:text-slate-400"
              />
              <button
                type="submit"
                disabled={loading || !inputQuery.trim()}
                className="px-3.5 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-200 disabled:text-slate-400 text-white rounded-lg transition-colors font-bold text-xs flex items-center gap-1 shadow-2xs"
              >
                <span>Query</span>
                <Send className="w-3.5 h-3.5" />
              </button>
            </form>
            <div className="mt-1.5 text-[10px] text-slate-400 text-center">
              Strictly grounded on hospital documents. Patient records isolated by role permissions.
            </div>
          </div>
        </div>
      </div>

      {/* Document Viewer Modal */}
      <DocumentViewerModal
        document={selectedDocToView}
        onClose={() => setSelectedDocToView(null)}
      />
    </>
  );
};
