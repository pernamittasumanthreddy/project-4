'use client';
import React, { useState, useEffect } from 'react';
import { HospitalRole, UserProfile } from '@/lib/types/roles';
import { DEMO_USERS, INITIAL_NOTIFICATIONS, SEED_PATIENTS } from '@/lib/data/mockDatabase';
import { HospitalDocument } from '@/lib/types/rag';
import { Patient } from '@/lib/types/hms';
import { Sidebar } from './Sidebar';
import { RoleBadge } from './RoleBadge';
import { RAGAssistantModal } from '../rag/RAGAssistantModal';
import { RAGEvaluationModal } from '../rag/RAGEvaluationModal';
import { DocumentViewerModal } from '../rag/DocumentViewerModal';
import { PatientWorkspaceModal } from '../shared/PatientWorkspaceModal';
import { SearchCommandModal } from '../shared/SearchCommandModal';
import { NotificationCenter } from '../shared/NotificationCenter';
import { HospitalHelpModal } from '../shared/HospitalHelpModal';
import { HospitalLoginPortal } from '../auth/HospitalLoginPortal';
import { HospitalHomePage } from '../home/HospitalHomePage';
import { WorkstationLaunchModal } from '../auth/WorkstationLaunchModal';
import { ThemeToggle } from '../theme/ThemeToggle';

// Role Dashboards
import { SuperAdminDashboard } from '../dashboards/SuperAdminDashboard';
import { HospitalAdminDashboard } from '../dashboards/HospitalAdminDashboard';
import { DoctorDashboard } from '../dashboards/DoctorDashboard';
import { NurseDashboard } from '../dashboards/NurseDashboard';
import { ReceptionistDashboard } from '../dashboards/ReceptionistDashboard';
import { PatientDashboard } from '../dashboards/PatientDashboard';
import { PharmacistDashboard } from '../dashboards/PharmacistDashboard';
import { LaboratoryDashboard } from '../dashboards/LaboratoryDashboard';
import { RadiologyDashboard } from '../dashboards/RadiologyDashboard';
import { BillingDashboard } from '../dashboards/BillingDashboard';
import { InsuranceDashboard } from '../dashboards/InsuranceDashboard';
import { HRDashboard } from '../dashboards/HRDashboard';
import { DepartmentManagerDashboard } from '../dashboards/DepartmentManagerDashboard';
import { ManagementExecutiveDashboard } from '../dashboards/ManagementExecutiveDashboard';
import { EmergencyDashboard } from '../dashboards/EmergencyDashboard';

import { 
  Search, Bell, ChevronDown, Check, LogOut, 
  Bot, Award, AlertCircle, HelpCircle, Flame, 
  Activity, Stethoscope, Sparkles 
} from 'lucide-react';

const ALL_ROLES: { role: HospitalRole; label: string; desc: string }[] = [
  { role: 'DOCTOR', label: 'Attending Physician', desc: 'Inpatient rounds, EMR charts, clinical orders' },
  { role: 'NURSE', label: 'Nurse Station', desc: 'Bedside telemetry, 5-rights medication administration' },
  { role: 'EMERGENCY_STAFF', label: 'Emergency & Trauma Bay', desc: 'ESI level 1-5 triage, resuscitation protocols' },
  { role: 'PATIENT', label: 'Patient Portal', desc: 'Health home, active prescriptions, appointments' },
  { role: 'HOSPITAL_ADMIN', label: 'Hospital Administrator', desc: 'Bed census, departmental workload, audit logs' },
  { role: 'SUPER_ADMIN', label: 'Cluster Super Admin', desc: 'Multi-hospital cluster governance, RBAC matrix' },
  { role: 'PHARMACIST', label: 'Clinical Pharmacy', desc: 'CPOE verification, formulary inventory, cold-chain' },
  { role: 'LABORATORY_STAFF', label: 'Diagnostic Laboratory', desc: 'LIS test accessioning, panic values, analyzer QC' },
  { role: 'RADIOLOGY_STAFF', label: 'Diagnostic Imaging', desc: 'CT, MRI, X-Ray modality PACS worklist' },
  { role: 'BILLING_STAFF', label: 'Medical Billing', desc: 'Inpatient claims ledger, standard chargemaster' },
  { role: 'INSURANCE_STAFF', label: 'Insurance & TPA', desc: 'Prior-authorizations, medical necessity review' },
  { role: 'HR_STAFF', label: 'Healthcare Human Resources', desc: 'Staff credentialing, state board licenses, leave' },
  { role: 'DEPARTMENT_MANAGER', label: 'Department Manager', desc: 'Nurse-to-patient staffing ratios, equipment QC' },
  { role: 'MANAGEMENT_EXECUTIVE', label: 'Executive Board / C-Suite', desc: 'EBITDA margin, Leapfrog Grade A quality scorecard' },
  { role: 'RECEPTIONIST', label: 'Front Desk / Intake', desc: 'Outpatient check-in, walk-in registration, visitor passes' },
];

