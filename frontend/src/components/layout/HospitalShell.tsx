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
  const [isLoggedIn, setIsLoggedIn] = useState(true);
  const [portalView, setPortalView] = useState<'home' | 'login'>('home');
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
    setPortalView('home');
  };

  const handleSelectPatientFromAnywhere = (patient: Patient) => {
    setSelectedPatientForEMR(patient);
  };

  // If not logged in, show the Welcome Home Page or the 15-Role Workstation Gateway
  if (!isLoggedIn) {
    if (portalView === 'home') {
      return (
        <HospitalHomePage 
          onOpenLogins={() => setPortalView('login')} 
          onQuickLogin={(role) => handleLoginFromPortal(role)}
        />
      );
    }
    return (
      <HospitalLoginPortal 
        onLogin={handleLoginFromPortal} 
        onBackToHome={() => setPortalView('home')} 
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

  return (
    <div className="flex h-screen bg-slate-100 dark:bg-[#0B1120] overflow-hidden font-sans text-slate-800 dark:text-[#F8FAFC]">
      {/* Sidebar Navigation */}
      <Sidebar
        currentRole={currentRole}
        onOpenRAG={() => setIsRAGOpen(true)}
        onOpenEval={() => setIsEvalOpen(true)}
        activeNav={activeNav}
        setActiveNav={setActiveNav}
      />

      {/* Main Container */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        
        {/* Top Header Command Bar */}
        <header className="h-16 bg-white dark:bg-[#111827] border-b border-slate-200 dark:border-[#293548] px-5 flex items-center justify-between gap-3 z-20 shrink-0">
          
          {/* Left: Department & Campus indicator + Global Search */}
          <div className="flex items-center gap-3 flex-1 max-w-xl">
            <div className="hidden sm:flex flex-col shrink-0">
              <span className="text-xs font-bold text-slate-900 leading-tight">
                CityCare Multi-Speciality
              </span>
              <span className="text-[10px] text-blue-600 font-semibold leading-tight">
                {currentUser.department} • Central Campus
              </span>
            </div>

            {/* Global Search Button / Trigger */}
            <button
              onClick={() => setIsSearchOpen(true)}
              className="flex-1 flex items-center justify-between pl-3 pr-2.5 py-1.5 bg-slate-50 hover:bg-slate-100/80 border border-slate-200 rounded-lg text-xs text-slate-500 transition-all text-left group"
            >
              <div className="flex items-center gap-2">
                <Search className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600 transition-colors" />
                <span className="text-slate-400 group-hover:text-slate-600 truncate">
                  Search patients, appointments, EMR records, SOPs...
                </span>
              </div>
              <kbd className="hidden md:inline-flex items-center gap-0.5 px-1.5 py-0.5 text-[10px] font-mono bg-white border border-slate-200 rounded text-slate-400 shadow-2xs">
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

        {/* Quick Role Switcher Strip for Easy Testing */}
        <div className="bg-slate-100 dark:bg-slate-800/80 border-b border-slate-200 dark:border-slate-700 px-6 py-2 flex items-center gap-2 overflow-x-auto text-xs shrink-0">
          <span className="text-slate-500 dark:text-slate-400 font-bold uppercase text-[10px] tracking-wider shrink-0 mr-1">Workstations:</span>
          {[
            { role: 'DOCTOR', label: '🩺 Doctor' },
            { role: 'NURSE', label: '👩‍⚕️ Nurse' },
            { role: 'PATIENT', label: '👤 Patient' },
            { role: 'LABORATORY_STAFF', label: '🔬 Laboratory' },
            { role: 'RADIOLOGY_STAFF', label: '🩻 Radiology' },
            { role: 'PHARMACIST', label: '💊 Pharmacy' },
            { role: 'BILLING_STAFF', label: '💳 Billing' },
            { role: 'EMERGENCY_STAFF', label: '🚑 Emergency' },
            { role: 'RECEPTIONIST', label: '📋 Reception' },
            { role: 'HOSPITAL_ADMIN', label: '🏢 Admin' },
          ].map(item => (
            <button
              key={item.role}
              onClick={() => handleRoleChange(item.role as any)}
              className={`px-3 py-1 rounded-full font-medium transition-all shrink-0 cursor-pointer ${
                currentRole === item.role
                  ? 'bg-blue-600 text-white shadow-xs font-bold'
                  : 'bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-600 border border-slate-200/80 dark:border-slate-600'
              }`}
            >
              {item.label}
            </button>
          ))}
          <button
            onClick={() => setIsLoggedIn(false)}
            className="ml-auto px-3 py-1 rounded-full font-medium text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-600 shrink-0 cursor-pointer"
          >
            🌐 Landing Page
          </button>
        </div>

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
