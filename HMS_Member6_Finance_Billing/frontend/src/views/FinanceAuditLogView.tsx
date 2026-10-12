import React, { useState, useEffect } from 'react';
import { FinancialAuditEvent } from '../types/finance';
import { api } from '../services/api';
import { History, Search, ShieldCheck } from 'lucide-react';

export const FinanceAuditLogView: React.FC = () => {
  const [events, setEvents] = useState<FinancialAuditEvent[]>([]);
  const [filterAction, setFilterAction] = useState('ALL');
  const [search, setSearch] = useState('');

  useEffect(() => {
    api.getAuditEvents().then(setEvents).catch(console.error);
  }, []);

  const filtered = events.filter((e) => {
    const matchAction = filterAction === 'ALL' || e.action_type === filterAction;
    const matchSearch =
      e.summary.toLowerCase().includes(search.toLowerCase()) ||
      e.actor_username.toLowerCase().includes(search.toLowerCase()) ||
      e.entity_id.toLowerCase().includes(search.toLowerCase());
    return matchAction && matchSearch;
  });

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1>Finance Audit Trail & Forensic Event Log</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Append-Only Immutable Records of Invoicing, Collections, Concessions, Journal Postings & Period Locks
          </p>
        </div>
      </div>

      {/* Filter Bar */}
      <div
        className="card"
        style={{
          padding: '14px 20px',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '16px'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1, maxWidth: '400px' }}>
          <Search size={16} color="var(--text-dim)" />
          <input
            type="text"
            className="form-control"
            placeholder="Search by Actor, Entity ID, Narrative..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {['ALL', 'INVOICE_ISSUED', 'PAYMENT_COLLECTED', 'REFUND_REQUESTED', 'JOURNAL_ENTRY_POSTED', 'FINANCIAL_PERIOD_CLOSED'].map((a) => (
            <button
              key={a}
              className={`btn btn-sm ${filterAction === a ? 'btn-primary' : 'btn-outline'}`}
              onClick={() => setFilterAction(a)}
            >
              {a.replace(/_/g, ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Actor / Officer</th>
              <th>Audit Action Type</th>
              <th>Target Entity</th>
              <th>Entity Identifier</th>
              <th>Audit Summary Narrative</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={6} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                  No audit events matching criteria.
                </td>
              </tr>
            ) : (
              filtered.map((ev) => (
                <tr key={ev.id}>
                  <td style={{ fontSize: '0.8125rem' }} className="mono-num">
                    {new Date(ev.created_at).toLocaleString()}
                  </td>
                  <td>
                    <strong style={{ color: '#38bdf8' }}>{ev.actor_username}</strong>
                  </td>
                  <td>
                    <span className="badge badge-neutral" style={{ fontSize: '0.6875rem' }}>
                      {ev.action_type}
                    </span>
                  </td>
                  <td>{ev.entity_name}</td>
                  <td className="mono-num" style={{ fontWeight: 600 }}>{ev.entity_id}</td>
                  <td style={{ fontSize: '0.8125rem', color: 'var(--text-main)' }}>{ev.summary}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
