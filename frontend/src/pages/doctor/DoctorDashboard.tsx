import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import {
  Stethoscope,
  Calendar,
  Clock,
  Video,
  UserCheck,
  FileCheck,
  AlertCircle,
  FileText,
  ChevronRight,
  Activity
} from 'lucide-react';

export const DoctorDashboard: React.FC = () => {
  const { setActiveTab, setSelectedAppointmentId, setSelectedTelemedicineSessionId, showToast } = useAuth();
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const loadDoctorDashboard = async () => {
    setLoading(true);
    try {
      const data = await api.getDoctorDashboard();
      setDashboardData(data);
    } catch (err: any) {
      console.error(err);
      showToast('Failed to load doctor dashboard.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDoctorDashboard();
  }, []);

  if (loading) {
    return (
      <div style={{ padding: '60px', textAlign: 'center', color: 'var(--slate-400)' }}>
        Loading physician clinic schedule and patient queue...
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--slate-500)' }}>
        Doctor profile not found. Please switch to a physician persona.
      </div>
    );
  }

  const { doctor, today_metrics, today_appointments, upcoming_appointments } = dashboardData;

  const handleOpenWorkspace = (appointmentId: string) => {
    setSelectedAppointmentId(appointmentId);
    setActiveTab('doctor-consultation');
  };

  const handleLaunchTelemedicine = (appointment: any) => {
    api.getAppointmentTelemedicineSession(appointment.id)
      .then((session) => {
        setSelectedTelemedicineSessionId(session.id);
        setActiveTab('telemedicine-room');
      })
      .catch((err) => {
        showToast(`Could not open virtual consultation room: ${err.message}`);
      });
  };

  return (
    <div>
      {/* Clinician Welcome Banner */}
      <div
        style={{
          background: 'linear-gradient(135deg, #0F766E 0%, #065F46 100%)',
          color: 'white',
          borderRadius: 'var(--radius-lg)',
          padding: '28px 32px',
          marginBottom: '28px',
          boxShadow: 'var(--shadow-md)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '20px',
        }}
      >
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
            <span className="badge badge-success" style={{ background: 'rgba(255,255,255,0.2)', color: 'white', border: 'none' }}>
              Physician Consultation Suite
            </span>
            <span style={{ fontSize: '0.82rem', opacity: 0.9 }}>
              {doctor.department} • {doctor.tenant_name}
            </span>
          </div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '6px' }}>
            Welcome, {doctor.name}
          </h1>
          <p style={{ opacity: 0.9, fontSize: '0.92rem' }}>
            {doctor.specialization} • Clinic Office: <strong>{doctor.office_room}</strong>
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={() => setActiveTab('doctor-schedule')} className="btn" style={{ background: 'rgba(255,255,255,0.2)', color: 'white' }}>
            <Calendar size={16} /> Agenda Calendar
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon-box teal">
            <Calendar size={24} />
          </div>
          <div>
            <div className="metric-value">{today_metrics.total_scheduled_today}</div>
            <div className="metric-label">Scheduled Today</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box blue">
            <UserCheck size={24} />
          </div>
          <div>
            <div className="metric-value">{today_metrics.waiting_patients_count}</div>
            <div className="metric-label">Checked-In Waiting</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box green">
            <FileCheck size={24} />
          </div>
          <div>
            <div className="metric-value">{today_metrics.completed_consultations_today}</div>
            <div className="metric-label">Completed Consults</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box amber">
            <Activity size={24} />
          </div>
          <div>
            <div className="metric-value">{today_metrics.pending_lab_reviews}</div>
            <div className="metric-label">Pending Lab Reviews</div>
          </div>
        </div>
      </div>

      {/* Today's Patient Queue */}
      <div className="card" style={{ marginBottom: '28px' }}>
        <div className="card-header">
          <div>
            <h2 className="card-title">
              <Clock className="text-teal-600" size={20} /> Today's Patient Consultation Queue
            </h2>
            <div className="card-subtitle">Scheduled visits, patient check-in status, and clinical actions</div>
          </div>
        </div>

        {today_appointments.length === 0 ? (
          <div style={{ padding: '30px', textAlign: 'center', color: 'var(--slate-400)' }}>
            No appointments scheduled for today.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {today_appointments.map((appt: any) => (
              <div
                key={appt.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '16px 20px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--slate-200)',
                  background: 'var(--surface-white)',
                  boxShadow: 'var(--shadow-sm)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <div
                    style={{
                      width: '44px',
                      height: '44px',
                      borderRadius: 'var(--radius-md)',
                      background: 'var(--slate-100)',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 800,
                      fontSize: '0.8rem',
                      color: 'var(--slate-700)',
                    }}
                  >
                    {appt.start_time.slice(0, 5)}
                  </div>

                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontWeight: 800, fontSize: '0.98rem', color: 'var(--slate-900)' }}>
                        {appt.patient_name}
                      </span>
                      <span style={{ fontSize: '0.8rem', color: 'var(--slate-500)' }}>
                        (MRN: {appt.patient_mrn})
                      </span>
                      <span className={`badge ${appt.appointment_type === 'TELEMEDICINE' ? 'badge-info' : 'badge-neutral'}`}>
                        {appt.appointment_type === 'TELEMEDICINE' ? 'Virtual Call' : 'In-Person'}
                      </span>
                      {appt.checked_in_at && (
                        <span className="badge badge-success">Checked-In</span>
                      )}
                    </div>

                    <div style={{ fontSize: '0.84rem', color: 'var(--slate-600)', marginTop: '4px' }}>
                      <strong>Reason:</strong> {appt.reason_for_visit}
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '10px' }}>
                  {appt.appointment_type === 'TELEMEDICINE' && appt.status !== 'COMPLETED' && (
                    <button
                      onClick={() => handleLaunchTelemedicine(appt)}
                      className="btn btn-sm btn-primary"
                      style={{ background: 'var(--color-accent)' }}
                    >
                      <Video size={14} /> Open Video
                    </button>
                  )}

                  <button
                    onClick={() => handleOpenWorkspace(appt.id)}
                    className="btn btn-sm btn-primary"
                  >
                    <Stethoscope size={14} /> Clinical Workspace
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Upcoming Visits Preview */}
      <div className="card">
        <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '14px' }}>
          Upcoming Consultations (This Week)
        </h3>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Appt #</th>
                <th>Patient Name</th>
                <th>MRN</th>
                <th>Date & Time</th>
                <th>Type</th>
                <th>Chief Complaint</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {upcoming_appointments?.map((u: any) => (
                <tr key={u.id}>
                  <td style={{ fontWeight: 700 }}>{u.appointment_number}</td>
                  <td style={{ fontWeight: 700, color: 'var(--slate-900)' }}>{u.patient_name}</td>
                  <td>{u.patient_mrn}</td>
                  <td>{u.appointment_date} at {u.start_time}</td>
                  <td><span className="badge badge-neutral">{u.appointment_type}</span></td>
                  <td>{u.reason_for_visit}</td>
                  <td>
                    <button onClick={() => handleOpenWorkspace(u.id)} className="btn btn-sm btn-outline">
                      Review Chart
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
