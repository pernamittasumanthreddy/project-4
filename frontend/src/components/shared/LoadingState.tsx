'use client';
import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingStateProps {
  message?: string;
  submessage?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  message = 'Loading Clinical Data...',
  submessage = 'Connecting to hospital FHIR repository & PACS telemetry',
}) => {
  return (
    <div className="bg-white dark:bg-[#111827] rounded-xl border border-[#DCE4EA] dark:border-[#293548] p-12 text-center my-6">
      <div className="w-10 h-10 rounded-full bg-teal-50 dark:bg-teal-950/50 flex items-center justify-center mx-auto mb-3 text-[#0F8B8D]">
        <Loader2 className="w-5 h-5 animate-spin" />
      </div>
      <h3 className="text-sm font-bold text-[#1E293B] dark:text-white">
        {message}
      </h3>
      {submessage && (
        <p className="text-xs text-[#64748B] dark:text-[#A8B4C7] mt-1 font-mono">
          {submessage}
        </p>
      )}
    </div>
  );
};
