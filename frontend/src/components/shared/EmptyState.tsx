'use client';
import React from 'react';
import { LucideIcon, Inbox } from 'lucide-react';

interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  description: string;
  actionText?: string;
  onAction?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon: Icon = Inbox,
  title,
  description,
  actionText,
  onAction,
}) => {
  return (
    <div className="bg-white dark:bg-[#111827] rounded-xl border border-[#DCE4EA] dark:border-[#293548] p-8 sm:p-12 text-center max-w-md mx-auto my-6">
      <div className="w-12 h-12 rounded-xl bg-slate-100 dark:bg-[#172033] flex items-center justify-center mx-auto mb-3.5 text-slate-400">
        <Icon className="w-6 h-6" />
      </div>
      <h3 className="text-base font-bold text-[#1E293B] dark:text-white">
        {title}
      </h3>
      <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-1.5 leading-relaxed">
        {description}
      </p>
      {actionText && onAction && (
        <button
          type="button"
          onClick={onAction}
          className="mt-4 px-4 py-2 rounded-lg bg-[#0F8B8D] hover:bg-[#0B7476] text-white text-xs font-semibold shadow-xs transition-colors cursor-pointer"
        >
          {actionText}
        </button>
      )}
    </div>
  );
};
