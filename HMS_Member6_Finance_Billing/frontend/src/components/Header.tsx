import React from 'react';
import { Building2, ShieldCheck, Calendar, IndianRupee, RefreshCw } from 'lucide-react';
import { Tenant } from '../types/finance';

interface HeaderProps {
  tenants: Tenant[];
  activeTenantId: string;
  onSelectTenant: (id: string) => void;
  integrityScore: number;
  periodName: string;
  onRefresh: () => void;
  isLoading: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  tenants,
  activeTenantId,
  onSelectTenant,
  integrityScore,
  periodName,
  onRefresh,
  isLoading
}) => {
  const currentTenant = tenants.find((t) => t.id === activeTenantId) || tenants[0];

  return (
    <header className="top-navbar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Building2 size={20} color="#38bdf8" />
          <span style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>Hospital Org:</span>
          <select
            className="form-control"
            style={{ width: 'auto', padding: '5px 10px', fontSize: '0.8125rem', fontWeight: 600 }}
            value={activeTenantId}
            onChange={(e) => onSelectTenant(e.target.value)}
          >
            {tenants.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name} ({t.default_currency})
              </option>
            ))}
          </select>
        </div>

        {currentTenant?.branches?.[0] && (
          <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', borderLeft: '1px solid var(--border-card)', paddingLeft: '12px' }}>
            Branch: <strong style={{ color: '#cbd5e1' }}>{currentTenant.branches[0].name}</strong> ({currentTenant.branches[0].city})
          </span>
        )}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        {/* Financial Period Pill */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            background: 'rgba(255, 255, 255, 0.05)',
            padding: '5px 12px',
            borderRadius: '6px',
            fontSize: '0.75rem',
            border: '1px solid var(--border-card)'
          }}
        >
          <Calendar size={14} color="#94a3b8" />
          <span style={{ color: 'var(--text-muted)' }}>Period:</span>
          <strong style={{ color: '#38bdf8' }}>{periodName || 'FY2026-M10 (OPEN)'}</strong>
        </div>

        {/* Financial Integrity Monitor Pill */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            background: integrityScore >= 90 ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
            padding: '5px 12px',
            borderRadius: '6px',
            fontSize: '0.75rem',
            border: `1px solid ${integrityScore >= 90 ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
            color: integrityScore >= 90 ? '#34d399' : '#f87171'
          }}
        >
          <ShieldCheck size={14} />
          <span>Integrity: <strong>{integrityScore}/100</strong></span>
        </div>

        {/* Currency Pill */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            background: 'rgba(2, 132, 199, 0.12)',
            padding: '5px 10px',
            borderRadius: '6px',
            fontSize: '0.75rem',
            border: '1px solid rgba(2, 132, 199, 0.3)',
            color: '#38bdf8'
          }}
        >
          <IndianRupee size={14} />
          <span>INR</span>
        </div>

        {/* Live Sync Refresh */}
        <button
          className="btn btn-outline btn-sm"
          onClick={onRefresh}
          disabled={isLoading}
          title="Sync with PostgreSQL / Django backend"
        >
          <RefreshCw size={14} className={isLoading ? 'spin' : ''} />
          <span>Sync</span>
        </button>
      </div>
    </header>
  );
};
