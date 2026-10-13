import React from 'react';
import {
  LayoutDashboard,
  FileText,
  Clock,
  CreditCard,
  RotateCcw,
  GitCompare,
  ShieldAlert,
  FileCheck2,
  Percent,
  BookOpen,
  Scale,
  TrendingDown,
  TrendingUp,
  BarChart3,
  Activity,
  Lock,
  History,
  Sliders,
  Hospital
} from 'lucide-react';

export type ViewKey =
  | 'dashboard'
  | 'invoices'
  | 'invoice-timeline'
  | 'payments'
  | 'refunds'
  | 'reconciliation'
  | 'insurance-payers'
  | 'claims-workbench'
  | 'gst-tax'
  | 'chart-of-accounts'
  | 'journal-entries'
  | 'accounts-receivable'
  | 'accounts-payable'
  | 'financial-reports'
  | 'integrity-monitor'
  | 'period-closing'
  | 'audit-log'
  | 'settings-policies';

interface SidebarProps {
  currentView: ViewKey;
  onNavigate: (view: ViewKey) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentView, onNavigate }) => {
  return (
    <aside className="sidebar">
      {/* Brand Header */}
      <div style={{ padding: '20px 20px 16px', borderBottom: '1px solid var(--border-card)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div
            style={{
              background: 'linear-gradient(135deg, #0284c7 0%, #0369a1 100%)',
              width: '34px',
              height: '34px',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <Hospital size={20} color="#ffffff" />
          </div>
          <div>
            <div style={{ fontSize: '1rem', fontWeight: 700, color: '#ffffff', letterSpacing: '-0.01em' }}>
              HMS Finance
            </div>
            <div style={{ fontSize: '0.6875rem', color: '#38bdf8', fontWeight: 600 }}>
              Member 6 — SaaS Suite
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Sections */}
      <div style={{ flex: 1, paddingBottom: '24px' }}>
        {/* Section 1: Executive & Intelligence */}
        <div className="nav-section-title">Overview & Intelligence</div>
        <div
          className={`nav-item ${currentView === 'dashboard' ? 'active' : ''}`}
          onClick={() => onNavigate('dashboard')}
        >
          <LayoutDashboard />
          <span>1. Finance Dashboard</span>
        </div>
        <div
          className={`nav-item ${currentView === 'integrity-monitor' ? 'active' : ''}`}
          onClick={() => onNavigate('integrity-monitor')}
        >
          <Activity />
          <span>15. Integrity Monitor</span>
        </div>
        <div
          className={`nav-item ${currentView === 'financial-reports' ? 'active' : ''}`}
          onClick={() => onNavigate('financial-reports')}
        >
          <BarChart3 />
          <span>14. Reports & Analytics</span>
        </div>

        {/* Section 2: Hospital Billing & Revenue */}
        <div className="nav-section-title">Billing & Patient Accounts</div>
        <div
          className={`nav-item ${currentView === 'invoices' ? 'active' : ''}`}
          onClick={() => onNavigate('invoices')}
        >
          <FileText />
          <span>2. Invoice Management</span>
        </div>
        <div
          className={`nav-item ${currentView === 'invoice-timeline' ? 'active' : ''}`}
          onClick={() => onNavigate('invoice-timeline')}
        >
          <Clock />
          <span>3. Details & Financial Timeline</span>
        </div>
        <div
          className={`nav-item ${currentView === 'accounts-receivable' ? 'active' : ''}`}
          onClick={() => onNavigate('accounts-receivable')}
        >
          <TrendingDown />
          <span>12. Accounts Receivable</span>
        </div>

        {/* Section 3: Payments & Cash Desk */}
        <div className="nav-section-title">Payments & Treasury</div>
        <div
          className={`nav-item ${currentView === 'payments' ? 'active' : ''}`}
          onClick={() => onNavigate('payments')}
        >
          <CreditCard />
          <span>4. Payments & Receipts</span>
        </div>
        <div
          className={`nav-item ${currentView === 'refunds' ? 'active' : ''}`}
          onClick={() => onNavigate('refunds')}
        >
          <RotateCcw />
          <span>5. Refund Management</span>
        </div>
        <div
          className={`nav-item ${currentView === 'reconciliation' ? 'active' : ''}`}
          onClick={() => onNavigate('reconciliation')}
        >
          <GitCompare />
          <span>6. Payment Reconciliation</span>
        </div>

        {/* Section 4: Insurance & Claims */}
        <div className="nav-section-title">Insurance & TPA Claims</div>
        <div
          className={`nav-item ${currentView === 'insurance-payers' ? 'active' : ''}`}
          onClick={() => onNavigate('insurance-payers')}
        >
          <ShieldAlert />
          <span>7. Payers & Policies</span>
        </div>
        <div
          className={`nav-item ${currentView === 'claims-workbench' ? 'active' : ''}`}
          onClick={() => onNavigate('claims-workbench')}
        >
          <FileCheck2 />
          <span>8. Claims Workbench</span>
        </div>

        {/* Section 5: General Ledger & Accounting */}
        <div className="nav-section-title">Accounting & General Ledger</div>
        <div
          className={`nav-item ${currentView === 'chart-of-accounts' ? 'active' : ''}`}
          onClick={() => onNavigate('chart-of-accounts')}
        >
          <BookOpen />
          <span>10. Chart of Accounts</span>
        </div>
        <div
          className={`nav-item ${currentView === 'journal-entries' ? 'active' : ''}`}
          onClick={() => onNavigate('journal-entries')}
        >
          <Scale />
          <span>11. Journal Entries & GL</span>
        </div>
        <div
          className={`nav-item ${currentView === 'accounts-payable' ? 'active' : ''}`}
          onClick={() => onNavigate('accounts-payable')}
        >
          <TrendingUp />
          <span>13. Accounts Payable</span>
        </div>
        <div
          className={`nav-item ${currentView === 'period-closing' ? 'active' : ''}`}
          onClick={() => onNavigate('period-closing')}
        >
          <Lock />
          <span>16. Period Closing</span>
        </div>

        {/* Section 6: Governance & Configuration */}
        <div className="nav-section-title">Compliance & Policies</div>
        <div
          className={`nav-item ${currentView === 'gst-tax' ? 'active' : ''}`}
          onClick={() => onNavigate('gst-tax')}
        >
          <Percent />
          <span>9. GST & Tax Config</span>
        </div>
        <div
          className={`nav-item ${currentView === 'audit-log' ? 'active' : ''}`}
          onClick={() => onNavigate('audit-log')}
        >
          <History />
          <span>17. Finance Audit Log</span>
        </div>
        <div
          className={`nav-item ${currentView === 'settings-policies' ? 'active' : ''}`}
          onClick={() => onNavigate('settings-policies')}
        >
          <Sliders />
          <span>18. Settings & Policies</span>
        </div>
      </div>
    </aside>
  );
};
