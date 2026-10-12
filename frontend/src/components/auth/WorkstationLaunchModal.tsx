'use client';

import React, { useState, useEffect, useRef } from 'react';
import { HospitalRole } from '@/lib/types/roles';
import { ROLE_CONFIGS } from '@/lib/data/roleConfigs';
import { DEMO_USERS } from '@/lib/data/mockDatabase';
import { Eye, EyeOff, X, Loader2 } from 'lucide-react';

export const ROLE_CREDENTIALS: Record<HospitalRole, {
  email: string;
  defaultPassword: string;
}> = {
  SUPER_ADMIN: {
    email: 'superadmin@hopkins-health.org',
    defaultPassword: 'ClusterRoot#2024',
  },
  HOSPITAL_ADMIN: {
    email: 'admin@hopkins-health.org',
    defaultPassword: 'AdminHospital#2024',
  },
  DOCTOR: {
    email: 'marcus.vance@hopkins-health.org',
    defaultPassword: 'DocCardio#2024',
  },
  NURSE: {
    email: 'sarah.jenkins@hopkins-health.org',
    defaultPassword: 'NurseCare#2024',
  },
  EMERGENCY_STAFF: {
    email: 'robert.thorne@hopkins-health.org',
    defaultPassword: 'TraumaBay#2024',
  },
  PHARMACIST: {
    email: 'samuel.miller@hopkins-health.org',
    defaultPassword: 'RxFormulary#2024',
  },
  LABORATORY_STAFF: {
    email: 'david.chen@hopkins-health.org',
    defaultPassword: 'LISPathology#2024',
  },
  RADIOLOGY_STAFF: {
    email: 'jonathan.blake@hopkins-health.org',
    defaultPassword: 'PACSImaging#2024',
  },
  PATIENT: {
    email: 'john.anderson@patient.org',
    defaultPassword: 'Patient#2024',
  },
  RECEPTIONIST: {
    email: 'reception@hopkins-health.org',
    defaultPassword: 'FrontDesk#2024',
  },
  BILLING_STAFF: {
    email: 'claire.h@hopkins-health.org',
    defaultPassword: 'RevenueCycle#2024',
  },
  INSURANCE_STAFF: {
    email: 'michael.chang@hopkins-health.org',
    defaultPassword: 'ClaimsAdjudicate#2024',
  },
  HR_STAFF: {
    email: 'eleanor.davis@hopkins-health.org',
    defaultPassword: 'StaffCredential#2024',
  },
  DEPARTMENT_MANAGER: {
    email: 'gregory.house@hopkins-health.org',
    defaultPassword: 'DeptManager#2024',
  },
  MANAGEMENT_EXECUTIVE: {
    email: 'victoria.hastings@hopkins-health.org',
    defaultPassword: 'ExecutiveBoard#2024',
  },
};

interface WorkstationLaunchModalProps {
  role: HospitalRole | null;
  isOpen: boolean;
  onComplete: (role: HospitalRole) => void;
  onCancel: () => void;
}

export const WorkstationLaunchModal: React.FC<WorkstationLaunchModalProps> = ({
  role,
  isOpen,
  onComplete,
  onCancel,
}) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isAuthenticating, setIsAuthenticating] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;

  const currentRole = role || 'DOCTOR';
  const roleConfig = ROLE_CONFIGS[currentRole];

  // Set default credentials whenever modal opens for a role
  useEffect(() => {
    if (isOpen && role) {
      const creds = ROLE_CREDENTIALS[role] || ROLE_CREDENTIALS['DOCTOR'];
      setUsername(creds.email);
      setPassword(creds.defaultPassword);
      setShowPassword(false);
      setIsAuthenticating(false);
      setErrorMsg(null);
    }
  }, [isOpen, role]);

  if (!isOpen || !role) return null;

  const handleLogin = () => {
    if (!username.trim() || !password.trim()) {
      setErrorMsg('Please enter User ID and Password.');
      return;
    }

    setErrorMsg(null);
    setIsAuthenticating(true);

    setTimeout(() => {
      setIsAuthenticating(false);
      onCompleteRef.current(role);
    }, 200);
  };

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 dark:bg-black/75 backdrop-blur-xs transition-opacity animate-in fade-in duration-150"
      role="dialog"
      aria-modal="true"
      aria-labelledby="login-modal-title"
    >
      <div className="relative w-full max-w-md bg-white dark:bg-[#111827] border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl p-6 sm:p-7 animate-in zoom-in-95 duration-150">
        {/* Heading */}
        <div className="flex items-center justify-between mb-6">
          <h3 id="login-modal-title" className="text-xl font-bold text-slate-900 dark:text-white">
            {roleConfig?.displayName || 'Workstation'} Login
          </h3>

          <button
            type="button"
            onClick={onCancel}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            title="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Login Form: Only User ID & Password */}
        <form 
          onSubmit={(e) => {
            e.preventDefault();
            handleLogin();
          }}
          className="space-y-4"
        >
          {/* User ID */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
              User ID
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter User ID"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#1A2436] text-slate-900 dark:text-white text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
              disabled={isAuthenticating}
              autoFocus
            />
          </div>

          {/* Password */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter Password"
                className="w-full pl-3.5 pr-10 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#1A2436] text-slate-900 dark:text-white text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                disabled={isAuthenticating}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                title={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {errorMsg && (
            <div className="p-2.5 rounded-lg bg-rose-50 dark:bg-rose-950/60 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 text-xs">
              {errorMsg}
            </div>
          )}

          {/* Buttons: Solid Blue Login & Cancel */}
          <div className="pt-2 flex items-center gap-3">
            <button
              type="submit"
              disabled={isAuthenticating}
              className="flex-1 h-11 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white font-bold text-sm rounded-xl shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-75"
            >
              {isAuthenticating ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-white" />
                  <span>Logging in...</span>
                </>
              ) : (
                <span>Login</span>
              )}
            </button>

            <button
              type="button"
              onClick={onCancel}
              disabled={isAuthenticating}
              className="h-11 px-5 rounded-xl font-semibold text-sm text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-300 dark:border-slate-700 transition-colors cursor-pointer"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
