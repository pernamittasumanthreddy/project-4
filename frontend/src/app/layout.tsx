import './globals.css';
import type { Metadata } from 'next';
import { ThemeProvider } from '@/components/theme/ThemeProvider';

export const metadata: Metadata = {
  title: 'CityCare Multi-Speciality Hospital | Enterprise Access Gateway & Clinical Workstations',
  description: 'Enterprise healthcare identity gateway and role-isolated Multi-RAG clinical workstations for CityCare Multi-Speciality Hospital Central Campus.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="bg-[#F5F8FC] dark:bg-[#0B1120] text-[#0F172A] dark:text-[#F8FAFC] min-h-screen antialiased selection:bg-blue-500 selection:text-white">
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
