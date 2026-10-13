'use client';
import React from 'react';

interface PageHeaderProps {
  badge?: React.ReactNode;
  department?: string;
  title: string;
  description?: string;
  actions?: React.ReactNode;
  navTabs?: {
    id: string;
    label: string;
    count?: number;
  }[];
  activeTab?: string;
  onTabChange?: (tabId: string) => void;
}

export const PageHeader: React.FC<PageHeaderProps> = ({
  badge,
  department,
  title,
  description,
  actions,
  navTabs,
  activeTab,
  onTabChange,
}) => {
  return (
    <div className="bg-white dark:bg-[#111827] rounded-xl p-5 border border-[#DCE4EA] dark:border-[#293548] shadow-2xs space-y-3">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            {badge}
            {department && (
              <span className="text-xs text-slate-500 font-medium">
                {department}
              </span>
            )}
          </div>
          <h1 className="text-xl font-bold mt-1 text-[#1E293B] dark:text-white tracking-tight">
            {title}
          </h1>
          {description && (
            <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-0.5 leading-relaxed">
              {description}
            </p>
          )}
        </div>

        {actions && (
          <div className="flex items-center gap-2 shrink-0">
            {actions}
          </div>
        )}
      </div>

      {navTabs && navTabs.length > 0 && (
        <div className="pt-2 border-t border-slate-100 dark:border-slate-800 flex items-center gap-1 overflow-x-auto scrollbar-none">
          {navTabs.map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => onTabChange?.(tab.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold capitalize transition-all flex items-center gap-1.5 cursor-pointer ${
                  isActive
                    ? 'bg-[#0F8B8D] text-white shadow-xs'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-[#172033]'
                }`}
              >
                <span>{tab.label}</span>
                {tab.count !== undefined && (
                  <span className={`text-[10px] px-1.5 py-0.2 rounded-full font-mono ${
                    isActive ? 'bg-white/25 text-white' : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300'
                  }`}>
                    {tab.count}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};
