'use strict';
import React from 'react';
import { HospitalRole } from '@/lib/types/roles';

interface RoleBadgeProps {
  role: HospitalRole;
  size?: 'sm' | 'md' | 'lg';
}

const ROLE_STYLES: Record<HospitalRole, { label: string; bg: string; text: string; border: string }> = {
  SUPER_ADMIN: { label: 'Super Admin', bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-200' },
  HOSPITAL_ADMIN: { label: 'Hospital Admin', bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
  DOCTOR: { label: 'Physician / MD', bg: 'bg-sky-50', text: 'text-sky-700', border: 'border-sky-200' },
  NURSE: { label: 'Registered Nurse', bg: 'bg-teal-50', text: 'text-teal-700', border: 'border-teal-200' },
  RECEPTIONIST: { label: 'Front Desk', bg: 'bg-indigo-50', text: 'text-indigo-700', border: 'border-indigo-200' },
  PATIENT: { label: 'Patient Portal', bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200' },
  PHARMACIST: { label: 'Pharmacist', bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
  LABORATORY_STAFF: { label: 'Lab Technologist', bg: 'bg-cyan-50', text: 'text-cyan-700', border: 'border-cyan-200' },
  RADIOLOGY_STAFF: { label: 'Radiology Tech', bg: 'bg-violet-50', text: 'text-violet-700', border: 'border-violet-200' },
  BILLING_STAFF: { label: 'Billing Specialist', bg: 'bg-emerald-50', text: 'text-emerald-800', border: 'border-emerald-200' },
  INSURANCE_STAFF: { label: 'Insurance Coordinator', bg: 'bg-blue-50', text: 'text-blue-800', border: 'border-blue-300' },
  HR_STAFF: { label: 'HR Officer', bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-200' },
  DEPARTMENT_MANAGER: { label: 'Dept Manager', bg: 'bg-slate-100', text: 'text-slate-800', border: 'border-slate-300' },
  MANAGEMENT_EXECUTIVE: { label: 'Executive Board', bg: 'bg-zinc-800', text: 'text-amber-300', border: 'border-zinc-700' },
  EMERGENCY_STAFF: { label: 'Emergency Trauma', bg: 'bg-red-50', text: 'text-red-700', border: 'border-red-200' },
};

export const RoleBadge: React.FC<RoleBadgeProps> = ({ role, size = 'md' }) => {
  const style = ROLE_STYLES[role] || { label: role, bg: 'bg-gray-50', text: 'text-gray-700', border: 'border-gray-200' };
  
  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-xs px-2.5 py-1 font-medium',
    lg: 'text-sm px-3 py-1.5 font-semibold'
  }[size];

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-md border ${style.bg} ${style.text} ${style.border} ${sizeClasses}`}>
      <span className="w-1.5 h-1.5 rounded-full bg-current opacity-80" />
      {style.label}
    </span>
  );
};
