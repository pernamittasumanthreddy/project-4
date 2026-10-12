'use client';

import React, { useState } from 'react';
import { HospitalRole } from '@/lib/types/roles';
import { ThemeToggle } from '../theme/ThemeToggle';
import { WorkstationLaunchModal } from '../auth/WorkstationLaunchModal';
import { 
  Building2, ShieldCheck, ArrowRight, Stethoscope, Heart, 
  Flame, Pill, FlaskConical, Scan, Users, Lock, Sparkles, 
  CheckCircle2, Phone, Activity, Award, 
  ChevronRight, UserCheck, Shield, HelpCircle,
  CreditCard, ShieldAlert, ClipboardList, BadgeCheck, FileText,
  Clock, Check
} from 'lucide-react';

interface HospitalHomePageProps {
  onOpenLogins: () => void;
  onQuickLogin: (role: HospitalRole) => void;
}

type RoleCategory = 'all' | 'clinical' | 'diagnostics' | 'admin' | 'operations';

interface HomeRoleItem {
  role: HospitalRole;
  title: string;
  category: 'clinical' | 'diagnostics' | 'admin' | 'operations';
  categoryLabel: string;
  demoStaff: string;
  department: string;
  desc: string;
  icon: any;
  accent: 'blue' | 'teal' | 'red' | 'indigo' | 'slate' | 'emerald' | 'amber';
}

