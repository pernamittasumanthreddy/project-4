'use client';
import React, { useState } from 'react';
import { 
  Bell, X, Check, AlertCircle, Calendar, 
  CreditCard, ShieldAlert, Activity, CheckCheck 
} from 'lucide-react';
import { NotificationItem } from '@/lib/types/hms';

interface NotificationCenterProps {
  notifications: NotificationItem[];
  isOpen: boolean;
  onClose: () => void;
  onSelectAction?: (notif: NotificationItem) => void;
}

export const NotificationCenter: React.FC<NotificationCenterProps> = ({
  notifications: initialNotifications,
  isOpen,
  onClose,
  onSelectAction,
}) => {
  const [notifications, setNotifications] = useState<NotificationItem[]>(initialNotifications);
  const [activeCategory, setActiveCategory] = useState<'All' | 'Clinical' | 'Emergency' | 'Billing' | 'System'>('All');

  if (!isOpen) return null;

  const handleMarkAllRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
  };

  const handleDismiss = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const filteredNotifs = notifications.filter(n => {
    if (activeCategory === 'All') return true;
    if (activeCategory === 'Clinical') return n.type === 'LAB_RESULT' || n.type === 'APPOINTMENT' || n.title.toLowerCase().includes('lab') || n.title.toLowerCase().includes('patient');
    if (activeCategory === 'Emergency') return n.type === 'CRITICAL_ALERT' || n.severity === 'urgent' || n.title.toLowerCase().includes('trauma') || n.title.toLowerCase().includes('code');
    if (activeCategory === 'Billing') return n.type === 'INSURANCE_CLAIM' || n.title.toLowerCase().includes('claim') || n.title.toLowerCase().includes('invoice');
    if (activeCategory === 'System') return n.type === 'POLICY_UPDATE' || n.type === 'MED_RESTOCK' || n.title.toLowerCase().includes('security') || n.title.toLowerCase().includes('login');
    return true;
  });

  return (
    <div className="absolute right-0 mt-2 w-88 sm:w-96 bg-white border border-slate-200 rounded-xl shadow-xl z-50 text-xs overflow-hidden animate-in fade-in duration-100 text-slate-800">
      {/* Header */}
      <div className="p-3.5 bg-slate-900 text-white flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Bell className="w-4 h-4 text-blue-400" />
          <h3 className="font-bold text-xs">Hospital Alert Center</h3>
          <span className="px-1.5 py-0.2 rounded bg-blue-600 text-white font-mono text-[10px] font-bold">
            {notifications.filter(n => !n.read).length} new
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleMarkAllRead}
            className="text-[11px] text-slate-300 hover:text-white flex items-center gap-1 transition-colors"
            title="Mark all as read"
          >
            <CheckCheck className="w-3.5 h-3.5" /> Mark all read
          </button>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-white rounded">
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Category Filter Tabs */}
      <div className="bg-slate-50 border-b border-slate-200 px-3 py-1.5 flex gap-1 overflow-x-auto scrollbar-none text-[11px] font-semibold">
        {(['All', 'Clinical', 'Emergency', 'Billing', 'System'] as const).map(cat => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-2.5 py-1 rounded-md transition-colors ${
              activeCategory === cat
                ? 'bg-blue-600 text-white'
                : 'text-slate-600 hover:bg-slate-200/60'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Notification List */}
      <div className="max-h-80 overflow-y-auto divide-y divide-slate-100 p-1">
        {filteredNotifs.length === 0 ? (
          <div className="p-6 text-center text-slate-400">
            <Bell className="w-6 h-6 mx-auto mb-1 opacity-40" />
            <p className="font-semibold text-slate-600">No active alerts in this category</p>
          </div>
        ) : (
          filteredNotifs.map(n => {
            const isUrgent = n.severity === 'urgent' || n.type === 'CRITICAL_ALERT';
            return (
              <div
                key={n.id}
                className={`p-3 hover:bg-slate-50 transition-colors flex items-start justify-between gap-2.5 ${
                  !n.read ? 'bg-blue-50/40' : ''
                }`}
              >
                <div className="space-y-0.5">
                  <div className="flex items-center gap-1.5">
                    {isUrgent && <AlertCircle className="w-3.5 h-3.5 text-rose-600 shrink-0" />}
                    <strong className={`text-xs ${isUrgent ? 'text-rose-900 font-bold' : 'text-slate-900'}`}>
                      {n.title}
                    </strong>
                    {!n.read && (
                      <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0" />
                    )}
                  </div>
                  <p className="text-[11px] text-slate-600 leading-snug">{n.message}</p>
                  <span className="text-[10px] text-slate-400 font-mono block pt-0.5">{n.timestamp}</span>
                </div>

                <button
                  onClick={() => handleDismiss(n.id)}
                  className="p-1 text-slate-400 hover:text-slate-700 rounded shrink-0"
                  title="Dismiss alert"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
            );
          })
        )}
      </div>

      {/* Footer */}
      <div className="p-2.5 bg-slate-50 border-t border-slate-200 text-center text-[11px] text-slate-500 font-medium">
        Hospital Alert Dispatch • Automated LIS, CPOE & Security Hooks
      </div>
    </div>
  );
};
