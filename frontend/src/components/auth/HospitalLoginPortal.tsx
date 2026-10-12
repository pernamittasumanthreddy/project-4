'use client';

import React, { useState, useEffect, useRef } from 'react';
import { HospitalRole, UserProfile } from '@/lib/types/roles';
import { DEMO_USERS } from '@/lib/data/mockDatabase';
import { ROLE_CONFIGS } from '@/lib/data/roleConfigs';
import { ThemeToggle } from '../theme/ThemeToggle';
import { WorkstationLaunchModal, ROLE_CREDENTIALS } from './WorkstationLaunchModal';
import { RoleAccessScopeModal } from './RoleAccessScopeModal';
import { SecurityCenterModal } from './SecurityCenterModal';
import { GatewayNotificationPopover } from './GatewayNotificationPopover';

import { 
  Stethoscope, Building2, ShieldCheck, Heart, User, 
  Pill, FlaskConical, Scan, CreditCard, ShieldAlert, 
  Users, Building, Award, Flame, BadgeCheck, 
  Lock, ArrowRight, Bot, Sparkles, CheckCircle2, Search, 
  SlidersHorizontal, CheckSquare, ClipboardList, UserCheck, ArrowLeft,
  Shield, Bell, Server, X, Eye, EyeOff, Loader2, KeyRound, Mail
} from 'lucide-react';

interface HospitalLoginPortalProps {
  onLogin: (role: HospitalRole) => void;
  onBackToHome?: () => void;
}

type FilterCategory = 
  | 'All'
  | 'Clinical Care'
  | 'Diagnostics & Pharmacy'
  | 'Patient Access'
  | 'Administration & Executive'
  | 'Operations & Billing';

interface RoleCardData {
  role: HospitalRole;
  title: string;
  category: Exclude<FilterCategory, 'All'>;
  icon: any;
  accent: 'blue' | 'indigo' | 'red' | 'teal' | 'slate' | 'amber' | 'emerald';
  user: UserProfile;
  ctaText: string;
  statusText: string;
  docScopeCount: number;
}