const ALL_15_ROLES: HomeRoleItem[] = [
  // 1. Doctor
  {
    role: 'DOCTOR',
    title: 'Attending Physician',
    category: 'clinical',
    categoryLabel: 'Clinical Care',
    demoStaff: 'Dr. Marcus Vance, MD (DOC-401)',
    department: 'Cardiology',
    desc: 'Inpatient ward rounds, bedside EMR charts, CPOE diagnostic orders, and clinical guidelines.',
    icon: Stethoscope,
    accent: 'blue',
  },
  // 2. Nurse
  {
    role: 'NURSE',
    title: 'Staff Registered Nurse',
    category: 'clinical',
    categoryLabel: 'Clinical Care',
    demoStaff: 'Sarah Jenkins, BSN, RN (NUR-204)',
    department: 'Cardiac Inpatient Ward',
    desc: 'Bedside telemetry logging, 5-rights medication administration, and SBAR shift handovers.',
    icon: Heart,
    accent: 'blue',
  },
  // 3. Emergency
  {
    role: 'EMERGENCY_STAFF',
    title: 'Emergency & Trauma Bay',
    category: 'clinical',
    categoryLabel: 'Clinical Care',
    demoStaff: 'Dr. Robert Thorne, MD (ED-112)',
    department: 'Emergency & Trauma Bay',
    desc: 'Level 1 Trauma command, ESI 1-5 triage queue, ACLS Code Blue resuscitation protocols.',
    icon: Flame,
    accent: 'red',
  },
  // 4. Pharmacist
  {
    role: 'PHARMACIST',
    title: 'Clinical Pharmacist',
    category: 'diagnostics',
    categoryLabel: 'Pharmacy',
    demoStaff: 'Dr. Samuel Miller, PharmD (PH-302)',
    department: 'Central Pharmacy',
    desc: 'CPOE prescription verification, formulary inventory, and 24/7 cold-chain telemetry.',
    icon: Pill,
    accent: 'teal',
  },
  // 5. Laboratory
  {
    role: 'LABORATORY_STAFF',
    title: 'Medical Laboratory Technologist',
    category: 'diagnostics',
    categoryLabel: 'Diagnostics',
    demoStaff: 'David Chen, MLS (LAB-503)',
    department: 'Pathology & Central Lab',
    desc: 'LIS test accessioning, STAT vs routine queues, panic value alerts, and Roche analyzer QC.',
    icon: FlaskConical,
    accent: 'indigo',
  },
  // 6. Radiology
  {
    role: 'RADIOLOGY_STAFF',
    title: 'Diagnostic Radiologist',
    category: 'diagnostics',
    categoryLabel: 'Diagnostics',
    demoStaff: 'Dr. Jonathan Blake, MD (RAD-601)',
    department: 'Diagnostic Imaging / PACS',
    desc: 'CT, MRI, X-Ray modality queues, DICOM viewer simulation, and ACR contrast checklists.',
    icon: Scan,
    accent: 'indigo',
  },
  // 7. Patient Portal
  {
    role: 'PATIENT',
    title: 'Patient Health Home',
    category: 'operations',
    categoryLabel: 'Patient Access',
    demoStaff: 'John Anderson (MRN-884920)',
    department: 'Cardiology Care Team',
    desc: 'Active medications with plain instructions, verified lab reports, and bill pay portal.',
    icon: UserCheck,
    accent: 'emerald',
  },
  // 8. Receptionist
  {
    role: 'RECEPTIONIST',
    title: 'Patient Intake & Front Desk',
    category: 'operations',
    categoryLabel: 'Patient Access',
    demoStaff: 'Jessica Gomez (REC-102)',
    department: 'Outpatient Ambulatory Desk',
    desc: 'Walk-in registration, appointment scheduling, queue tokens, and RFID visitor badges.',
    icon: BadgeCheck,
    accent: 'blue',
  },
  // 9. Hospital Admin
  {
    role: 'HOSPITAL_ADMIN',
    title: 'Hospital Administrator',
    category: 'admin',
    categoryLabel: 'Administration',
    demoStaff: 'Dr. Arthur Pendelton (EMP-0010)',
    department: 'Hospital Administration',
    desc: '18-department workload matrices, 520-bed census, quality indices, and SOP repository.',
    icon: Building2,
    accent: 'slate',
  },
  // 10. Super Admin
  {
    role: 'SUPER_ADMIN',
    title: 'Cluster Super Admin',
    category: 'admin',
    categoryLabel: 'Governance',
    demoStaff: 'Alexander Sterling (EMP-0001)',
    department: 'Multi-Hospital Cluster HQ',
    desc: 'Multi-tenant cluster governance (HOSP-01 to HOSP-04), 15-role RBAC matrix, and SHA-256 logs.',
    icon: ShieldAlert,
    accent: 'slate',
  },
  // 11. Department Manager
  {
    role: 'DEPARTMENT_MANAGER',
    title: 'Clinical Department Manager',
    category: 'admin',
    categoryLabel: 'Administration',
    demoStaff: 'Dr. Gregory House (MGR-101)',
    department: 'Internal Medicine Wing',
    desc: 'Title 22 & ANA nurse-to-patient staffing ratios, float nurse deployment, and equipment QC.',
    icon: ClipboardList,
    accent: 'teal',
  },
  // 12. Management Executive
  {
    role: 'MANAGEMENT_EXECUTIVE',
    title: 'Executive Board / C-Suite Chief',
    category: 'admin',
    categoryLabel: 'Governance',
    demoStaff: 'Victoria Hastings, COO (EXEC-002)',
    department: 'Executive Board Suite',
    desc: 'C-Suite scorecard, service line margins, EBITDA analytics, and Leapfrog Grade A metrics.',
    icon: Award,
    accent: 'indigo',
  },
  // 13. Billing Staff
  {
    role: 'BILLING_STAFF',
    title: 'Medical Billing Specialist',
    category: 'operations',
    categoryLabel: 'Revenue Cycle',
    demoStaff: 'Claire Henderson (BIL-701)',
    department: 'Billing & Finance Annex',
    desc: 'Revenue KPIs, inpatient invoices, payments collection, and Chargemaster tariff schedule.',
    icon: CreditCard,
    accent: 'amber',
  },
  // 14. Insurance Staff
  {
    role: 'INSURANCE_STAFF',
    title: 'Health Insurance & TPA Officer',
    category: 'operations',
    categoryLabel: 'Revenue Cycle',
    demoStaff: 'Michael Chang, CPA (INS-802)',
    department: 'Insurance Services',
    desc: 'TPA claims center, pre-authorization reviews, claim adjudication, and payer contracts.',
    icon: ShieldCheck,
    accent: 'blue',
  },
  // 15. HR Staff
  {
    role: 'HR_STAFF',
    title: 'Healthcare Human Resources',
    category: 'operations',
    categoryLabel: 'Operations',
    demoStaff: 'Eleanor Davis, SPHR (HR-901)',
    department: 'Human Resources Division',
    desc: 'Staff credentialing roster, state board license tracking, Joint Commission readiness, and leave.',
    icon: Users,
    accent: 'emerald',
  },
];

