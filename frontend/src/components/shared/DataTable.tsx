'use client';
import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, Search, ArrowUpDown } from 'lucide-react';

export interface Column<T> {
  header: string;
  accessorKey?: keyof T;
  cell?: (item: T) => React.ReactNode;
  sortable?: boolean;
  className?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  pageSize?: number;
  searchable?: boolean;
  searchPlaceholder?: string;
  filterFn?: (item: T, query: string) => boolean;
  onRowClick?: (item: T) => void;
  emptyMessage?: string;
}

export function DataTable<T extends { id?: string | number }>({
  columns,
  data,
  pageSize = 10,
  searchable = true,
  searchPlaceholder = 'Search records...',
  filterFn,
  onRowClick,
  emptyMessage = 'No records found matching the query.',
}: DataTableProps<T>) {
  const [query, setQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [sortKey, setSortKey] = useState<keyof T | null>(null);
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  // Filter
  const filteredData = React.useMemo(() => {
    if (!query.trim()) return data;
    if (filterFn) return data.filter(item => filterFn(item, query));
    return data.filter(item => {
      return Object.values(item as Record<string, any>).some(val =>
        String(val).toLowerCase().includes(query.toLowerCase())
      );
    });
  }, [data, query, filterFn]);

  // Sort
  const sortedData = React.useMemo(() => {
    if (!sortKey) return filteredData;
    return [...filteredData].sort((a, b) => {
      const aVal = a[sortKey];
      const bVal = b[sortKey];
      if (aVal === bVal) return 0;
      if (aVal === null || aVal === undefined) return 1;
      if (bVal === null || bVal === undefined) return -1;
      if (aVal < bVal) return sortOrder === 'asc' ? -1 : 1;
      return sortOrder === 'asc' ? 1 : -1;
    });
  }, [filteredData, sortKey, sortOrder]);

  // Paginate
  const totalPages = Math.ceil(sortedData.length / pageSize) || 1;
  const paginatedData = sortedData.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  const handleSort = (key?: keyof T) => {
    if (!key) return;
    if (sortKey === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortOrder('asc');
    }
  };

  return (
    <div className="bg-white dark:bg-[#111827] rounded-xl border border-[#DCE4EA] dark:border-[#293548] overflow-hidden shadow-2xs">
      {searchable && (
        <div className="p-3.5 border-b border-[#DCE4EA] dark:border-[#293548] flex items-center justify-between gap-3 bg-[#F4F7FA]/50 dark:bg-[#172033]/50">
          <div className="relative flex-1 max-w-sm">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              value={query}
              onChange={(e) => {
                setQuery(e.target.value);
                setCurrentPage(1);
              }}
              placeholder={searchPlaceholder}
              className="w-full pl-8.5 pr-3 py-1.5 rounded-lg border border-[#DCE4EA] dark:border-[#293548] bg-white dark:bg-[#0F172A] text-xs text-[#1E293B] dark:text-white placeholder-slate-400 focus:outline-hidden focus:ring-1 focus:ring-[#0F8B8D] focus:border-[#0F8B8D]"
            />
          </div>
          <div className="text-[11px] text-slate-500 font-medium">
            Showing <strong className="text-[#1E293B] dark:text-white">{sortedData.length}</strong> records
          </div>
        </div>
      )}

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-[#DCE4EA] dark:border-[#293548] bg-[#F4F7FA] dark:bg-[#172033] text-slate-600 dark:text-slate-300 uppercase text-[10px] tracking-wider font-semibold">
              {columns.map((col, idx) => (
                <th
                  key={idx}
                  onClick={() => col.sortable && col.accessorKey && handleSort(col.accessorKey)}
                  className={`p-3.5 ${col.sortable ? 'cursor-pointer select-none hover:text-[#0F8B8D]' : ''} ${col.className || ''}`}
                >
                  <div className="flex items-center gap-1.5">
                    <span>{col.header}</span>
                    {col.sortable && <ArrowUpDown className="w-3 h-3 text-slate-400" />}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-[#DCE4EA] dark:divide-[#293548]">
            {paginatedData.length > 0 ? (
              paginatedData.map((item, rowIdx) => (
                <tr
                  key={item.id || rowIdx}
                  onClick={() => onRowClick?.(item)}
                  className={`transition-colors hover:bg-slate-50 dark:hover:bg-[#1A2436] ${
                    onRowClick ? 'cursor-pointer' : ''
                  }`}
                >
                  {columns.map((col, colIdx) => (
                    <td key={colIdx} className={`p-3.5 text-[#1E293B] dark:text-slate-200 ${col.className || ''}`}>
                      {col.cell
                        ? col.cell(item)
                        : col.accessorKey
                        ? String(item[col.accessorKey] ?? '-')
                        : null}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={columns.length} className="p-8 text-center text-slate-400 text-xs">
                  {emptyMessage}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="p-3 border-t border-[#DCE4EA] dark:border-[#293548] bg-[#F4F7FA]/30 dark:bg-[#172033]/30 flex items-center justify-between text-xs text-slate-500">
          <span>
            Page <strong className="text-[#1E293B] dark:text-white">{currentPage}</strong> of <strong>{totalPages}</strong>
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setCurrentPage(p => Math.max(p - 1, 1))}
              disabled={currentPage === 1}
              className="p-1 rounded-md border border-[#DCE4EA] dark:border-[#293548] hover:bg-white dark:hover:bg-[#0F172A] disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setCurrentPage(p => Math.min(p + 1, totalPages))}
              disabled={currentPage === totalPages}
              className="p-1 rounded-md border border-[#DCE4EA] dark:border-[#293548] hover:bg-white dark:hover:bg-[#0F172A] disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
