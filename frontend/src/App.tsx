import React from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { PatientDashboard } from './pages/patient/PatientDashboard';
import { PatientAppointments } from './pages/patient/PatientAppointments';
import { PatientMedicalRecords } from './pages/patient/PatientMedicalRecords';
import { PatientBilling } from './pages/patient/PatientBilling';
import { PatientProfileSettings } from './pages/patient/PatientProfileSettings';
import { DoctorDashboard } from './pages/doctor/DoctorDashboard';
import { DoctorSchedule } from './pages/doctor/DoctorSchedule';
import { ConsultationWorkspace } from './pages/doctor/ConsultationWorkspace';
import { TelemedicineRoom } from './pages/telemedicine/TelemedicineRoom';
import { IntegrationHub } from './pages/integration/IntegrationHub';

const MainLayout: React.FC = () => {
  const { activeTab, toastMessage } = useAuth();

  const renderContent = () => {
    switch (activeTab) {
      case 'patient-dashboard':
        return <PatientDashboard />;
      case 'patient-appointments':
        return <PatientAppointments />;
      case 'patient-records':
        return <PatientMedicalRecords />;
      case 'patient-billing':
        return <PatientBilling />;
      case 'patient-profile':
        return <PatientProfileSettings />;
      case 'doctor-dashboard':
        return <DoctorDashboard />;
      case 'doctor-schedule':
        return <DoctorSchedule />;
      case 'doctor-consultation':
        return <ConsultationWorkspace />;
      case 'telemedicine-room':
        return <TelemedicineRoom />;
      case 'integration-qa':
        return <IntegrationHub />;
      default:
        return <PatientDashboard />;
    }
  };

  return (
    <div className="app-container">
      <Navbar />
      <main className="main-content">
        {renderContent()}
      </main>

      {/* Floating Toast Notification */}
      {toastMessage && (
        <div className="toast-container">
          <div className="toast">
            <span>{toastMessage}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <MainLayout />
    </AuthProvider>
  );
};

export default App;
