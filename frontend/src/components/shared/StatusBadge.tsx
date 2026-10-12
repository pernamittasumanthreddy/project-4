'use client';
import React from 'react';
import { CheckCircle2, AlertTriangle, AlertCircle, Info, Clock, ShieldCheck, XCircle } from 'lucide-react';

export type StatusVariant = 'success' | 'warning' | 'critical' | 'info' | 'neutral' | 'emergency';

interface StatusBadgeProps {
  status: string;
  variant?: StatusVariant;
  size?: 'sm' | 'md';
  showIcon?: boolean;
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  variant,
  size = 'sm',
  showIcon = true,
  className = '',
}) => {
  // Infer variant if not explicitly provided
  const inferVariant = (txt: string): StatusVariant => {
    const lower = txt.toLowerCase();
    if (lower.includes('critical') || lower.includes('emergency') || lower.includes('code blue') || lower.includes('panic') || lower.includes('failed') || lower.includes('rejected') || lower.includes('out of stock')) {
      return 'critical';
    }
    if (lower.includes('warning') || lower.includes('pending') || lower.includes('waiting') || lower.includes('attention') || lower.includes('near') || lower.includes('expir') || lower.includes('deficit')) {
      return 'warning';
    }
    if (lower.includes('completed') || lower.includes('stable') || lower.includes('active') || lower.includes('approved') || lower.includes('optimal') || lower.includes('verified') || lower.includes('passed') || lower.includes('normal') || lower.includes('operational')) {
      return 'success';
    }
    if (lower.includes('scheduled') || lower.includes('in progress') || lower.includes('review') || lower.includes('info') || lower.includes('processing')) {
      return 'info';
    }
    return 'neutral';
  };

  const currentVariant = variant || inferVariant(status);

  const VARIANT_CONFIG: Record<StatusVariant, { bg: string; text: string; border: string; icon: any }> = {
    success: {
      bg: 'bg-emerald-50',
      text: 'text-emerald-700',
      border: 'border-emerald-200',
      icon: CheckCircle2,
    },
    warning: {
      bg: 'bg-amber-50',
      text: 'text-amber-700',
      border: 'border-amber-200',
      icon: AlertTriangle,
    },
    critical: {
      bg: 'bg-rose-50',
      text: 'text-rose-700',
      border: 'border-rose-200',
      icon: AlertCircle,
    },
    emergency: {
      bg: 'bg-red-600 text-white',
      text: 'text-white font-bold',
      border: 'border-red-700',
      icon: AlertCircle,
    },
    info: {
      bg: 'bg-blue-50',
      text: 'text-blue-700',
      border: 'border-blue-200',
      icon: Info,
    },
    neutral: {
      bg: 'bg-slate-100',
      text: 'text-slate-700',
      border: 'border-slate-200',
      icon: Clock,
    },
  };

  const config = VARIANT_CONFIG[currentVariant];
  const Icon = config.icon;

  const sizeClasses = size === 'sm' ? 'px-2 py-0.5 text-[11px]' : 'px-2.5 py-1 text-xs';
  const iconSize = size === 'sm' ? 'w-3 h-3' : 'w-3.5 h-3.5';

  return (
    <span
      className={`inline-flex items-center gap-1 font-semibold rounded-md border ${config.bg} ${config.text} ${config.border} ${sizeClasses} ${className}`}
    >
      {showIcon && <Icon className={`${iconSize} shrink-0`} />}
      <span>{status}</span>
    </span>
  );
};