const ALL_ROLE_CARDS: RoleCardData[] = [
  // 1. Attending Physician
  {
    role: 'DOCTOR',
    title: 'Attending Physician',
    category: 'Clinical Care',
    icon: Stethoscope,
    accent: 'blue',
    user: DEMO_USERS['DOCTOR'],
    ctaText: 'Launch Physician Workstation →',
    statusText: 'On Duty • Ward Rounds Active',
    docScopeCount: 16,
  },
  // 2. Staff Registered Nurse
  {
    role: 'NURSE',
    title: 'Staff Registered Nurse',
    category: 'Clinical Care',
    icon: Heart,
    accent: 'blue',
    user: DEMO_USERS['NURSE'],
    ctaText: 'Launch Nurse Station →',
    statusText: 'Shift Active • Station 3-B',
    docScopeCount: 12,
  },
  // 3. Emergency & Trauma Bay
  {
    role: 'EMERGENCY_STAFF',
    title: 'Emergency & Trauma Bay',
    category: 'Clinical Care',
    icon: Flame,
    accent: 'red',
    user: DEMO_USERS['EMERGENCY_STAFF'],
    ctaText: 'Launch Trauma Workstation →',
    statusText: 'On Duty • Level 1 Trauma Active',
    docScopeCount: 14,
  },

  // 4. Clinical Pharmacist
  {
    role: 'PHARMACIST',
    title: 'Clinical Pharmacist',
    category: 'Diagnostics & Pharmacy',
    icon: Pill,
    accent: 'teal',
    user: DEMO_USERS['PHARMACIST'],
    ctaText: 'Launch Pharmacy Workstation →',
    statusText: 'On Duty • Main Dispensing Unit',
    docScopeCount: 11,
  },
  // 5. Medical Laboratory Technologist
  {
    role: 'LABORATORY_STAFF',
    title: 'Medical Laboratory Technologist',
    category: 'Diagnostics & Pharmacy',
    icon: FlaskConical,
    accent: 'indigo',
    user: DEMO_USERS['LABORATORY_STAFF'],
    ctaText: 'Launch LIS Workstation →',
    statusText: 'Active • Central Pathology Lab',
    docScopeCount: 10,
  },
  // 6. Diagnostic Radiologist
  {
    role: 'RADIOLOGY_STAFF',
    title: 'Diagnostic Radiologist',
    category: 'Diagnostics & Pharmacy',
    icon: Scan,
    accent: 'indigo',
    user: DEMO_USERS['RADIOLOGY_STAFF'],
    ctaText: 'Launch PACS Workstation →',
    statusText: 'On Duty • Reading Room 2',
    docScopeCount: 9,
  },

  // 7. Patient Portal
  {
    role: 'PATIENT',
    title: 'Patient Portal',
    category: 'Patient Access',
    icon: UserCheck,
    accent: 'emerald',
    user: DEMO_USERS['PATIENT'],
    ctaText: 'Launch Patient Health Home →',
    statusText: 'Active Session • Room 304-B',
    docScopeCount: 6,
  },
  // 8. Patient Intake & Front Desk
  {
    role: 'RECEPTIONIST',
    title: 'Patient Intake & Front Desk',
    category: 'Patient Access',
    icon: BadgeCheck,
    accent: 'blue',
    user: DEMO_USERS['RECEPTIONIST'],
    ctaText: 'Launch Intake Workstation →',
    statusText: 'On Duty • Main Atrium Desk 1',
    docScopeCount: 8,
  },

  // 9. Hospital Administrator
  {
    role: 'HOSPITAL_ADMIN',
    title: 'Hospital Administrator',
    category: 'Administration & Executive',
    icon: Building2,
    accent: 'slate',
    user: DEMO_USERS['HOSPITAL_ADMIN'],
    ctaText: 'Launch Administration Console →',
    statusText: 'Executive Suite • Floor 6',
    docScopeCount: 17,
  },
  // 10. Cluster Super Admin
  {
    role: 'SUPER_ADMIN',
    title: 'Cluster Super Admin',
    category: 'Administration & Executive',
    icon: ShieldAlert,
    accent: 'slate',
    user: DEMO_USERS['SUPER_ADMIN'],
    ctaText: 'Launch Cluster Governance →',
    statusText: 'Root Access • Multi-Hospital Ops',
    docScopeCount: 22,
  },
  // 11. Clinical Department Manager
  {
    role: 'DEPARTMENT_MANAGER',
    title: 'Clinical Department Manager',
    category: 'Administration & Executive',
    icon: ClipboardList,
    accent: 'teal',
    user: DEMO_USERS['DEPARTMENT_MANAGER'],
    ctaText: 'Launch Department Console →',
    statusText: 'Internal Medicine Wing',
    docScopeCount: 13,
  },
  // 12. Executive Board / C-Suite Chief
  {
    role: 'MANAGEMENT_EXECUTIVE',
    title: 'Executive Board / C-Suite Chief',
    category: 'Administration & Executive',
    icon: Award,
    accent: 'indigo',
    user: DEMO_USERS['MANAGEMENT_EXECUTIVE'],
    ctaText: 'Launch Executive Scorecard →',
    statusText: 'Board of Governors • Floor 7',
    docScopeCount: 15,
  },

  // 13. Medical Billing Specialist
  {
    role: 'BILLING_STAFF',
    title: 'Medical Billing Specialist',
    category: 'Operations & Billing',
    icon: CreditCard,
    accent: 'amber',
    user: DEMO_USERS['BILLING_STAFF'],
    ctaText: 'Launch Billing Workstation →',
    statusText: 'Active • Revenue Cycle Unit',
    docScopeCount: 9,
  },
  // 14. Health Insurance & Claims Officer
  {
    role: 'INSURANCE_STAFF',
    title: 'Health Insurance & TPA Officer',
    category: 'Operations & Billing',
    icon: ShieldCheck,
    accent: 'blue',
    user: DEMO_USERS['INSURANCE_STAFF'],
    ctaText: 'Launch Claims Workstation →',
    statusText: 'Active • Claims Adjudication',
    docScopeCount: 10,
  },
  // 15. Healthcare Human Resources
  {
    role: 'HR_STAFF',
    title: 'Healthcare Human Resources',
    category: 'Operations & Billing',
    icon: Users,
    accent: 'emerald',
    user: DEMO_USERS['HR_STAFF'],
    ctaText: 'Launch HR Console →',
    statusText: 'Active • Credentialing Unit',
    docScopeCount: 11,
  },
];

const FILTER_TABS: { label: FilterCategory; count: number }[] = [
  { label: 'All', count: 15 },
  { label: 'Clinical Care', count: 3 },
  { label: 'Diagnostics & Pharmacy', count: 3 },
  { label: 'Patient Access', count: 2 },
  { label: 'Administration & Executive', count: 4 },
  { label: 'Operations & Billing', count: 3 },
];

