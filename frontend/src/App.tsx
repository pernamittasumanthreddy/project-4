import React from 'react';
import { ThemeProvider } from './components/theme/ThemeProvider';
import { HospitalShell } from './components/layout/HospitalShell';

export const App: React.FC = () => {
  return (
    <ThemeProvider>
      <HospitalShell />
    </ThemeProvider>
  );
};

export default App;
