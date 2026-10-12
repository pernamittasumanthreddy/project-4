'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useTheme } from './ThemeProvider';
import { Sun, Moon, Laptop, ChevronDown, Check } from 'lucide-react';

interface ThemeToggleProps {
  variant?: 'pill' | 'dropdown' | 'compact';
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({ variant = 'pill' }) => {
  const { theme, resolvedTheme, setTheme } = useTheme();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (variant === 'pill') {
    return (
      <div 
        className="inline-flex items-center p-0.5 rounded-lg border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#172033] shadow-xs text-xs font-medium"
        role="radiogroup"
        aria-label="Theme mode switcher"
      >
        <button
          type="button"
          onClick={() => setTheme('light')}
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-all ${
            theme === 'light'
              ? 'bg-[#2563EB] text-white shadow-xs font-semibold'
              : 'text-[#64748B] dark:text-[#A8B4C7] hover:text-[#0F172A] dark:hover:text-white hover:bg-slate-100 dark:hover:bg-[#1D293D]'
          }`}
          title="Light theme"
          aria-checked={theme === 'light'}
          role="radio"
        >
          <Sun className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Light</span>
        </button>

        <button
          type="button"
          onClick={() => setTheme('dark')}
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-all ${
            theme === 'dark'
              ? 'bg-[#2563EB] text-white shadow-xs font-semibold'
              : 'text-[#64748B] dark:text-[#A8B4C7] hover:text-[#0F172A] dark:hover:text-white hover:bg-slate-100 dark:hover:bg-[#1D293D]'
          }`}
          title="Dark theme"
          aria-checked={theme === 'dark'}
          role="radio"
        >
          <Moon className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Dark</span>
        </button>

        <button
          type="button"
          onClick={() => setTheme('system')}
          className={`flex items-center gap-1.5 px-2 py-1 rounded-md transition-all ${
            theme === 'system'
              ? 'bg-[#2563EB] text-white shadow-xs font-semibold'
              : 'text-[#64748B] dark:text-[#A8B4C7] hover:text-[#0F172A] dark:hover:text-white hover:bg-slate-100 dark:hover:bg-[#1D293D]'
          }`}
          title="System theme"
          aria-checked={theme === 'system'}
          role="radio"
        >
          <Laptop className="w-3.5 h-3.5" />
          <span className="hidden md:inline">System</span>
        </button>
      </div>
    );
  }

  // Dropdown variant for tighter topbars
  return (
    <div className="relative" ref={dropdownRef}>
      <button
        type="button"
        onClick={() => setDropdownOpen(!dropdownOpen)}
        className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#172033] hover:bg-slate-50 dark:hover:bg-[#1D293D] text-[#0F172A] dark:text-[#F8FAFC] text-xs font-medium transition-colors shadow-xs"
        aria-label="Select theme"
      >
        {theme === 'light' && <Sun className="w-3.5 h-3.5 text-amber-500" />}
        {theme === 'dark' && <Moon className="w-3.5 h-3.5 text-blue-400" />}
        {theme === 'system' && <Laptop className="w-3.5 h-3.5 text-slate-400" />}
        <span className="capitalize hidden sm:inline">{theme}</span>
        <ChevronDown className="w-3 h-3 text-slate-400" />
      </button>

      {dropdownOpen && (
        <div className="absolute right-0 mt-1.5 w-36 rounded-lg border border-[#DCE4EF] dark:border-[#293548] bg-white dark:bg-[#172033] shadow-lg py-1 z-50 animate-in fade-in zoom-in-95 duration-100">
          <button
            type="button"
            onClick={() => { setTheme('light'); setDropdownOpen(false); }}
            className={`w-full flex items-center justify-between px-3 py-1.5 text-xs text-left ${
              theme === 'light' 
                ? 'bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 font-semibold' 
                : 'text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-[#1D293D]'
            }`}
          >
            <span className="flex items-center gap-2">
              <Sun className="w-3.5 h-3.5 text-amber-500" /> Light
            </span>
            {theme === 'light' && <Check className="w-3.5 h-3.5" />}
          </button>

          <button
            type="button"
            onClick={() => { setTheme('dark'); setDropdownOpen(false); }}
            className={`w-full flex items-center justify-between px-3 py-1.5 text-xs text-left ${
              theme === 'dark' 
                ? 'bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 font-semibold' 
                : 'text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-[#1D293D]'
            }`}
          >
            <span className="flex items-center gap-2">
              <Moon className="w-3.5 h-3.5 text-blue-400" /> Dark
            </span>
            {theme === 'dark' && <Check className="w-3.5 h-3.5" />}
          </button>

          <button
            type="button"
            onClick={() => { setTheme('system'); setDropdownOpen(false); }}
            className={`w-full flex items-center justify-between px-3 py-1.5 text-xs text-left ${
              theme === 'system' 
                ? 'bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 font-semibold' 
                : 'text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-[#1D293D]'
            }`}
          >
            <span className="flex items-center gap-2">
              <Laptop className="w-3.5 h-3.5 text-slate-400" /> System
            </span>
            {theme === 'system' && <Check className="w-3.5 h-3.5" />}
          </button>
        </div>
      )}
    </div>
  );
};
