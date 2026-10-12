'use client';
import React, { useState } from 'react';
import { HospitalRole } from '@/lib/types/roles';
import { 
  LayoutDashboard, Users, Calendar, Bed, Pill, 
  FlaskConical, Scan, CreditCard, ShieldCheck, 
  Building2, Activity, Heart, Award, FileText, 
  Flame, BookOpen, Clock, Settings, Bell, Lock, 
  ChevronLeft, ChevronRight, Stethoscope, Sparkles 
} from 'lucide-react';

interface SidebarProps {
  currentRole: HospitalRole;
  onOpenRAG: () => void;
  onOpenEval: () => void;
  activeNav: string;
  setActiveNav: (nav: string) => void;
  currentUser?: {
    name: string;
    role: HospitalRole;
    department: string;
    employeeId?: string;
  };
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentRole,
  onOpenRAG,
  onOpenEval,
  activeNav,
  setActiveNav,
  currentUser,
}) => {
  const [collapsed, setCollapsed] = useState(false);

  // Navigation items specific to role
  const getNavItems = () => {
    switch (currentRole) {
      case 'SUPER_ADMIN':
        return [
          { id: 'dashboard', label: 'Cluster Governance', icon: LayoutDashboard },
          { id: 'tenants', label: 'Hospital Tenants', icon: Building2 },
          { id: 'rbac', label: 'RBAC Security Matrix', icon: Lock },
          { id: 'audit', label: 'Global Audit Logs', icon: Clock },
          { id: 'settings', label: 'System Settings', icon: Settings },
        ];
      case 'HOSPITAL_ADMIN':
        return [
          { id: 'dashboard', label: 'Operations Overview', icon: LayoutDashboard },
          { id: 'census', label: 'Bed & Ward Census', icon: Bed },
          { id: 'departments', label: 'Departments', icon: Building2 },
          { id: 'documents', label: 'Hospital Documents', icon: FileText },
          { id: 'audit', label: 'Audit Trail', icon: Clock },
        ];
      case 'DOCTOR':
        return [
          { id: 'dashboard', label: 'Clinical Dashboard', icon: LayoutDashboard },
          { id: 'workspace', label: 'Clinical Workstation', icon: Stethoscope },
          { id: 'emr', label: 'Longitudinal EMR', icon: FileText },
          { id: 'patients', label: 'Assigned Patients', icon: Users },
          { id: 'appointments', label: 'Consultations', icon: Calendar },
          { id: 'labs', label: 'Lab & Diagnostic Results', icon: FlaskConical },
          { id: 'guidelines', label: 'Clinical Guidelines', icon: BookOpen },
        ];
      case 'NURSE':
        return [
          { id: 'dashboard', label: 'Nurse Station', icon: LayoutDashboard },
          { id: 'console', label: 'Telemetry & MEWS', icon: Activity },
          { id: 'vitals', label: 'Bedside Vitals', icon: Heart },
          { id: 'meds', label: 'Med Administration', icon: Pill },
          { id: 'tasks', label: 'Shift Handover & Care', icon: FileText },
        ];
      case 'PATIENT':
        return [
          { id: 'dashboard', label: 'My Health Home', icon: LayoutDashboard },
          { id: 'records', label: 'Medical Records', icon: FileText },
          { id: 'prescriptions', label: 'My Medications', icon: Pill },
          { id: 'bills', label: 'Bills & Insurance', icon: CreditCard },
        ];
      case 'PHARMACIST':
        return [
          { id: 'dashboard', label: 'Pharmacy Workstation', icon: LayoutDashboard },
          { id: 'orders', label: 'CPOE Order Queue', icon: Pill },
          { id: 'formulary', label: 'Formulary Inventory', icon: BookOpen },
          { id: 'coldchain', label: 'Cold-Chain Telemetry', icon: Activity },
        ];
      case 'LABORATORY_STAFF':
        return [
          { id: 'dashboard', label: 'Laboratory Console', icon: LayoutDashboard },
          { id: 'worklist', label: 'LIS Test Worklist', icon: FlaskConical },
          { id: 'panic', label: 'Panic Values Log', icon: Flame },
          { id: 'qc', label: 'Analyzer Quality Control', icon: ShieldCheck },
        ];
      case 'RADIOLOGY_STAFF':
        return [
          { id: 'dashboard', label: 'Imaging Console', icon: LayoutDashboard },
          { id: 'scans', label: 'Modality Queue', icon: Scan },
          { id: 'safety', label: 'Contrast & Radiation', icon: ShieldCheck },
        ];
      case 'BILLING_STAFF':
        return [
          { id: 'dashboard', label: 'Billing Overview', icon: LayoutDashboard },
          { id: 'invoices', label: 'Inpatient Invoices', icon: CreditCard },
          { id: 'tariffs', label: 'Hospital Tariffs', icon: BookOpen },
        ];
      case 'INSURANCE_STAFF':
        return [
          { id: 'dashboard', label: 'TPA Claims Center', icon: LayoutDashboard },
          { id: 'preauth', label: 'Pre-Authorizations', icon: ShieldCheck },
          { id: 'payers', label: 'Payer Contracts', icon: Building2 },
        ];
      case 'HR_STAFF':
        return [
          { id: 'dashboard', label: 'HR Administration', icon: LayoutDashboard },
          { id: 'roster', label: 'Staff Roster & Creds', icon: Users },
          { id: 'leave', label: 'Leave & Attendance', icon: Calendar },
        ];
      case 'DEPARTMENT_MANAGER':
        return [
          { id: 'dashboard', label: 'Dept Operations', icon: LayoutDashboard },
          { id: 'staffing', label: 'Staff Ratios', icon: Users },
          { id: 'equipment', label: 'Equipment QC', icon: ShieldCheck },
        ];
      case 'MANAGEMENT_EXECUTIVE':
        return [
          { id: 'dashboard', label: 'Executive Scorecard', icon: LayoutDashboard },
          { id: 'revenue', label: 'Revenue Analytics', icon: CreditCard },
          { id: 'quality', label: 'Quality & JCAHO', icon: Award },
        ];
      case 'EMERGENCY_STAFF':
        return [
          { id: 'dashboard', label: 'Trauma Bay Triage', icon: LayoutDashboard },
          { id: 'queue', label: 'ESI Patient Queue', icon: Flame },
          { id: 'codeblue', label: 'Code Blue Resus', icon: Heart },
        ];
      case 'RECEPTIONIST':
      default:
        return [
          { id: 'dashboard', label: 'Patient Access', icon: LayoutDashboard },
          { id: 'appointments', label: 'Appointments', icon: Calendar },
          { id: 'visitors', label: 'Visitor Badges', icon: ShieldCheck },
        ];
    }
  };

  const navItems = getNavItems();

  return (
    <aside
      className={`bg-[#123B52] border-r border-[#0B2C3D] flex flex-col justify-between shrink-0 select-none text-[#D7E6EE] transition-all duration-200 ${
        collapsed ? 'w-18' : 'w-64'
      }`}
    >
      {/* Brand Header */}
      <div>
        <div className="p-4 border-b border-[#0B2C3D] flex items-center justify-between gap-3">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-8 h-8 rounded-lg bg-[#0F8B8D] flex items-center justify-center text-white shadow-xs font-bold text-base shrink-0">
              +
            </div>
            {!collapsed && (
              <div className="truncate">
                <h1 className="text-xs font-bold text-white tracking-tight leading-tight truncate">
                  CityCare Hospital
                </h1>
                <span className="text-[10px] text-[#0F8B8D] font-semibold block leading-tight truncate">
                  Central Campus
                </span>
              </div>
            )}
          </div>

          <button
            onClick={() => setCollapsed(!collapsed)}
            className="p-1 text-[#D7E6EE]/70 hover:text-white hover:bg-[#0B2C3D] rounded-md transition-colors"
            title={collapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
          >
            {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>

        {/* Navigation list */}
        <div className="p-2.5 space-y-1">
          {!collapsed && (
            <div className="px-2.5 py-1 text-[10px] uppercase font-bold text-[#D7E6EE]/60 tracking-wider">
              Clinical Workspace
            </div>
          )}
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeNav === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveNav(item.id)}
                title={collapsed ? item.label : undefined}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-[#0F8B8D] text-white shadow-xs'
                    : 'text-[#D7E6EE] hover:text-white hover:bg-[#0B2C3D]'
                } ${collapsed ? 'justify-center px-0' : ''}`}
              >
                <Icon className="w-4 h-4 shrink-0" />
                {!collapsed && <span className="truncate">{item.label}</span>}
              </button>
            );
          })}
        </div>

        {/* Dedicated Hospital Intelligence Section */}
        <div className="p-2.5 pt-1 space-y-1 border-t border-[#0B2C3D] mt-2">
          {!collapsed && (
            <div className="px-2.5 py-1 text-[10px] uppercase font-bold text-[#D7E6EE]/60 tracking-wider">
              Clinical Intelligence
            </div>
          )}

          <button
            onClick={onOpenRAG}
            title={collapsed ? 'Role RAG Assistant' : undefined}
            className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-bold bg-[#0B2C3D] text-[#0F8B8D] hover:bg-[#082230] border border-[#0F8B8D]/40 transition-all ${
              collapsed ? 'justify-center px-0' : ''
            }`}
          >
            <Sparkles className="w-4 h-4 shrink-0 text-[#0F8B8D]" />
            {!collapsed && <span className="truncate">Clinical Knowledge RAG</span>}
          </button>

          <button
            onClick={onOpenEval}
            title={collapsed ? 'RAG Quality Benchmark' : undefined}
            className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-medium text-[#D7E6EE] hover:text-white hover:bg-[#0B2C3D] transition-all ${
              collapsed ? 'justify-center px-0' : ''
            }`}
          >
            <Award className="w-4 h-4 shrink-0 text-emerald-400" />
            {!collapsed && <span className="truncate">RAG Quality Benchmark</span>}
          </button>
        </div>
      </div>

      {/* Footer: Current User Profile + Security Badge */}
      <div className="border-t border-[#0B2C3D] bg-[#0B2C3D]/60 text-[11px] text-[#D7E6EE]">
        {currentUser && (
          <div className={`p-3 border-b border-[#0B2C3D] flex items-center gap-2.5 ${collapsed ? 'justify-center' : ''}`}>
            <div className="relative shrink-0">
              <div className="w-8 h-8 rounded-lg bg-[#0F8B8D] text-white flex items-center justify-center font-bold text-xs">
                {currentUser.name.split(' ').map(n => n[0]).join('').slice(0, 2)}
              </div>
              <span className="w-2 h-2 rounded-full bg-[#16A34A] absolute -bottom-0.5 -right-0.5 ring-2 ring-[#0B2C3D]" title="Online" />
            </div>
            {!collapsed && (
              <div className="min-w-0 flex-1 truncate">
                <div className="font-bold text-white text-xs truncate leading-tight">{currentUser.name}</div>
                <div className="text-[10px] text-[#D7E6EE]/75 truncate leading-tight">{currentUser.department}</div>
              </div>
            )}
          </div>
        )}

        <div className="p-3">
          <div className={`flex items-center gap-1.5 text-emerald-400 font-semibold mb-0.5 ${collapsed ? 'justify-center' : ''}`}>
            <ShieldCheck className="w-3.5 h-3.5 shrink-0" />
            {!collapsed && <span>HIPAA Certified</span>}
          </div>
          {!collapsed && (
            <p className="text-[10px] leading-tight text-[#D7E6EE]/60">
              Multi-Tenant Isolation • AES-256
            </p>
          )}
        </div>
      </div>
    </aside>
  );
};
