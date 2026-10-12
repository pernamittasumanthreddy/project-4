'use client';

import React, { useRef, useEffect } from 'react';
import { Bell, ShieldCheck, CheckCircle2, AlertTriangle, Info, Clock, X } from 'lucide-react';

interface GatewayNotificationPopoverProps {
  isOpen: boolean;
  onClose: () => void;
}

const GATEWAY_NOTIFICATIONS = [
  {
    id: 'NOTIF-GW-1',
    type: 'security',
    title: 'Active Directory Kerberos Sync Complete',
    detail: 'All 15 RBAC roles and organizational units re-synchronized with Central Campus LDAP.',
    time: '4 mins ago',
    read: false,
  },
  {
    id: 'NOTIF-GW-2',
    type: 'compliance',
    title: 'Quarterly HIPAA Audit Baseline Verified',
    detail: 'SHA-256 cryptographic audit logs verified across emergency, inpatient, and pharmacy partitions.',
    time: '28 mins ago',
    read: false,
  },
  {
    id: 'NOTIF-GW-3',
    type: 'system',
    title: 'Formulary Knowledge Base v4.6 Deployed',
    detail: 'Updated drug storage protocols and antibiotic stewardship guidelines loaded into isolated vectors.',
    time: '2 hours ago',
    read: true,
  },
];

export const GatewayNotificationPopover: React.FC<GatewayNotificationPopoverProps> = ({
  isOpen,
  onClose,
}) => {
  const popoverRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (popoverRef.current && !popoverRef.current.contains(event.target as Node)) {
        onClose();
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      ref={popoverRef}
      className="absolute right-0 top-full mt-2 w-80 sm:w-96 rounded-xl border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#111827] shadow-xl z-50 overflow-hidden animate-in fade-in zoom-in-95 duration-150"
    >
      <div className="flex items-center justify-between p-3.5 border-b border-[#DCE4EF] dark:border-[#293548] bg-slate-50/70 dark:bg-[#172033]/70">
        <div className="flex items-center gap-2">
          <Bell className="w-4 h-4 text-blue-600 dark:text-blue-400" />
          <span className="text-xs font-bold text-[#0F172A] dark:text-[#F8FAFC]">
            Enterprise Gateway Advisories
          </span>
        </div>
        <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300">
          2 New
        </span>
      </div>

      <div className="divide-y divide-slate-100 dark:divide-slate-800 max-h-80 overflow-y-auto">
        {GATEWAY_NOTIFICATIONS.map((n) => (
          <div 
            key={n.id} 
            className={`p-3 text-xs transition-colors hover:bg-slate-50/80 dark:hover:bg-[#172033]/60 ${
              !n.read ? 'bg-blue-50/20 dark:bg-blue-950/20' : ''
            }`}
          >
            <div className="flex items-start gap-2.5">
              <div className="mt-0.5 shrink-0">
                {n.type === 'security' && <ShieldCheck className="w-4 h-4 text-emerald-500" />}
                {n.type === 'compliance' && <CheckCircle2 className="w-4 h-4 text-blue-500" />}
                {n.type === 'system' && <Info className="w-4 h-4 text-slate-400" />}
              </div>
              <div className="flex-1 min-w-0">
                <div className="font-semibold text-slate-800 dark:text-slate-200">
                  {n.title}
                </div>
                <div className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 leading-relaxed">
                  {n.detail}
                </div>
                <div className="flex items-center gap-1 text-[10px] text-slate-400 dark:text-slate-500 mt-1.5 font-mono">
                  <Clock className="w-3 h-3" /> {n.time}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="p-2 border-t border-[#DCE4EF] dark:border-[#293548] bg-slate-50/50 dark:bg-[#172033]/50 text-center">
        <button
          type="button"
          onClick={onClose}
          className="text-[11px] font-semibold text-blue-600 dark:text-blue-400 hover:underline"
        >
          Dismiss All Advisories
        </button>
      </div>
    </div>
  );
};