export const HospitalLoginPortal: React.FC<HospitalLoginPortalProps> = ({ onLogin, onBackToHome }) => {
  const [selectedCategory, setSelectedCategory] = useState<FilterCategory>('All');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Modals
  const [launchingRole, setLaunchingRole] = useState<HospitalRole | null>(null);
  const [scopeRole, setScopeRole] = useState<HospitalRole | null>(null);
  const [isSecurityCenterOpen, setIsSecurityCenterOpen] = useState(false);
  const [isNotifOpen, setIsNotifOpen] = useState(false);
  const [showForgotModal, setShowForgotModal] = useState(false);

  // Two-column authentication panel state
  const [selectedAuthRole, setSelectedAuthRole] = useState<HospitalRole>('DOCTOR');
  const [authEmail, setAuthEmail] = useState(ROLE_CREDENTIALS['DOCTOR']?.email || 'marcus.vance@hopkins-health.org');
  const [authPassword, setAuthPassword] = useState(ROLE_CREDENTIALS['DOCTOR']?.defaultPassword || 'DocCardio#2024');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [isAuthenticating, setIsAuthenticating] = useState(false);
  const [authError, setAuthError] = useState<string | null>(null);

  const resolveRoleFromEmail = (email: string): HospitalRole | null => {
    const clean = email.toLowerCase().trim();
    for (const [role, creds] of Object.entries(ROLE_CREDENTIALS)) {
      if (creds.email.toLowerCase() === clean) return role as HospitalRole;
    }
    if (clean.includes('doc') || clean.includes('vance')) return 'DOCTOR';
    if (clean.includes('nurse') || clean.includes('jenkins')) return 'NURSE';
    if (clean.includes('trauma') || clean.includes('thorne') || clean.includes('emergency')) return 'EMERGENCY_STAFF';
    if (clean.includes('pharm') || clean.includes('miller')) return 'PHARMACIST';
    if (clean.includes('lab') || clean.includes('chen')) return 'LABORATORY_STAFF';
    if (clean.includes('rad') || clean.includes('blake')) return 'RADIOLOGY_STAFF';
    if (clean.includes('patient') || clean.includes('anderson')) return 'PATIENT';
    if (clean.includes('reception')) return 'RECEPTIONIST';
    if (clean.includes('bill') || clean.includes('claire')) return 'BILLING_STAFF';
    if (clean.includes('insur') || clean.includes('chang')) return 'INSURANCE_STAFF';
    if (clean.includes('hr') || clean.includes('davis')) return 'HR_STAFF';
    if (clean.includes('dept') || clean.includes('house')) return 'DEPARTMENT_MANAGER';
    if (clean.includes('exec') || clean.includes('hastings')) return 'MANAGEMENT_EXECUTIVE';
    if (clean.includes('superadmin')) return 'SUPER_ADMIN';
    if (clean.includes('admin')) return 'HOSPITAL_ADMIN';
    return null;
  };

  const handleAuthSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!authEmail.trim()) {
      setAuthError('Please enter your Institutional User ID or Email.');
      return;
    }
    if (!authPassword.trim()) {
      setAuthError('Please enter your workstation password.');
      return;
    }
    const resolved = resolveRoleFromEmail(authEmail) || selectedAuthRole;
    setAuthError(null);
    setIsAuthenticating(true);
    setTimeout(() => {
      setIsAuthenticating(false);
      onLogin(resolved);
    }, 250);
  };

  const searchInputRef = useRef<HTMLInputElement>(null);

  // Keyboard shortcut '/' to focus search
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === '/' && document.activeElement !== searchInputRef.current) {
        e.preventDefault();
        searchInputRef.current?.focus();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Filter roles
  const filteredRoles = ALL_ROLE_CARDS.filter((item) => {
    const matchesCategory = selectedCategory === 'All' || item.category === selectedCategory;
    const query = searchQuery.toLowerCase().trim();
    const matchesSearch = 
      !query ||
      item.title.toLowerCase().includes(query) ||
      item.user.name.toLowerCase().includes(query) ||
      item.user.department.toLowerCase().includes(query) ||
      (item.user.employeeId && item.user.employeeId.toLowerCase().includes(query)) ||
      item.role.toLowerCase().includes(query);

    return matchesCategory && matchesSearch;
  });

  const getAccentStyles = (accent: RoleCardData['accent']) => {
    switch (accent) {
      case 'red':
        return {
          iconBg: 'bg-rose-50 dark:bg-rose-950/40 text-rose-600 dark:text-rose-400 border-rose-200 dark:border-rose-800/60',
          badge: 'bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-300 border-rose-200 dark:border-rose-800/60',
          hoverBorder: 'hover:border-rose-300 dark:hover:border-rose-700/60',
          dot: 'bg-rose-500',
        };
      case 'teal':
        return {
          iconBg: 'bg-teal-50 dark:bg-teal-950/40 text-teal-600 dark:text-teal-400 border-teal-200 dark:border-teal-800/60',
          badge: 'bg-teal-50 dark:bg-teal-950/40 text-teal-700 dark:text-teal-300 border-teal-200 dark:border-teal-800/60',
          hoverBorder: 'hover:border-teal-300 dark:hover:border-teal-700/60',
          dot: 'bg-teal-500',
        };
      case 'indigo':
        return {
          iconBg: 'bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 border-indigo-200 dark:border-indigo-800/60',
          badge: 'bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-300 border-indigo-200 dark:border-indigo-800/60',
          hoverBorder: 'hover:border-indigo-300 dark:hover:border-indigo-700/60',
          dot: 'bg-indigo-500',
        };
      case 'amber':
        return {
          iconBg: 'bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 border-amber-200 dark:border-amber-800/60',
          badge: 'bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-amber-800/60',
          hoverBorder: 'hover:border-amber-300 dark:hover:border-amber-700/60',
          dot: 'bg-amber-500',
        };
      case 'emerald':
        return {
          iconBg: 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800/60',
          badge: 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800/60',
          hoverBorder: 'hover:border-emerald-300 dark:hover:border-emerald-700/60',
          dot: 'bg-emerald-500',
        };
      case 'slate':
        return {
          iconBg: 'bg-slate-100 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700',
          badge: 'bg-slate-100 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700',
          hoverBorder: 'hover:border-slate-400 dark:hover:border-slate-600',
          dot: 'bg-slate-500',
        };
      case 'blue':
      default:
        return {
          iconBg: 'bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-800/60',
          badge: 'bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800/60',
          hoverBorder: 'hover:border-blue-300 dark:hover:border-blue-700/60',
          dot: 'bg-blue-500',
        };
    }
  };

  return (
    <div className="min-h-screen bg-[#F5F8FC] dark:bg-[#0B1120] text-[#0F172A] dark:text-[#F8FAFC] transition-colors duration-200 flex flex-col font-sans">
      {/* 1. STICKY ENTERPRISE HEADER */}
      <header className="sticky top-0 z-40 border-b border-[#DCE4EF] dark:border-[#293548] bg-white/95 dark:bg-[#111827]/95 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between gap-4">
          {/* Left: Hospital Brand & Trust Badges */}
          <div className="flex items-center gap-3.5 min-w-0">
            <div className="w-10 h-10 rounded-xl bg-linear-to-br from-[#1E3A8A] to-[#2563EB] flex items-center justify-center text-white shadow-xs shrink-0">
              <Building2 className="w-5 h-5" />
            </div>

            <div className="min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="font-bold text-base sm:text-lg text-[#0F172A] dark:text-[#F8FAFC] tracking-tight truncate">
                  CityCare Multi-Speciality Hospital
                </span>
                <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300 border border-blue-200 dark:border-blue-800/60 shrink-0">
                  Central Campus
                </span>
                <span className="hidden sm:inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60 shrink-0">
                  <ShieldCheck className="w-3 h-3" /> HIPAA / HITECH Compliant
                </span>
              </div>
              <p className="text-[11px] text-[#64748B] dark:text-[#A8B4C7] truncate hidden md:block">
                Enterprise Role Authentication Hub • Isolated Multi-RAG Assistants Gateway
              </p>
            </div>
          </div>

          {/* Right: Security Status, Notifications, Theme, Security Center */}
          <div className="flex items-center gap-2 sm:gap-3 shrink-0">
            {/* Active Directory Connected Indicator */}
            <div className="hidden lg:flex items-center gap-2 px-2.5 py-1.5 rounded-lg border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#172033] shadow-2xs">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
              </span>
              <span className="text-xs font-medium text-slate-700 dark:text-slate-200">
                Active Directory Connected
              </span>
            </div>

            {/* 15 Roles Badge */}
            <span className="hidden xl:inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1.5 rounded-lg bg-blue-50 dark:bg-blue-950/50 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
              <CheckCircle2 className="w-3.5 h-3.5" /> 15 Enterprise RBAC Roles
            </span>

            {/* Security Center trigger */}
            <button
              type="button"
              onClick={() => setIsSecurityCenterOpen(true)}
              className="hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#172033] hover:bg-slate-50 dark:hover:bg-[#1D293D] text-[#0F172A] dark:text-[#F8FAFC] text-xs font-semibold shadow-2xs transition-colors"
              title="View Security & Compliance Center"
            >
              <Shield className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
              <span>Security Center</span>
            </button>

            {/* Notification Bell */}
            <div className="relative">
              <button
                type="button"
                onClick={() => setIsNotifOpen(!isNotifOpen)}
                className="relative p-2 rounded-lg border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#172033] hover:bg-slate-50 dark:hover:bg-[#1D293D] text-slate-600 dark:text-slate-300 transition-colors shadow-2xs"
                aria-label="View notifications"
              >
                <Bell className="w-4 h-4" />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-blue-600 ring-2 ring-white dark:ring-[#111827]" />
              </button>

              <GatewayNotificationPopover 
                isOpen={isNotifOpen} 
                onClose={() => setIsNotifOpen(false)} 
              />
            </div>

            {/* Back to Hospital Home */}
            {onBackToHome && (
              <button
                type="button"
                onClick={onBackToHome}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#172033] hover:bg-slate-50 dark:hover:bg-[#1D293D] text-[#0F172A] dark:text-[#F8FAFC] text-xs font-semibold shadow-2xs transition-colors shrink-0"
                title="Return to Welcome Home Page"
              >
                <ArrowLeft className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
                <span className="hidden sm:inline">Hospital Home</span>
              </button>
            )}

            {/* Theme Toggle (Light / Dark / System) */}
            <ThemeToggle variant="pill" />
          </div>
        </div>
      </header>

      {/* MAIN CONTAINER */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        {/* 2. TWO-COLUMN MASTER ENTERPRISE LOGIN PANEL */}
        <section className="mb-10 grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-8 items-stretch">
          {/* LEFT COLUMN: Deep Navy Branding & Hospital Identity Panel (#123B52) */}
          <div className="lg:col-span-6 bg-[#123B52] text-[#D7E6EE] rounded-2xl p-6 sm:p-9 shadow-md flex flex-col justify-between border border-[#0B2C3D] relative overflow-hidden">
            {/* Background Medical Tone Glow */}
            <div className="absolute top-0 right-0 w-72 h-72 bg-radial from-[#0F8B8D]/25 via-transparent to-transparent pointer-events-none -mr-20 -mt-20 rounded-full" />

            <div>
              {/* Hospital Badge */}
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#0B2C3D] border border-[#0F8B8D]/40 text-[#D7E6EE] text-xs font-semibold mb-5">
                <ShieldCheck className="w-4 h-4 text-[#0F8B8D]" />
                <span>CityCare Multispecialty Hospital Network</span>
              </div>

              {/* Title & Welcome */}
              <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight leading-tight">
                Enterprise Clinical & Hospital Operating System
              </h1>

              <p className="mt-3 text-xs sm:text-sm text-[#D7E6EE]/85 leading-relaxed">
                Integrated workstation authentication for clinical practitioners, registered nursing staff, diagnostic laboratory, pharmacy, radiology PACS, and hospital administrative leadership.
              </p>

              {/* Security & Operational Badges */}
              <div className="grid grid-cols-3 gap-2.5 sm:gap-3 mt-6 pt-6 border-t border-[#0B2C3D]">
                <div className="p-3 rounded-xl bg-[#0B2C3D]/70 border border-[#0F8B8D]/20">
                  <div className="text-[10px] uppercase font-bold text-[#D7E6EE]/60 tracking-wider">Accreditation</div>
                  <div className="text-xs sm:text-sm font-bold text-white mt-0.5">HIPAA / HITECH</div>
                  <div className="text-[10px] text-teal-300 mt-0.5">Level 3 Verified</div>
                </div>
                <div className="p-3 rounded-xl bg-[#0B2C3D]/70 border border-[#0F8B8D]/20">
                  <div className="text-[10px] uppercase font-bold text-[#D7E6EE]/60 tracking-wider">Directories</div>
                  <div className="text-xs sm:text-sm font-bold text-white mt-0.5">Kerberos AD</div>
                  <div className="text-[10px] text-emerald-400 mt-0.5">SSO Connected</div>
                </div>
                <div className="p-3 rounded-xl bg-[#0B2C3D]/70 border border-[#0F8B8D]/20">
                  <div className="text-[10px] uppercase font-bold text-[#D7E6EE]/60 tracking-wider">Isolation</div>
                  <div className="text-xs sm:text-sm font-bold text-white mt-0.5">15 Workstations</div>
                  <div className="text-[10px] text-blue-300 mt-0.5">RBAC Sandboxes</div>
                </div>
              </div>
            </div>

            {/* Quick Role Preset Picker (Evaluator / Reviewer Assistant) */}
            <div className="mt-6 pt-5 border-t border-[#0B2C3D]">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-white flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-[#0F8B8D]" />
                  <span>Quick-Fill Workstation Role:</span>
                </span>
                <span className="text-[10px] text-[#D7E6EE]/60">Select to test</span>
              </div>
              <div className="flex items-center gap-1.5 flex-wrap">
                {(['DOCTOR', 'NURSE', 'EMERGENCY_STAFF', 'PHARMACIST', 'LABORATORY_STAFF', 'RADIOLOGY_STAFF', 'PATIENT', 'HOSPITAL_ADMIN', 'SUPER_ADMIN'] as HospitalRole[]).map((r) => {
                  const isSelected = selectedAuthRole === r;
                  const label = ROLE_CONFIGS[r]?.displayName || r;
                  return (
                    <button
                      key={r}
                      type="button"
                      onClick={() => {
                        setSelectedAuthRole(r);
                        setAuthEmail(ROLE_CREDENTIALS[r].email);
                        setAuthPassword(ROLE_CREDENTIALS[r].defaultPassword);
                        setAuthError(null);
                      }}
                      className={`text-[11px] px-2.5 py-1 rounded-lg font-medium transition-all cursor-pointer ${
                        isSelected
                          ? 'bg-[#0F8B8D] text-white font-bold shadow-xs'
                          : 'bg-[#0B2C3D] text-[#D7E6EE] hover:bg-[#082230] hover:text-white'
                      }`}
                    >
                      {label}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* RIGHT COLUMN: White Authentication Panel (#FFFFFF, Teal Button #0F8B8D) */}
          <div className="lg:col-span-6 bg-white dark:bg-[#111827] rounded-2xl p-6 sm:p-9 shadow-md border border-[#DCE4EA] dark:border-[#293548] flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-xl sm:text-2xl font-bold text-[#1E293B] dark:text-white tracking-tight">
                  Workstation Authentication
                </h2>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-teal-50 dark:bg-teal-950/60 text-[#0F8B8D] font-bold border border-teal-200 dark:border-teal-800">
                  TLS 1.3 SECURE
                </span>
              </div>

              <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mb-6">
                Enter your institutional User ID or corporate email to initialize your clinical session.
              </p>

              {/* Form */}
              <form onSubmit={handleAuthSubmit} className="space-y-4">
                {/* User ID / Email */}
                <div>
                  <label className="block text-xs font-semibold text-[#1E293B] dark:text-[#F8FAFC] mb-1.5">
                    Institutional Email / User ID
                  </label>
                  <div className="relative">
                    <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                    <input
                      type="text"
                      value={authEmail}
                      onChange={(e) => {
                        setAuthEmail(e.target.value);
                        setAuthError(null);
                      }}
                      placeholder="e.g. physician@hopkins-health.org"
                      className="w-full pl-10 pr-3.5 py-2.5 rounded-xl border border-[#DCE4EA] dark:border-[#293548] bg-white dark:bg-[#0F172A] text-[#1E293B] dark:text-white text-xs font-mono focus:outline-hidden focus:ring-2 focus:ring-[#0F8B8D]/50 focus:border-[#0F8B8D] transition-all"
                    />
                  </div>
                </div>

                {/* Password with Visibility Toggle */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-semibold text-[#1E293B] dark:text-[#F8FAFC]">
                      Password
                    </label>
                    <button
                      type="button"
                      onClick={() => setShowForgotModal(true)}
                      className="text-xs font-semibold text-[#0F8B8D] hover:underline cursor-pointer"
                    >
                      Forgot password?
                    </button>
                  </div>
                  <div className="relative">
                    <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={authPassword}
                      onChange={(e) => {
                        setAuthPassword(e.target.value);
                        setAuthError(null);
                      }}
                      placeholder="Enter password"
                      className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-[#DCE4EA] dark:border-[#293548] bg-white dark:bg-[#0F172A] text-[#1E293B] dark:text-white text-xs font-mono focus:outline-hidden focus:ring-2 focus:ring-[#0F8B8D]/50 focus:border-[#0F8B8D] transition-all"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1 cursor-pointer"
                      title={showPassword ? 'Hide password' : 'Show password'}
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Remember Me Checkbox */}
                <div className="flex items-center justify-between text-xs pt-1">
                  <label className="flex items-center gap-2 cursor-pointer text-[#64748B] dark:text-[#A8B4C7]">
                    <input
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      className="w-4 h-4 rounded-sm border-[#DCE4EA] text-[#0F8B8D] focus:ring-[#0F8B8D]"
                    />
                    <span>Remember workstation session</span>
                  </label>
                  <span className="text-[11px] text-slate-400">15-min idle timeout</span>
                </div>

                {/* Error Banner */}
                {authError && (
                  <div className="p-3 rounded-xl bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 text-xs flex items-center gap-2 animate-in fade-in">
                    <ShieldAlert className="w-4 h-4 shrink-0 text-red-600" />
                    <span>{authError}</span>
                  </div>
                )}

                {/* Primary Teal Login Button */}
                <button
                  type="submit"
                  disabled={isAuthenticating}
                  className="w-full h-12 rounded-xl bg-[#0F8B8D] hover:bg-[#0B7476] active:bg-[#085B5D] text-white font-bold text-xs uppercase tracking-wider flex items-center justify-center gap-2 shadow-sm hover:shadow-md transition-all cursor-pointer disabled:opacity-75"
                >
                  {isAuthenticating ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin text-white" />
                      <span>Authenticating Workstation...</span>
                    </>
                  ) : (
                    <>
                      <span>Sign In to Workstation</span>
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              </form>
            </div>

            {/* Quick Demo Helper Hint */}
            <div className="mt-6 pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-[11px] text-[#64748B] dark:text-[#A8B4C7]">
              <span>Active Role: <strong className="text-[#1E293B] dark:text-white font-semibold">{ROLE_CONFIGS[selectedAuthRole]?.displayName || selectedAuthRole}</strong></span>
              <span className="text-teal-600 dark:text-teal-400 font-medium">Session audit enabled</span>
            </div>
          </div>
        </section>

        {/* 3. NAVIGATION FILTERS & SEARCH BAR */}
        <section className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-2 sm:p-2.5 rounded-xl bg-white dark:bg-[#111827] border border-[#DCE4EF] dark:border-[#293548] shadow-xs">
            {/* Filter Pills */}
            <div className="flex items-center gap-1.5 overflow-x-auto pb-2 md:pb-0 scrollbar-none">
              {FILTER_TABS.map((tab) => {
                const isSelected = selectedCategory === tab.label;
                return (
                  <button
                    key={tab.label}
                    type="button"
                    onClick={() => setSelectedCategory(tab.label)}
                    className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                      isSelected
                        ? 'bg-[#2563EB] text-white shadow-xs font-bold'
                        : 'bg-transparent text-[#64748B] dark:text-[#A8B4C7] hover:text-[#0F172A] dark:hover:text-white hover:bg-slate-100 dark:hover:bg-[#172033]'
                    }`}
                  >
                    <span>{tab.label}</span>
                    <span className={`text-[10px] px-1.5 py-0.2 rounded-full font-mono ${
                      isSelected 
                        ? 'bg-blue-800 text-white' 
                        : 'bg-slate-100 dark:bg-[#1D293D] text-slate-500 dark:text-slate-400'
                    }`}>
                      {tab.count}
                    </span>
                  </button>
                );
              })}
            </div>

            {/* Search Input */}
            <div className="relative md:w-80 shrink-0">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 dark:text-slate-500 pointer-events-none" />
              <input
                ref={searchInputRef}
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by role, clinician, department..."
                className="w-full pl-9 pr-14 py-2 text-xs rounded-lg border border-[#DCE4EF] dark:border-[#293548] bg-[#F5F8FC] dark:bg-[#0F172A] text-[#0F172A] dark:text-[#F8FAFC] placeholder-slate-400 focus:outline-hidden focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all"
              />
              <div className="absolute right-2.5 top-1/2 -translate-y-1/2 flex items-center gap-1">
                {searchQuery ? (
                  <button
                    type="button"
                    onClick={() => setSearchQuery('')}
                    className="p-1 rounded-md text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                    title="Clear search"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                ) : (
                  <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] font-mono font-semibold rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#172033] text-slate-400">
                    /
                  </kbd>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* 4. WORKSTATION ROLE CARDS (RESPONSIVE GRID) */}
        {filteredRoles.length > 0 ? (
          <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredRoles.map((item) => {
              const IconComponent = item.icon;
              const config = ROLE_CONFIGS[item.role];
              const accentStyles = getAccentStyles(item.accent);

              return (
                <div
                  key={item.role}
                  className={`group relative flex flex-col justify-between rounded-2xl bg-white dark:bg-[#111827] border border-[#DCE4EF] dark:border-[#293548] p-5 sm:p-6 shadow-xs transition-all duration-200 hover:-translate-y-1 hover:shadow-md ${accentStyles.hoverBorder}`}
                >
                  <div>
                    {/* Top Card Row: Icon & Category Badge */}
                    <div className="flex items-start justify-between gap-3 mb-4">
                      <div className={`w-12 h-12 rounded-xl border flex items-center justify-center shrink-0 transition-transform group-hover:scale-105 duration-200 ${accentStyles.iconBg}`}>
                        <IconComponent className="w-6 h-6" />
                      </div>

                      <span className={`text-[11px] font-semibold px-2.5 py-1 rounded-md border ${accentStyles.badge}`}>
                        {item.category}
                      </span>
                    </div>

                    {/* Role Title & Description */}
                    <h3 className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                      {item.title}
                    </h3>
                    <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] leading-relaxed line-clamp-2 mb-4">
                      {config?.knowledgeScopeDescription || 'Clinical workstation with authorized medical records and verified hospital knowledge vectors.'}
                    </p>

                    {/* Credential Identity Panel */}
                    <div className="p-3.5 mb-4 rounded-xl border border-[#DCE4EF] dark:border-[#293548] bg-[#F5F8FC] dark:bg-[#172033]">
                      <div className="flex items-center justify-between mb-1.5">
                        <span className="text-xs font-bold text-[#0F172A] dark:text-[#F8FAFC] truncate">
                          {item.user.name}
                        </span>
                        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded-md bg-white dark:bg-[#1D293D] border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
                          {item.user.employeeId || 'CRED-SYS'}
                        </span>
                      </div>

                      <div className="flex items-center justify-between text-[11px] text-[#64748B] dark:text-[#A8B4C7]">
                        <span className="truncate">{item.user.department}</span>
                        <span className="flex items-center gap-1.5 shrink-0 font-medium text-slate-600 dark:text-slate-300">
                          <span className={`w-1.5 h-1.5 rounded-full ${accentStyles.dot}`} />
                          {item.statusText.split('•')[0].trim()}
                        </span>
                      </div>
                    </div>

                    {/* Dedicated Grounded RAG Panel */}
                    <div className="p-3 mb-5 rounded-xl border border-blue-100 dark:border-blue-900/50 bg-blue-50/30 dark:bg-blue-950/20 flex items-start gap-2.5">
                      <div className="mt-0.5 shrink-0 text-blue-600 dark:text-blue-400">
                        <Sparkles className="w-4 h-4" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-[10px] font-bold uppercase tracking-wider text-blue-700 dark:text-blue-300">
                          Dedicated Grounded RAG
                        </div>
                        <div className="text-xs font-semibold text-[#0F172A] dark:text-[#F8FAFC] truncate mt-0.5">
                          {config?.ragTitle || 'Sandboxed Knowledge Assistant'}
                        </div>
                        <div className="flex items-center gap-1 text-[11px] text-slate-500 dark:text-slate-400 mt-1">
                          <Lock className="w-3 h-3 text-slate-400" />
                          <span>Restricted: {item.docScopeCount} verified SOP partitions</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Actions: Primary CTA & Secondary View Scope */}
                  <div className="space-y-2 pt-2 border-t border-slate-100 dark:border-slate-800/80">
                    <button
                      type="button"
                      onClick={() => setLaunchingRole(item.role)}
                      className="group/btn relative w-full h-11 rounded-xl font-semibold text-xs text-white bg-linear-to-r from-[#1E3A8A] to-[#2563EB] hover:from-[#1D4ED8] hover:to-[#2563EB] dark:from-[#2563EB] dark:to-[#3B82F6] dark:hover:from-[#1D4ED8] dark:hover:to-[#2563EB] shadow-xs hover:shadow-md transition-all active:scale-[0.98] flex items-center justify-center gap-2 cursor-pointer"
                    >
                      <Lock className="w-3.5 h-3.5" />
                      <span>{item.ctaText}</span>
                      <ArrowRight className="w-4 h-4 transition-transform group-hover/btn:translate-x-1" />
                    </button>

                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        onClick={() => onLogin(item.role)}
                        className="flex-1 py-1.5 rounded-lg text-xs font-semibold text-blue-700 dark:text-blue-300 bg-blue-50 dark:bg-blue-950/40 hover:bg-blue-100 dark:hover:bg-blue-900/40 border border-blue-200 dark:border-blue-800 transition-colors text-center cursor-pointer"
                        title="Enter directly into dashboard"
                      >
                        ⚡ Quick Enter
                      </button>

                      <button
                        type="button"
                        onClick={() => setScopeRole(item.role)}
                        className="flex-1 py-1.5 rounded-lg text-xs font-semibold text-[#64748B] dark:text-[#A8B4C7] hover:text-[#0F172A] dark:hover:text-white hover:bg-slate-100 dark:hover:bg-[#172033] border border-transparent hover:border-slate-200 dark:hover:border-slate-800 transition-colors text-center cursor-pointer"
                      >
                        Scope & Security
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </section>
        ) : (
          /* 5. EMPTY SEARCH STATE */
          <div className="text-center py-16 px-4 rounded-2xl bg-white dark:bg-[#111827] border border-[#DCE4EF] dark:border-[#293548]">
            <div className="w-12 h-12 rounded-full bg-slate-100 dark:bg-[#1D293D] flex items-center justify-center mx-auto mb-3 text-slate-400">
              <Search className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-[#0F172A] dark:text-[#F8FAFC]">
              No matching workstations found
            </h3>
            <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-1 max-w-sm mx-auto">
              We couldn't find any workstations matching "{searchQuery}". Try searching by role title, clinician name, or department.
            </p>
            <button
              type="button"
              onClick={() => { setSearchQuery(''); setSelectedCategory('All'); }}
              className="mt-4 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-2xs transition-colors"
            >
              Clear Search & Show All Roles
            </button>
          </div>
        )}
      </main>

      {/* 6. ENTERPRISE SECURITY FOOTER */}
      <footer className="border-t border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#111827] py-6 transition-colors">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-[#64748B] dark:text-[#A8B4C7]">
            <div className="flex items-center gap-3 flex-wrap justify-center md:justify-start">
              <span className="flex items-center gap-1.5 font-medium text-slate-700 dark:text-slate-300">
                <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                SECURE IDENTITY GATEWAY
              </span>
              <span className="hidden sm:inline text-slate-300 dark:text-slate-700">•</span>
              <span>Kerberos AD Single Sign-On</span>
              <span className="hidden sm:inline text-slate-300 dark:text-slate-700">•</span>
              <span>15-Minute Clinical Idle Timeout</span>
              <span className="hidden sm:inline text-slate-300 dark:text-slate-700">•</span>
              <span className="font-mono text-[11px]">SHA-256 Audit Stream Active</span>
            </div>

            <div className="flex items-center gap-4">
              <button
                type="button"
                onClick={() => setIsSecurityCenterOpen(true)}
                className="text-blue-600 dark:text-blue-400 hover:underline font-semibold"
              >
                Security & Compliance
              </button>
              <span className="text-slate-300 dark:text-slate-700">•</span>
              <span>FedRAMP High Ready</span>
              <span className="text-slate-300 dark:text-slate-700">•</span>
              <span>v2.8 Enterprise</span>
            </div>
          </div>
        </div>
      </footer>

      {/* Modals */}
      <WorkstationLaunchModal
        role={launchingRole}
        isOpen={!!launchingRole}
        onComplete={(role) => {
          setLaunchingRole(null);
          onLogin(role);
        }}
        onCancel={() => setLaunchingRole(null)}
      />

      <RoleAccessScopeModal
        role={scopeRole}
        isOpen={!!scopeRole}
        onClose={() => setScopeRole(null)}
        onLaunch={(role) => {
          setScopeRole(null);
          setLaunchingRole(role);
        }}
      />

      <SecurityCenterModal
        isOpen={isSecurityCenterOpen}
        onClose={() => setIsSecurityCenterOpen(false)}
      />

      {/* Institutional Password Reset Modal */}
      {showForgotModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 dark:bg-black/75 backdrop-blur-xs animate-in fade-in">
          <div className="relative w-full max-w-md bg-white dark:bg-[#111827] border border-[#DCE4EA] dark:border-slate-800 rounded-2xl p-6 shadow-2xl">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2 text-[#123B52] dark:text-teal-400 font-bold text-base">
                <KeyRound className="w-5 h-5 text-[#0F8B8D]" />
                <span>Password Recovery Assistance</span>
              </div>
              <button
                type="button"
                onClick={() => setShowForgotModal(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed mb-4">
              Clinical workstations authenticate via Kerberos Active Directory federated SSO. To reset your hospital password, contact the Enterprise IT Operations Helpdesk or use the quick role autofill presets.
            </p>
            <div className="p-3 rounded-xl bg-slate-50 dark:bg-[#1A2436] border border-slate-200 dark:border-slate-700 text-xs space-y-1 mb-5">
              <div className="flex justify-between">
                <span className="text-slate-500">IT Helpdesk Ext:</span>
                <span className="font-mono font-bold text-slate-800 dark:text-white">x4400 (Internal)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Self-Service Portal:</span>
                <span className="font-mono text-teal-600 dark:text-teal-400">ad.hopkins-health.org/sspr</span>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setShowForgotModal(false)}
              className="w-full h-10 rounded-xl bg-[#0F8B8D] hover:bg-[#0B7476] text-white font-bold text-xs"
            >
              Return to Workstation Login
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