export const HospitalHomePage: React.FC<HospitalHomePageProps> = ({
  onOpenLogins,
  onQuickLogin,
}) => {
  const [selectedFilter, setSelectedFilter] = useState<RoleCategory>('all');
  const [launchingRole, setLaunchingRole] = useState<HospitalRole | null>(null);

  const filteredRoleList = ALL_15_ROLES.filter((item) => {
    if (selectedFilter === 'all') return true;
    return item.category === selectedFilter;
  });

  const getAccentColorClasses = (accent: HomeRoleItem['accent']) => {
    switch (accent) {
      case 'red':
        return {
          icon: 'bg-rose-100 dark:bg-rose-950 text-rose-600 dark:text-rose-400',
          badge: 'bg-rose-50 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300 border-rose-200 dark:border-rose-800',
          btn: 'bg-rose-600 hover:bg-rose-700 text-white',
          hoverBorder: 'hover:border-rose-300 dark:hover:border-rose-700',
        };
      case 'teal':
        return {
          icon: 'bg-teal-100 dark:bg-teal-950 text-teal-600 dark:text-teal-400',
          badge: 'bg-teal-50 text-teal-700 dark:bg-teal-950/60 dark:text-teal-300 border-teal-200 dark:border-teal-800',
          btn: 'bg-teal-600 hover:bg-teal-700 text-white',
          hoverBorder: 'hover:border-teal-300 dark:hover:border-teal-700',
        };
      case 'indigo':
        return {
          icon: 'bg-indigo-100 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400',
          badge: 'bg-indigo-50 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300 border-indigo-200 dark:border-indigo-800',
          btn: 'bg-indigo-600 hover:bg-indigo-700 text-white',
          hoverBorder: 'hover:border-indigo-300 dark:hover:border-indigo-700',
        };
      case 'amber':
        return {
          icon: 'bg-amber-100 dark:bg-amber-950 text-amber-600 dark:text-amber-400',
          badge: 'bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300 border-amber-200 dark:border-amber-800',
          btn: 'bg-amber-600 hover:bg-amber-700 text-white',
          hoverBorder: 'hover:border-amber-300 dark:hover:border-amber-700',
        };
      case 'emerald':
        return {
          icon: 'bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400',
          badge: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800',
          btn: 'bg-emerald-600 hover:bg-emerald-700 text-white',
          hoverBorder: 'hover:border-emerald-300 dark:hover:border-emerald-700',
        };
      case 'slate':
        return {
          icon: 'bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300',
          badge: 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border-slate-300 dark:border-slate-700',
          btn: 'bg-slate-800 hover:bg-slate-900 text-white',
          hoverBorder: 'hover:border-slate-400 dark:hover:border-slate-600',
        };
      case 'blue':
      default:
        return {
          icon: 'bg-blue-100 dark:bg-blue-950 text-blue-600 dark:text-blue-400',
          badge: 'bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300 border-blue-200 dark:border-blue-800',
          btn: 'bg-blue-600 hover:bg-blue-700 text-white',
          hoverBorder: 'hover:border-blue-300 dark:hover:border-blue-700',
        };
    }
  };

  return (
    <div className="min-h-screen bg-[#F5F8FC] dark:bg-[#0B1120] text-[#0F172A] dark:text-[#F8FAFC] transition-colors duration-200 flex flex-col font-sans">
      {/* MAIN HEADER NAVIGATION */}
      <header className="sticky top-0 z-40 border-b border-[#DCE4EF] dark:border-[#293548] bg-white/95 dark:bg-[#111827]/95 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between gap-4">
          {/* Left: Brand Identity */}
          <div className="flex items-center gap-3.5">
            <div className="w-11 h-11 rounded-xl bg-linear-to-br from-[#1E3A8A] to-[#2563EB] flex items-center justify-center text-white shadow-xs shrink-0">
              <Building2 className="w-6 h-6" />
            </div>

            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-base sm:text-lg text-[#0F172A] dark:text-[#F8FAFC] tracking-tight">
                  CityCare Multi-Speciality Hospital
                </span>
                <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300 border border-blue-200 dark:border-blue-800/60 shrink-0">
                  Central Campus
                </span>
              </div>
              <p className="text-[11px] text-[#64748B] dark:text-[#A8B4C7] hidden sm:block">
                Advanced Healthcare System & Grounded Clinical Workstations
              </p>
            </div>
          </div>

          {/* Right: Accreditations, Theme Toggle, Main Login Button */}
          <div className="flex items-center gap-3">
            {/* Theme Toggle */}
            <ThemeToggle variant="pill" />
          </div>
        </div>
      </header>

      {/* 3. HERO / SHOWCASE SECTION WITH CREATIVE HOSPITAL IMAGE */}
      <section className="relative overflow-hidden py-10 lg:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
            {/* Left Content (Text & Call-to-Actions) */}
            <div className="lg:col-span-6 space-y-6">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-950/60 border border-blue-200 dark:border-blue-800 text-blue-700 dark:text-blue-300 text-xs font-bold">
                <Sparkles className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
                <span>Next-Generation Healthcare Intelligence</span>
              </div>

              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black text-[#0F172A] dark:text-[#F8FAFC] tracking-tight leading-[1.15]">
                Welcome to Our Hospital Management System
              </h1>

              <p className="text-sm sm:text-base text-[#64748B] dark:text-[#A8B4C7] leading-relaxed">
                Empowering doctors, nurses, administrators, and patients with integrated clinical workstations, real-time bedside telemetry, automated pharmacy dispensing, and sandboxed AI-grounded multi-RAG assistance.
              </p>

              {/* Key Trust Checkmarks */}
              <div className="grid grid-cols-2 gap-3 pt-1 text-xs">
                <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300 font-medium">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
                  <span>15 Dedicated Role Workstations</span>
                </div>
                <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300 font-medium">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
                  <span>Grounded Zero-Hallucination AI</span>
                </div>
                <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300 font-medium">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
                  <span>24/7 Level 1 Emergency & Trauma</span>
                </div>
                <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300 font-medium">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
                  <span>Kerberos Active Directory SSO</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-2 flex flex-col sm:flex-row items-stretch sm:items-center gap-3.5">

                <button
                  type="button"
                  onClick={() => setLaunchingRole('DOCTOR')}
                  className="h-13 px-5 rounded-xl font-semibold text-xs sm:text-sm border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#172033] hover:bg-slate-50 dark:hover:bg-[#1D293D] text-[#0F172A] dark:text-[#F8FAFC] transition-colors flex items-center justify-center gap-2 shadow-2xs cursor-pointer"
                >
                  <Stethoscope className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                  <span>Physician Demo Intake</span>
                </button>
              </div>

              {/* Quick Operational Metrics */}
              <div className="pt-3 border-t border-[#DCE4EF] dark:border-[#293548] grid grid-cols-4 gap-2 text-center">
                <div className="p-2 rounded-lg bg-white/60 dark:bg-[#172033]/60 border border-slate-200/60 dark:border-slate-800">
                  <div className="text-base sm:text-lg font-black text-[#0F172A] dark:text-[#F8FAFC]">520+</div>
                  <div className="text-[10px] text-slate-500 uppercase font-semibold">Beds</div>
                </div>
                <div className="p-2 rounded-lg bg-white/60 dark:bg-[#172033]/60 border border-slate-200/60 dark:border-slate-800">
                  <div className="text-base sm:text-lg font-black text-blue-600 dark:text-blue-400">15</div>
                  <div className="text-[10px] text-slate-500 uppercase font-semibold">Specialties</div>
                </div>
                <div className="p-2 rounded-lg bg-white/60 dark:bg-[#172033]/60 border border-slate-200/60 dark:border-slate-800">
                  <div className="text-base sm:text-lg font-black text-emerald-600 dark:text-emerald-400">99.8%</div>
                  <div className="text-[10px] text-slate-500 uppercase font-semibold">Grounded</div>
                </div>
                <div className="p-2 rounded-lg bg-white/60 dark:bg-[#172033]/60 border border-slate-200/60 dark:border-slate-800">
                  <div className="text-base sm:text-lg font-black text-rose-600 dark:text-rose-400">24/7</div>
                  <div className="text-[10px] text-slate-500 uppercase font-semibold">Trauma Bay</div>
                </div>
              </div>
            </div>

            {/* Right Column (Creative Image Frame with Live Overlays) */}
            <div className="lg:col-span-6">
              <div className="relative group rounded-3xl overflow-hidden border-2 border-white dark:border-[#293548] shadow-2xl bg-white dark:bg-[#172033]">
                {/* The Uploaded Hospital Image */}
                <div className="relative h-96 sm:h-[460px] w-full overflow-hidden bg-slate-200 dark:bg-slate-800">
                  <img
                    src="/images/hospital-exterior.jpg"
                    alt="CityCare Multi-Speciality Hospital Campus"
                    className="w-full h-full object-cover object-center transition-transform duration-700 group-hover:scale-105"
                  />
                  {/* Subtle gradient vignette for readability */}
                  <div className="absolute inset-0 bg-linear-to-t from-slate-950/80 via-slate-950/20 to-transparent pointer-events-none" />
                </div>

                {/* Overlay Top Badge: Campus Identification */}
                <div className="absolute top-4 left-4 z-10 flex items-center gap-2 bg-white/90 dark:bg-[#111827]/90 backdrop-blur-md px-3.5 py-1.5 rounded-full border border-white/40 dark:border-slate-700/60 shadow-md">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="text-xs font-bold text-slate-900 dark:text-white">
                    CityCare Main Pavilion • Tower A & B
                  </span>
                </div>

                {/* Overlay Top Right: Live Emergency Ready Badge */}
                <div className="absolute top-4 right-4 z-10 hidden sm:flex items-center gap-1.5 bg-rose-600/90 backdrop-blur-md text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-md">
                  <Flame className="w-3.5 h-3.5" />
                  <span>Trauma Bay Open</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. ALL 15 ROLE WORKSTATIONS SHOWCASE (TABBED & COMPLETE) */}
      <section className="py-12 bg-white dark:bg-[#111827] border-y border-[#DCE4EF] dark:border-[#293548]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-6">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
                15 Enterprise Clinical & Operational Workstations
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight mt-1">
                Direct Role Access & Dashboards
              </h2>
              <p className="text-xs sm:text-sm text-[#64748B] dark:text-[#A8B4C7] mt-1">
                Click any discipline below to immediately launch its dedicated role dashboard and sandboxed RAG assistant.
              </p>
            </div>

            <button
              type="button"
              onClick={onOpenLogins}
              className="inline-flex items-center gap-1.5 text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline cursor-pointer"
            >
              <span>View Full Access Gateway</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Category Filter Pills */}
          <div className="flex items-center gap-2 overflow-x-auto pb-3 mb-6 scrollbar-none">
            <button
              type="button"
              onClick={() => setSelectedFilter('all')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                selectedFilter === 'all'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'bg-slate-100 dark:bg-[#172033] text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              All Roles (15)
            </button>
            <button
              type="button"
              onClick={() => setSelectedFilter('clinical')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                selectedFilter === 'clinical'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'bg-slate-100 dark:bg-[#172033] text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              Clinical Care (3)
            </button>
            <button
              type="button"
              onClick={() => setSelectedFilter('diagnostics')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                selectedFilter === 'diagnostics'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'bg-slate-100 dark:bg-[#172033] text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              Diagnostics & Pharmacy (3)
            </button>
            <button
              type="button"
              onClick={() => setSelectedFilter('admin')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                selectedFilter === 'admin'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'bg-slate-100 dark:bg-[#172033] text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              Administration & Exec (4)
            </button>
            <button
              type="button"
              onClick={() => setSelectedFilter('operations')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                selectedFilter === 'operations'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'bg-slate-100 dark:bg-[#172033] text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              Operations & Billing (5)
            </button>
          </div>

          {/* Complete Grid of Filtered Role Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {filteredRoleList.map((item) => {
              const IconComponent = item.icon;
              const colorClasses = getAccentColorClasses(item.accent);

              return (
                <div 
                  key={item.role}
                  className={`p-5 rounded-2xl border border-[#DCE4EF] dark:border-[#293548] bg-[#F5F8FC] dark:bg-[#172033] ${colorClasses.hoverBorder} transition-all hover:-translate-y-1 shadow-xs flex flex-col justify-between`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${colorClasses.icon}`}>
                        <IconComponent className="w-5 h-5" />
                      </div>
                      <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-md border ${colorClasses.badge}`}>
                        {item.categoryLabel}
                      </span>
                    </div>

                    <h3 className="font-bold text-base text-[#0F172A] dark:text-[#F8FAFC]">
                      {item.title}
                    </h3>
                    <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-1 line-clamp-2">
                      {item.desc}
                    </p>

                    <div className="mt-3 p-2.5 rounded-lg bg-white/80 dark:bg-[#1D293D]/80 border border-slate-200/60 dark:border-slate-800 text-[11px]">
                      <div className="font-semibold text-slate-800 dark:text-slate-200 truncate">
                        {item.demoStaff}
                      </div>
                      <div className="text-slate-500 dark:text-slate-400 truncate mt-0.5">
                        {item.department}
                      </div>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => setLaunchingRole(item.role)}
                    className={`mt-4 w-full py-2.5 rounded-xl font-bold text-xs ${colorClasses.btn} transition-colors flex items-center justify-center gap-1.5 shadow-2xs cursor-pointer active:scale-[0.98]`}
                  >
                    <span>Launch {item.title} Dashboard</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* 5. CORE SYSTEM CAPABILITIES */}
      <section className="py-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-10">
          <span className="text-xs font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
            Enterprise Architectural Standard
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight mt-1">
            Engineered for High-Reliability Healthcare
          </h2>
          <p className="text-xs sm:text-sm text-[#64748B] dark:text-[#A8B4C7] mt-2">
            Built following strict clinical guidelines, hospital SOPs, HIPAA privacy requirements, and verifiable cryptographic audit trails.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 rounded-2xl border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#111827] shadow-xs">
            <div className="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950/60 border border-blue-200 dark:border-blue-800 flex items-center justify-center text-blue-600 dark:text-blue-400 mb-4">
              <Sparkles className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-[#0F172A] dark:text-[#F8FAFC]">
              Isolated Multi-RAG Intelligence
            </h3>
            <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-2 leading-relaxed">
              Every role has a dedicated assistant bounded strictly to authorized clinical guidelines, SOPs, and formulary docs. Anti-hallucination guardrails guarantee zero fabricated facts.
            </p>
          </div>

          <div className="p-6 rounded-2xl border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#111827] shadow-xs">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-emerald-600 dark:text-emerald-400 mb-4">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-[#0F172A] dark:text-[#F8FAFC]">
              HIPAA & Active Directory RBAC
            </h3>
            <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-2 leading-relaxed">
              Kerberos SSO directory integration, 256-bit AES transmission encryption, and granular PHI scope limits prevent unauthorized data cross-exposure.
            </p>
          </div>

          <div className="p-6 rounded-2xl border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#111827] shadow-xs">
            <div className="w-10 h-10 rounded-xl bg-purple-50 dark:bg-purple-950/60 border border-purple-200 dark:border-purple-800 flex items-center justify-center text-purple-600 dark:text-purple-400 mb-4">
              <FileText className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-[#0F172A] dark:text-[#F8FAFC]">
              Immutable SHA-256 Audit Trail
            </h3>
            <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-2 leading-relaxed">
              Every patient record consultation, prescription dispense, lab accession, and RAG query generates a cryptographically hashed compliance audit record.
            </p>
          </div>
        </div>
      </section>

      {/* 6. ENTERPRISE FOOTER */}
      <footer className="mt-auto border-t border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#111827] py-8 transition-colors">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-[#64748B] dark:text-[#A8B4C7]">
            <div className="flex items-center gap-3">
              <div className="w-7 h-7 rounded-lg bg-blue-600 text-white flex items-center justify-center font-black">
                C
              </div>
              <div>
                <span className="font-bold text-[#0F172A] dark:text-[#F8FAFC]">
                  CityCare Multi-Speciality Hospital
                </span>
                <span className="block text-[11px]">Central Inpatient Campus • Tower 1 & 2</span>
              </div>
            </div>

            <div className="flex items-center gap-4 flex-wrap justify-center text-xs">
              <button
                type="button"
                onClick={onOpenLogins}
                className="text-blue-600 dark:text-blue-400 font-bold hover:underline cursor-pointer"
              >
                Enter Logins Gateway →
              </button>
              <span>•</span>
              <span>Code Blue: Ext. 4444</span>
              <span>•</span>
              <span>FedRAMP High Ready</span>
              <span>•</span>
              <span>Joint Commission Certified</span>
            </div>
          </div>
        </div>
      </footer>

      {/* Workstation Access Credentials Modal */}
      <WorkstationLaunchModal
        role={launchingRole}
        isOpen={!!launchingRole}
        onComplete={(role) => {
          setLaunchingRole(null);
          onQuickLogin(role);
        }}
        onCancel={() => setLaunchingRole(null)}
      />
    </div>
  );
};
