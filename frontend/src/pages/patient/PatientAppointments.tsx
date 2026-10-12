import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { Appointment } from '../../types';
import { BookAppointmentModal } from './BookAppointmentModal';
import {
  Calendar,
  Clock,
  Video,
  XCircle,
  Plus,
  Filter,
  CheckCircle,
  AlertCircle,
  Stethoscope,
  ChevronRight
} from 'lucide-react';

export const PatientAppointments: React.FC = () => {
  const { setActiveTab, setSelectedTelemedicineSessionId, showToast } = useAuth();
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [statusFilter, setStatusFilter] = useState<string>('ALL');
  const [isBookModalOpen, setIsBookModalOpen] = useState<boolean>(false);

  // Cancellation state
  const [cancelModalAppt, setCancelModalAppt] = useState<Appointment | null>(null);
  const [cancelReason, setCancelReason] = useState<string>('');
  const [isCancelling, setIsCancelling] = useState<boolean>(false);

  const loadAppointments = async () => {
    setLoading(true);
    try {
      const dashboard = await api.getPatientDashboard();
      const upcoming = dashboard.upcoming_appointments || [];
      const completed = dashboard.recent_completed_appointments || [];
      
      // Combine and deduplicate
      const all = [...upcoming, ...completed];
      const seen = new Set();
      const deduped = all.filter((a: any) => {
        if (seen.has(a.id)) return false;
        seen.add(a.id);
        return true;
      });
      setAppointments(deduped);
    } catch (err: any) {
      console.error(err);
      showToast('Failed to load appointments.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAppointments();
  }, []);

  const handleLaunchTelemedicine = (appointment: Appointment) => {
    api.getAppointmentTelemedicineSession(appointment.id)
      .then((session) => {
        setSelectedTelemedicineSessionId(session.id);
        setActiveTab('telemedicine-room');
      })
      .catch((err) => {
        showToast(`Could not open virtual consultation room: ${err.message}`);
      });
  };

  const handleConfirmCancel = async () => {
    if (!cancelModalAppt) return;
    setIsCancelling(true);
    try {
      await api.cancelAppointment(cancelModalAppt.id, cancelReason || 'Patient requested schedule cancellation.');
      showToast(`Appointment #${cancelModalAppt.appointment_number} has been cancelled.`);
      setCancelModalAppt(null);
      setCancelReason('');
      loadAppointments();
    } catch (err: any) {
      showToast(`Cancellation failed: ${err.message}`);
    } finally {
      setIsCancelling(false);
    }
  };

  const filteredAppointments = appointments.filter((a) => {
    if (statusFilter === 'ALL') return true;
    return a.status === statusFilter;
  });

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--slate-900)' }}>
            My Clinical Consultations
          </h1>
          <p style={{ fontSize: '0.88rem', color: 'var(--slate-500)' }}>
            Manage in-clinic and virtual telemedicine appointments with board-certified physicians.
          </p>
        </div>
        <button onClick={() => setIsBookModalOpen(true)} className="btn btn-primary">
          <Plus size={16} /> Book New Appointment
        </button>
      </div>

      {/* Filter Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
        {[
          { key: 'ALL', label: 'All Appointments' },
          { key: 'CONFIRMED', label: 'Confirmed & Upcoming' },
          { key: 'COMPLETED', label: 'Completed History' },
          { key: 'CANCELLED', label: 'Cancelled' },
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setStatusFilter(tab.key)}
            className={`btn btn-sm ${statusFilter === tab.key ? 'btn-primary' : 'btn-secondary'}`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Appointment Cards List */}
      <div className="card">
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--slate-400)' }}>
            Loading appointments...
          </div>
        ) : filteredAppointments.length === 0 ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--slate-400)' }}>
            No appointments found for the selected filter.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {filteredAppointments.map((appt) => (
              <div
                key={appt.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '18px 20px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--slate-200)',
                  background: 'var(--surface-white)',
                  boxShadow: 'var(--shadow-sm)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <img
                    src={appt.doctor_avatar || 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=100'}
                    alt={appt.doctor_name}
                    style={{ width: '52px', height: '52px', borderRadius: '50%', objectFit: 'cover', border: '2px solid var(--slate-200)' }}
                  />
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontWeight: 800, fontSize: '1rem', color: 'var(--slate-900)' }}>
                        {appt.doctor_name}
                      </span>
                      <span className={`badge ${appt.status === 'CONFIRMED' ? 'badge-success' : appt.status === 'COMPLETED' ? 'badge-info' : 'badge-danger'}`}>
                        {appt.status}
                      </span>
                      <span className={`badge ${appt.appointment_type === 'TELEMEDICINE' ? 'badge-info' : 'badge-neutral'}`}>
                        {appt.appointment_type === 'TELEMEDICINE' ? 'Virtual Video' : 'In-Person'}
                      </span>
                    </div>

                    <div style={{ fontSize: '0.84rem', color: 'var(--slate-500)', marginTop: '4px' }}>
                      {appt.doctor_specialization} • <strong>{appt.appointment_date}</strong> at {appt.start_time}
                    </div>

                    <div style={{ fontSize: '0.82rem', color: 'var(--slate-700)', marginTop: '6px' }}>
                      <strong>Reason:</strong> {appt.reason_for_visit}
                    </div>

                    <div style={{ fontSize: '0.74rem', color: 'var(--slate-400)', marginTop: '4px' }}>
                      Reference: #{appt.appointment_number} • Fee: ${appt.doctor_fee}
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', alignItems: 'flex-end' }}>
                  {appt.appointment_type === 'TELEMEDICINE' && appt.status === 'CONFIRMED' && (
                    <button
                      onClick={() => handleLaunchTelemedicine(appt)}
                      className="btn btn-primary"
                      style={{ gap: '6px' }}
                    >
                      <Video size={16} /> Join Virtual Call
                    </button>
                  )}

                  {appt.status === 'CONFIRMED' && (
                    <button
                      onClick={() => setCancelModalAppt(appt)}
                      className="btn btn-sm btn-secondary"
                      style={{ color: 'var(--color-danger)' }}
                    >
                      <XCircle size={14} /> Cancel Appointment
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Cancel Appointment Modal */}
      {cancelModalAppt && (
        <div className="modal-overlay" onClick={() => setCancelModalAppt(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '480px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '10px' }}>
              Cancel Appointment #{cancelModalAppt.appointment_number}
            </h3>
            <p style={{ fontSize: '0.86rem', color: 'var(--slate-600)', marginBottom: '16px' }}>
              Are you sure you want to cancel your consultation with <strong>{cancelModalAppt.doctor_name}</strong> on <strong>{cancelModalAppt.appointment_date}</strong>?
            </p>

            <div className="form-group">
              <label className="form-label">Reason for Cancellation</label>
              <textarea
                className="form-textarea"
                rows={3}
                placeholder="Please state why you are cancelling this visit..."
                value={cancelReason}
                onChange={(e) => setCancelReason(e.target.value)}
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '16px' }}>
              <button onClick={() => setCancelModalAppt(null)} className="btn btn-secondary">
                Keep Appointment
              </button>
              <button onClick={handleConfirmCancel} disabled={isCancelling} className="btn btn-danger">
                {isCancelling ? 'Processing...' : 'Confirm Cancellation'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Book Wizard Modal */}
      <BookAppointmentModal
        isOpen={isBookModalOpen}
        onClose={() => setIsBookModalOpen(false)}
        onSuccess={loadAppointments}
      />
    </div>
  );
};
