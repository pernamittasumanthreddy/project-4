import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { BookAppointmentModal } from './BookAppointmentModal';
import {
  Calendar,
  Clock,
  Video,
  FileText,
  CreditCard,
  Pill,
  AlertTriangle,
  ChevronRight,
  ShieldCheck,
  Plus,
  CheckCircle2,
  ExternalLink,
  UserCheck
} from 'lucide-react';

export const PatientDashboard: React.FC = () => {
  const { setActiveTab, setSelectedTelemedicineSessionId, showToast } = useAuth();
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [isBookModalOpen, setIsBookModalOpen] = useState<boolean>(false);

  const loadDashboard = async () => {
    setLoading(true);
    try {
      const data = await api.getPatientDashboard();
      setDashboardData(data);
    } catch (err: any) {
      console.error(err);
      showToast(err.message || 'Failed to load patient dashboard.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div style={{ padding: '60px 0', textAlign: 'center', color: 'var(--slate-500)' }}>
        <div style={{ fontSize: '1.1rem', fontWeight: 600 }}>Loading verified patient records...</div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: 'var(--slate-500)' }}>
        Patient record not available. Please switch to a patient persona.
      </div>
    );
  }

  const { patient, summary_stats, upcoming_appointments, approved_lab_reports, active_prescriptions, hospital_announcements } = dashboardData;

  const handleLaunchTelemedicine = (appointment: any) => {
    // Navigate to telemedicine room for this appointment
    api.getAppointmentTelemedicineSession(appointment.id)
      .then((session) => {
        setSelectedTelemedicineSessionId(session.id);
        setActiveTab('telemedicine-room');
      })
      .catch((err) => {
        showToast(`Could not open virtual room: ${err.message}`);
      });
  };

  return (
    <div>
      {/* Welcome & Patient Header */}
      <div
        style={{
          background: 'linear-gradient(135deg, #0F766E 0%, #0369A1 100%)',
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
              Verified Patient Portal
            </span>
            <span style={{ fontSize: '0.82rem', opacity: 0.9 }}>
              {patient.tenant_name}
            </span>
          </div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '6px' }}>
            Welcome back, {patient.full_name}
          </h1>
          <p style={{ opacity: 0.9, fontSize: '0.92rem', maxWidth: '600px' }}>
            Medical Record Number: <strong>{patient.mrn}</strong> • Blood Type: <strong>{patient.blood_group}</strong> • Gender: <strong>{patient.gender}</strong>
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={() => setIsBookModalOpen(true)}
            className="btn btn-primary"
            style={{ background: 'white', color: 'var(--color-primary-dark)', fontWeight: 700 }}
          >
            <Plus size={16} /> Book Appointment
          </button>
          <button
            onClick={() => setActiveTab('patient-records')}
            className="btn"
            style={{ background: 'rgba(255,255,255,0.15)', color: 'white', border: '1px solid rgba(255,255,255,0.3)' }}
          >
            <FileText size={16} /> My Records
          </button>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon-box teal">
            <Calendar size={24} />
          </div>
          <div>
            <div className="metric-value">{summary_stats.upcoming_appointments_count}</div>
            <div className="metric-label">Upcoming Appointments</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box blue">
            <Pill size={24} />
          </div>
          <div>
            <div className="metric-value">{summary_stats.active_prescriptions_count}</div>
            <div className="metric-label">Active Prescriptions</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box green">
            <FileText size={24} />
          </div>
          <div>
            <div className="metric-value">{summary_stats.approved_lab_reports_count}</div>
            <div className="metric-label">Approved Lab Reports</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon-box amber">
            <CreditCard size={24} />
          </div>
          <div>
            <div className="metric-value">${summary_stats.outstanding_balance_usd.toFixed(2)}</div>
            <div className="metric-label">Outstanding Balance</div>
          </div>
        </div>
      </div>

      {/* Main 2-Column Dashboard Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.6fr 1fr', gap: '24px' }}>
        {/* Left Column: Upcoming Consultations & Active Prescriptions */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Upcoming Appointments Card */}
          <div className="card">
            <div className="card-header">
              <div>
                <h2 className="card-title">
                  <Calendar className="text-teal-600" size={20} /> Upcoming Consultations
                </h2>
                <div className="card-subtitle">Scheduled in-person and virtual telemedicine appointments</div>
              </div>
              <button onClick={() => setActiveTab('patient-appointments')} className="btn btn-sm btn-outline">
                View All
              </button>
            </div>

            {upcoming_appointments.length === 0 ? (
              <div style={{ padding: '24px', textAlign: 'center', color: 'var(--slate-400)', background: 'var(--slate-50)', borderRadius: 'var(--radius-md)' }}>
                No appointments scheduled. Click "Book Appointment" to reserve a time with your doctor.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {upcoming_appointments.map((appt: any) => (
                  <div
                    key={appt.id}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '16px',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--slate-200)',
                      background: 'var(--surface-white)',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                      <img
                        src={appt.doctor_avatar || 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=80'}
                        alt={appt.doctor_name}
                        style={{ width: '46px', height: '46px', borderRadius: '50%', objectFit: 'cover' }}
                      />
                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <span style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--slate-900)' }}>
                            {appt.doctor_name}
                          </span>
                          <span className={`badge ${appt.appointment_type === 'TELEMEDICINE' ? 'badge-info' : 'badge-neutral'}`}>
                            {appt.appointment_type === 'TELEMEDICINE' ? 'Virtual Video' : 'In-Person'}
                          </span>
                        </div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--slate-500)', marginTop: '2px' }}>
                          {appt.doctor_specialization} • <strong>{appt.appointment_date}</strong> at {appt.start_time}
                        </div>
                        <div style={{ fontSize: '0.78rem', color: 'var(--slate-600)', marginTop: '4px' }}>
                          Reason: {appt.reason_for_visit}
                        </div>
                      </div>
                    </div>

                    <div>
                      {appt.appointment_type === 'TELEMEDICINE' ? (
                        <button
                          onClick={() => handleLaunchTelemedicine(appt)}
                          className="btn btn-sm btn-primary"
                          style={{ gap: '6px' }}
                        >
                          <Video size={14} /> Join Call
                        </button>
                      ) : (
                        <span className="badge badge-success">
                          Confirmed
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Active Prescriptions Card */}
          <div className="card">
            <div className="card-header">
              <div>
                <h2 className="card-title">
                  <Pill className="text-teal-600" size={20} /> Current Prescriptions & Medications
                </h2>
                <div className="card-subtitle">Active therapies prescribed by authorized clinicians</div>
              </div>
              <button onClick={() => setActiveTab('patient-records')} className="btn btn-sm btn-outline">
                Full EMR History
              </button>
            </div>

            {active_prescriptions.length === 0 ? (
              <div style={{ padding: '20px', textAlign: 'center', color: 'var(--slate-400)' }}>
                No active prescriptions recorded.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {active_prescriptions.map((rx: any) => (
                  <div
                    key={rx.id}
                    style={{
                      padding: '14px 16px',
                      borderRadius: 'var(--radius-md)',
                      background: 'var(--slate-50)',
                      border: '1px solid var(--slate-200)',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <span style={{ fontWeight: 700, fontSize: '0.88rem', color: 'var(--slate-900)' }}>
                        Prescription #{rx.prescription_number}
                      </span>
                      <span style={{ fontSize: '0.78rem', color: 'var(--slate-500)' }}>
                        Valid through: {rx.valid_until}
                      </span>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                      {rx.items?.map((item: any, idx: number) => (
                        <div key={idx} style={{ fontSize: '0.82rem', color: 'var(--slate-700)' }}>
                          • <strong>{item.medication_name} ({item.dosage})</strong> — {item.frequency}. <em>{item.instructions}</em>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Approved Lab Results & Hospital Announcements */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Approved Lab Investigations */}
          <div className="card">
            <div className="card-header">
              <div>
                <h2 className="card-title">
                  <CheckCircle2 className="text-green-600" size={20} /> Diagnostic Lab Results
                </h2>
                <div className="card-subtitle">Pathologist-approved clinical investigations</div>
              </div>
            </div>

            {approved_lab_reports.length === 0 ? (
              <div style={{ padding: '20px', textAlign: 'center', color: 'var(--slate-400)' }}>
                No published laboratory reports available.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {approved_lab_reports.map((lab: any) => (
                  <div
                    key={lab.id}
                    style={{
                      padding: '12px 14px',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--slate-200)',
                      background: 'var(--surface-white)',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                      <span style={{ fontWeight: 700, fontSize: '0.86rem', color: 'var(--slate-900)' }}>
                        {lab.test_name}
                      </span>
                      <span className="badge badge-success">Approved</span>
                    </div>
                    <div style={{ fontSize: '0.76rem', color: 'var(--slate-500)' }}>
                      Collected: {lab.order_date} • {lab.results?.length || 0} metrics reported
                    </div>
                    {lab.conclusion && (
                      <div style={{ fontSize: '0.78rem', color: 'var(--slate-600)', marginTop: '4px', fontStyle: 'italic' }}>
                        "{lab.conclusion}"
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Outstanding Invoice Summary */}
          <div className="card" style={{ background: summary_stats.outstanding_balance_usd > 0 ? 'var(--color-warning-light)' : 'var(--surface-white)', border: summary_stats.outstanding_balance_usd > 0 ? '1px solid #FDE68A' : 'var(--border-light)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CreditCard className="text-amber-600" size={20} />
                <h3 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--slate-900)' }}>Billing Summary</h3>
              </div>
              <span className="badge badge-warning">
                {summary_stats.unpaid_invoices_count} Unpaid
              </span>
            </div>
            <p style={{ fontSize: '0.84rem', color: 'var(--slate-700)', marginBottom: '14px' }}>
              Your current outstanding balance is <strong>${summary_stats.outstanding_balance_usd.toFixed(2)}</strong>. Settle seamlessly using our sandbox payment adapter.
            </p>
            <button
              onClick={() => setActiveTab('patient-billing')}
              className="btn btn-sm btn-primary"
              style={{ width: '100%' }}
            >
              Review Invoices & Pay in Sandbox
            </button>
          </div>

          {/* Hospital Announcements */}
          <div className="card">
            <h3 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <AlertTriangle className="text-teal-600" size={18} /> Network Announcements
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {hospital_announcements?.map((ann: any) => (
                <div key={ann.id} style={{ borderLeft: '3px solid var(--color-primary)', paddingLeft: '12px' }}>
                  <div style={{ fontWeight: 700, fontSize: '0.84rem', color: 'var(--slate-900)' }}>
                    {ann.title}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--slate-600)', marginTop: '2px' }}>
                    {ann.content}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Book Appointment Wizard Modal */}
      <BookAppointmentModal
        isOpen={isBookModalOpen}
        onClose={() => setIsBookModalOpen(false)}
        onSuccess={loadDashboard}
      />
    </div>
  );
};