export const HospitalShell: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [portalView, setPortalView] = useState<'home' | 'login'>('login');
  const [currentRole, setCurrentRole] = useState<HospitalRole>('DOCTOR');
  const [currentUser, setCurrentUser] = useState<UserProfile>(DEMO_USERS['DOCTOR']);
  const [activeNav, setActiveNav] = useState('dashboard');
  
  // Modals state
  const [isRAGOpen, setIsRAGOpen] = useState(false);
  const [isEvalOpen, setIsEvalOpen] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState<HospitalDocument | null>(null);
  const [selectedPatientForEMR, setSelectedPatientForEMR] = useState<Patient | null>(null);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isHelpOpen, setIsHelpOpen] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [showRoleSwitcher, setShowRoleSwitcher] = useState(false);
  const [pendingSwitchRole, setPendingSwitchRole] = useState<HospitalRole | null>(null);

  // Global Keyboard Shortcuts (Ctrl + K / Cmd + K)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsSearchOpen(true);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleLoginFromPortal = (role: HospitalRole) => {
    setCurrentRole(role);
    setCurrentUser(DEMO_USERS[role] || DEMO_USERS['DOCTOR']);
    setIsLoggedIn(true);
    setActiveNav('dashboard');
  };

  const handleRoleChange = (role: HospitalRole) => {
    setCurrentRole(role);
    setCurrentUser(DEMO_USERS[role] || DEMO_USERS['DOCTOR']);
    setShowRoleSwitcher(false);
    setActiveNav('dashboard');
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setPortalView('login');
  };

  const handleSelectPatientFromAnywhere = (patient: Patient) => {
    setSelectedPatientForEMR(patient);
  };

  // If not logged in, show the 15-Role Workstation Login Gateway
  if (!isLoggedIn) {
    return (
      <HospitalLoginPortal 
        onLogin={handleLoginFromPortal} 
      />
    );
  }

  const roleNotifications = INITIAL_NOTIFICATIONS.filter(
    n => !n.targetRole || n.targetRole === currentRole || n.userId === currentUser.id
  );

  // Render the appropriate role dashboard with activeNav wiring
  const renderDashboard = () => {
    switch (currentRole) {
      case 'SUPER_ADMIN':
        return <SuperAdminDashboard activeNav={activeNav} setActiveNav={setActiveNav} />;
      case 'HOSPITAL_ADMIN':
        return <HospitalAdminDashboard onOpenRAG={() => setIsRAGOpen(true)} onOpenDoc={setSelectedDoc} activeNav={activeNav} setActiveNav={setActiveNav} />;
      case 'DOCTOR':
        return (
          <DoctorDashboard 
            onOpenRAG={() => setIsRAGOpen(true)} 
            onOpenDoc={setSelectedDoc} 
            activeNav={activeNav} 
            setActiveNav={setActiveNav}
            onSelectPatient={handleSelectPatientFromAnywhere}
          />
        );
      case 'NURSE':
        return (
          <NurseDashboard 
            onOpenRAG={() => setIsRAGOpen(true)} 
            onOpenDoc={setSelectedDoc} 
            activeNav={activeNav} 
            setActiveNav={setActiveNav}
            onSelectPatient={handleSelectPatientFromAnywhere}
          />
        );
      case 'PATIENT':
        return <PatientDashboard onOpenRAG={() => setIsRAGOpen(true)} onOpenDoc={setSelectedDoc} activeNav={activeNav} setActiveNav={setActiveNav} />;
      case 'PHARMACIST':
        return <PharmacistDashboard onOpenRAG={() => setIsRAGOpen(true)} onOpenDoc={setSelectedDoc} activeNav={activeNav} setActiveNav={setActiveNav} />;
      case 'LABORATORY_STAFF':
        return <LaboratoryDashboard onOpenRAG={() => setIsRAGOpen(true)} onOpenDoc={setSelectedDoc} activeNav={activeNav} setActiveNav={setActiveNav} />;
      case 'RADIOLOGY_STAFF':
        return <RadiologyDashboard onOpenRAG={() => setIsRAGOpen(true)} onOpenDoc={setSelectedDoc} activeNav={activeNav} setActiveNav={setActiveNav} />;
      case 'BILLING_STAFF':
        return <BillingDashboard onOpenRAG={() => setIsRAGOpen(true)} onOpenDoc={setSelectedDoc} activeNav={activeNav} setActiveNav={setActiveNav} />;
      case 'INSURANCE_STAFF':
        return <InsuranceDashboard onOpenRAG={() => setIsRAGOpen(true)} onOpenDoc={setSelectedDoc} activeNav={activeNav} setActiveNav={setActiveNav} />;
      case 'HR_STAFF':
        return <HRDashboard onOpenRAG={() => setIsRAGOpen(true)} onOpenDoc={setSelectedDoc} activeNav={activeNav} setActiveNav={setActiveNav} />;
      case 'DEPARTMENT_MANAGER':
        return <DepartmentManagerDashboard onOpenRAG={() => setIsRAGOpen(true)} onOpenDoc={setSelectedDoc} activeNav={activeNav} setActiveNav={setActiveNav} />;
      case 'MANAGEMENT_EXECUTIVE':
        return <ManagementExecutiveDashboard onOpenRAG={() => setIsRAGOpen(true)} onOpenDoc={setSelectedDoc} activeNav={activeNav} setActiveNav={setActiveNav} />;
      case 'EMERGENCY_STAFF':
        return (
          <EmergencyDashboard 
            onOpenRAG={() => setIsRAGOpen(true)} 
            onOpenDoc={setSelectedDoc} 
            activeNav={activeNav} 
            setActiveNav={setActiveNav} 
            onSelectPatient={handleSelectPatientFromAnywhere}
          />
        );
      case 'RECEPTIONIST':
      default:
        return (
          <ReceptionistDashboard 
            onOpenRAG={() => setIsRAGOpen(true)} 
            onOpenDoc={setSelectedDoc} 
            activeNav={activeNav} 
            setActiveNav={setActiveNav} 
            onSelectPatient={handleSelectPatientFromAnywhere}
          />
        );
    }
  };

  const currentDateString = new Date().toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });

  const getRoleCategoryLabel = (role: HospitalRole): string => {
    switch (role) {
      case 'DOCTOR':
      case 'NURSE':
      case 'EMERGENCY_STAFF':
        return 'Clinical Care';
      case 'PHARMACIST':
      case 'LABORATORY_STAFF':
      case 'RADIOLOGY_STAFF':
        return 'Diagnostics & Rx';
      case 'PATIENT':
      case 'RECEPTIONIST':
        return 'Patient Access';
      case 'BILLING_STAFF':
      case 'INSURANCE_STAFF':
      case 'HR_STAFF':
        return 'Operations & Finance';
      default:
        return 'Governance & Admin';
    }
  };

  return (
    <div className="flex h-screen bg-[#F4F7FA] dark:bg-[#0B1120] overflow-hidden font-sans text-[#1E293B] dark:text-[#F8FAFC]">
      {/* Sidebar Navigation */}
      <Sidebar
        currentRole={currentRole}
        onOpenRAG={() => setIsRAGOpen(true)}
        onOpenEval={() => setIsEvalOpen(true)}
        activeNav={activeNav}
        setActiveNav={setActiveNav}
        currentUser={currentUser}
      />

      {/* Main Container */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        
        {/* Top Header Command Bar */}
        <header className="h-16 bg-white dark:bg-[#111827] border-b border-[#DCE4EA] dark:border-[#293548] px-5 flex items-center justify-between gap-3 z-20 shrink-0">
          
          {/* Left: Breadcrumbs & Campus Context */}
          <div className="flex items-center gap-3 flex-1 max-w-xl">
            <div className="flex flex-col shrink-0 min-w-0">
              {/* Breadcrumb Navigation */}
              <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-xs text-slate-500">
                <span className="font-semibold text-slate-700 dark:text-slate-300">CityCare</span>
                <span>/</span>
                <span>{getRoleCategoryLabel(currentRole)}</span>
                <span>/</span>
                <span className="text-[#0F8B8D] font-bold truncate">{currentUser.name.split(' ')[0]} Workstation</span>
              </nav>

              <div className="flex items-center gap-2 mt-0.5 text-[11px] text-slate-400">
                <span className="font-mono text-[#0F8B8D] font-semibold">{currentUser.department}</span>
                <span>•</span>
                <span>{currentDateString}</span>
              </div>
            </div>

            {/* Global Search Button / Trigger */}
            <button
              onClick={() => setIsSearchOpen(true)}
              className="hidden md:flex flex-1 items-center justify-between pl-3 pr-2.5 py-1.5 bg-[#F4F7FA] hover:bg-slate-100 dark:bg-[#172033] dark:hover:bg-[#1D293D] border border-[#DCE4EA] dark:border-[#293548] rounded-lg text-xs text-slate-500 transition-all text-left group ml-2"
            >
              <div className="flex items-center gap-2">
                <Search className="w-3.5 h-3.5 text-slate-400 group-hover:text-[#0F8B8D] transition-colors" />
                <span className="text-slate-400 group-hover:text-slate-600 dark:group-hover:text-slate-300 truncate">
                  Search patients, orders, EMR, SOPs...
                </span>
              </div>
              <kbd className="hidden lg:inline-flex items-center gap-0.5 px-1.5 py-0.5 text-[10px] font-mono bg-white dark:bg-[#111827] border border-[#DCE4EA] dark:border-[#293548] rounded text-slate-400 shadow-2xs">
                Ctrl + K
              </kbd>
            </button>
          </div>

          {/* Right: Live Emergency Indicator, Notifications, Help, User Profile & Actions */}
          <div className="flex items-center gap-2.5 shrink-0">
            
            {/* Live Emergency Alert Indicator */}
            <button
              onClick={() => {
                if (currentRole !== 'EMERGENCY_STAFF') {
                  setPendingSwitchRole('EMERGENCY_STAFF');
                } else {
                  setActiveNav('dashboard');
                }
              }}
              className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 text-xs font-semibold transition-colors"
              title="Click to view Emergency Department status"
            >
              <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping" />
              <Flame className="w-3.5 h-3.5 text-rose-600" />
              <span>Emergency: 3 Active</span>
            </button>

            {/* Hospital Directory & Help */}
            <button
              onClick={() => setIsHelpOpen(true)}
              className="p-2 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-lg border border-slate-200/80 transition-colors"
              title="Hospital Telephone & Emergency Directory"
            >
              <HelpCircle className="w-4 h-4" />
            </button>

            {/* Notifications Center */}
            <div className="relative">
              <button
                onClick={() => setShowNotifications(!showNotifications)}
                className="p-2 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-lg border border-slate-200/80 transition-colors relative"
                title="Hospital Alerts"
              >
                <Bell className="w-4 h-4" />
                {roleNotifications.length > 0 && (
                  <span className="w-2 h-2 rounded-full bg-rose-500 absolute top-1.5 right-1.5 ring-2 ring-white" />
                )}
              </button>

              <NotificationCenter
                notifications={roleNotifications}
                isOpen={showNotifications}
                onClose={() => setShowNotifications(false)}
              />
            </div>

            {/* Quick Role Perspective Switcher */}
            <div className="relative">
              <button
                onClick={() => setShowRoleSwitcher(!showRoleSwitcher)}
                className="flex items-center gap-2 px-2.5 py-1.5 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg text-xs font-semibold text-slate-800 transition-all shadow-2xs"
                title="Switch Role Perspective"
              >
                <span className="text-slate-400 font-normal hidden sm:inline">Role:</span>
                <RoleBadge role={currentRole} size="sm" />
                <ChevronDown className="w-3 h-3 text-slate-400" />
              </button>

              {/* Role Switcher Dropdown */}
              {showRoleSwitcher && (
                <div className="absolute right-0 mt-2 w-80 bg-white border border-slate-200 rounded-xl shadow-2xl p-2 z-50 text-xs animate-in fade-in duration-100 max-h-96 overflow-y-auto">
                  <div className="p-2 border-b border-slate-100 font-bold text-slate-500 uppercase tracking-wider text-[10px] flex items-center justify-between">
                    <span>Switch Role Perspective (15 Roles)</span>
                    <span className="font-mono text-blue-600">RBAC Switch</span>
                  </div>
                  <div className="space-y-1 mt-1">
                    {ALL_ROLES.map((r) => {
                      const isSelected = r.role === currentRole;
                      return (
                        <button
                          key={r.role}
                          onClick={() => {
                            setShowRoleSwitcher(false);
                            if (r.role !== currentRole) {
                              setPendingSwitchRole(r.role);
                            }
                          }}
                          className={`w-full text-left p-2 rounded-lg transition-all flex items-start justify-between ${
                            isSelected
                              ? 'bg-blue-50 text-blue-900 font-bold'
                              : 'hover:bg-slate-50 text-slate-700'
                          }`}
                        >
                          <div>
                            <div className="flex items-center gap-1.5">
                              <span className="font-semibold text-slate-900">{r.label}</span>
                              {isSelected && <Check className="w-3.5 h-3.5 text-blue-600" />}
                            </div>
                            <p className="text-[10px] text-slate-500 mt-0.5 line-clamp-1">{r.desc}</p>
                          </div>
                          <RoleBadge role={r.role} size="sm" />
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>

            {/* Theme Toggle */}
            <ThemeToggle variant="dropdown" />

            {/* User Profile Pill */}
            <div className="flex items-center gap-2 pl-2 border-l border-slate-200 dark:border-slate-800">
              <div className="relative">
                <div className="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-300 flex items-center justify-center font-bold text-xs shrink-0">
                  {currentUser.name.split(' ').map(n => n[0]).join('').slice(0, 2)}
                </div>
                <span className="w-2 h-2 rounded-full bg-emerald-500 absolute -bottom-0.5 -right-0.5 ring-2 ring-white dark:ring-[#111827]" title="Online" />
              </div>
              <div className="hidden xl:block text-left">
                <span className="text-xs font-bold text-slate-900 dark:text-slate-100 block leading-tight">{currentUser.name}</span>
                <span className="text-[10px] text-slate-500 dark:text-slate-400 block leading-tight">{currentUser.department}</span>
              </div>
            </div>

            {/* Logout Button */}
            <button
              onClick={handleLogout}
              className="flex items-center gap-1.5 px-2.5 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 rounded-lg text-xs font-semibold transition-all shadow-2xs"
              title="Return to Main Login Gateway"
            >
              <LogOut className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Log Out</span>
            </button>
          </div>
        </header>

        {/* Dynamic Role Dashboard Body */}
        <main className="flex-1 overflow-y-auto p-6">
          {renderDashboard()}
        </main>
      </div>

      {/* Floating Action Button (FAB) for Role RAG Assistant */}
      <button
        onClick={() => setIsRAGOpen(true)}
        className="fixed bottom-6 right-6 z-30 flex items-center gap-2 px-3.5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 font-bold text-xs active:scale-95 border border-blue-500"
      >
        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping absolute -top-0.5 -right-0.5" />
        <Bot className="w-4 h-4" />
        <span>Ask Clinical Assistant</span>
      </button>

      {/* Global Search Command Modal (Ctrl + K) */}
      <SearchCommandModal
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        onSelectPatient={handleSelectPatientFromAnywhere}
        onSelectDocument={(doc) => setSelectedDoc(doc)}
      />

      {/* Hospital Help & Directory Modal */}
      <HospitalHelpModal
        isOpen={isHelpOpen}
        onClose={() => setIsHelpOpen(false)}
      />

      {/* Full Clinical EMR Patient Workspace Modal */}
      <PatientWorkspaceModal
        patient={selectedPatientForEMR}
        isOpen={Boolean(selectedPatientForEMR)}
        onClose={() => setSelectedPatientForEMR(null)}
        onOpenDoc={setSelectedDoc}
        onOpenRAG={() => setIsRAGOpen(true)}
      />

      {/* Dedicated Personal RAG Assistant Modal */}
      <RAGAssistantModal
        isOpen={isRAGOpen}
        onClose={() => setIsRAGOpen(false)}
        currentUser={currentUser}
      />

      {/* RAG Evaluation & Benchmarking Modal */}
      <RAGEvaluationModal
        isOpen={isEvalOpen}
        onClose={() => setIsEvalOpen(false)}
      />

      {/* Hospital Document Viewer Modal */}
      <DocumentViewerModal
        document={selectedDoc}
        onClose={() => setSelectedDoc(null)}
      />

      {/* Workstation Access Credentials Modal for In-Dashboard Role Switching */}
      <WorkstationLaunchModal
        role={pendingSwitchRole}
        isOpen={!!pendingSwitchRole}
        onComplete={(role) => {
          setPendingSwitchRole(null);
          handleRoleChange(role);
        }}
        onCancel={() => setPendingSwitchRole(null)}
      />
    </div>
  );
};
