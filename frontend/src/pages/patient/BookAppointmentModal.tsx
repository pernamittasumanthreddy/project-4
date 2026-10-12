import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { Department, DoctorProfile, TimeSlot } from '../../types';
import { useAuth } from '../../context/AuthContext';
import { X, Calendar, Clock, Video, UserCheck, AlertCircle, CheckCircle, ChevronRight, Stethoscope } from 'lucide-react';

interface BookAppointmentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export const BookAppointmentModal: React.FC<BookAppointmentModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const { showToast } = useAuth();
  const [departments, setDepartments] = useState<Department[]>([]);
  const [selectedDept, setSelectedDept] = useState<string>('');
  const [doctors, setDoctors] = useState<DoctorProfile[]>([]);
  const [selectedDoctor, setSelectedDoctor] = useState<DoctorProfile | null>(null);
  
  // Date and slot
  const tomorrowStr = new Date(Date.now() + 86400000).toISOString().split('T')[0];
  const [selectedDate, setSelectedDate] = useState<string>(tomorrowStr);
  const [slots, setSlots] = useState<TimeSlot[]>([]);
  const [selectedTime, setSelectedTime] = useState<string>('');
  
  const [appointmentType, setAppointmentType] = useState<'TELEMEDICINE' | 'IN_PERSON'>('TELEMEDICINE');
  const [reason, setReason] = useState<string>('');
  
  const [loading, setLoading] = useState<boolean>(false);
  const [loadingSlots, setLoadingSlots] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Load departments
  useEffect(() => {
    if (isOpen) {
      api.getDepartments().then(setDepartments).catch(console.error);
      api.getDoctors().then(setDoctors).catch(console.error);
    }
  }, [isOpen]);

  // Filter doctors when department changes
  useEffect(() => {
    if (selectedDept) {
      api.getDoctors(selectedDept).then(setDoctors).catch(console.error);
    } else {
      api.getDoctors().then(setDoctors).catch(console.error);
    }
  }, [selectedDept]);

  // Load slots when doctor or date changes
  useEffect(() => {
    if (selectedDoctor && selectedDate) {
      setLoadingSlots(true);
      setErrorMsg(null);
      api.getDoctorAvailableSlots(selectedDoctor.id, selectedDate)
        .then((res) => {
          setSlots(res.slots || []);
          setSelectedTime('');
        })
        .catch((err) => {
          console.error(err);
          setErrorMsg('Failed to load slots for this date.');
        })
        .finally(() => setLoadingSlots(false));
    }
  }, [selectedDoctor, selectedDate]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedDoctor) {
      setErrorMsg('Please select a physician.');
      return;
    }
    if (!selectedTime) {
      setErrorMsg('Please select an available consultation slot.');
      return;
    }
    if (!reason.trim()) {
      setErrorMsg('Please enter a brief reason for your consultation.');
      return;
    }

    setLoading(true);
    setErrorMsg(null);
    try {
      const result = await api.bookAppointment({
        doctor_id: selectedDoctor.id,
        appointment_date: selectedDate,
        start_time: selectedTime,
        appointment_type: appointmentType,
        reason_for_visit: reason,
      });

      showToast(`Appointment #${result.appointment_number} confirmed with ${selectedDoctor.name}!`);
      onSuccess();
      onClose();
    } catch (err: any) {
      setErrorMsg(err.message || 'Booking failed. Slot may already be reserved.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '640px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--slate-900)' }}>
              Schedule Clinical Consultation
            </h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--slate-500)' }}>
              Real-time slot reservation directly integrated with hospital clinician agendas.
            </p>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--slate-400)' }}>
            <X size={22} />
          </button>
        </div>

        {errorMsg && (
          <div style={{ padding: '12px 16px', background: 'var(--color-danger-light)', color: 'var(--color-danger)', borderRadius: 'var(--radius-md)', marginBottom: '16px', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertCircle size={18} /> {errorMsg}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Step 1: Department & Consultation Mode */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '16px' }}>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Clinical Specialty</label>
              <select
                className="form-select"
                value={selectedDept}
                onChange={(e) => setSelectedDept(e.target.value)}
              >
                <option value="">All Hospital Departments</option>
                {departments.map((d) => (
                  <option key={d.id} value={d.id}>{d.name}</option>
                ))}
              </select>
            </div>

            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Consultation Mode</label>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button
                  type="button"
                  onClick={() => setAppointmentType('TELEMEDICINE')}
                  style={{
                    flex: 1,
                    padding: '8px 10px',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: '0.8rem',
                    fontWeight: 700,
                    border: appointmentType === 'TELEMEDICINE' ? '2px solid var(--color-primary)' : '1px solid var(--slate-200)',
                    background: appointmentType === 'TELEMEDICINE' ? 'var(--color-primary-light)' : 'var(--slate-50)',
                    color: appointmentType === 'TELEMEDICINE' ? 'var(--color-primary-dark)' : 'var(--slate-600)',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '4px',
                  }}
                >
                  <Video size={14} /> Virtual Video
                </button>
                <button
                  type="button"
                  onClick={() => setAppointmentType('IN_PERSON')}
                  style={{
                    flex: 1,
                    padding: '8px 10px',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: '0.8rem',
                    fontWeight: 700,
                    border: appointmentType === 'IN_PERSON' ? '2px solid var(--color-accent)' : '1px solid var(--slate-200)',
                    background: appointmentType === 'IN_PERSON' ? 'var(--color-accent-light)' : 'var(--slate-50)',
                    color: appointmentType === 'IN_PERSON' ? 'var(--color-accent-dark)' : 'var(--slate-600)',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '4px',
                  }}
                >
                  <Stethoscope size={14} /> In-Clinic
                </button>
              </div>
            </div>
          </div>

          {/* Step 2: Select Doctor Card List */}
          <div className="form-group">
            <label className="form-label">Select Physician</label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '180px', overflowY: 'auto' }}>
              {doctors.map((doc) => {
                const isSelected = selectedDoctor?.id === doc.id;
                return (
                  <div
                    key={doc.id}
                    onClick={() => setSelectedDoctor(doc)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '10px 14px',
                      borderRadius: 'var(--radius-md)',
                      border: isSelected ? '2px solid var(--color-primary)' : '1px solid var(--slate-200)',
                      background: isSelected ? 'var(--color-primary-light)' : 'var(--surface-white)',
                      cursor: 'pointer',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <img
                        src={doc.avatar_url || 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=80'}
                        alt={doc.name}
                        style={{ width: '38px', height: '38px', borderRadius: '50%', objectFit: 'cover' }}
                      />
                      <div>
                        <div style={{ fontWeight: 700, fontSize: '0.88rem', color: 'var(--slate-900)' }}>
                          {doc.name}
                        </div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--slate-500)' }}>
                          {doc.specialization} • ⭐ {doc.rating} ({doc.review_count} reviews)
                        </div>
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontWeight: 800, fontSize: '0.9rem', color: 'var(--color-primary-dark)' }}>
                        ${doc.consultation_fee}
                      </div>
                      <div style={{ fontSize: '0.7rem', color: 'var(--slate-400)' }}>
                        {doc.slot_duration_minutes} min
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Step 3: Date & Slots */}
          {selectedDoctor && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '14px', marginBottom: '16px' }}>
              <div className="form-group" style={{ margin: 0 }}>
                <label className="form-label">Consultation Date</label>
                <input
                  type="date"
                  className="form-input"
                  min={tomorrowStr}
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                />
              </div>

              <div className="form-group" style={{ margin: 0 }}>
                <label className="form-label">
                  Available Slots {loadingSlots && <span style={{ fontSize: '0.75rem', color: 'var(--slate-400)' }}>Loading...</span>}
                </label>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '6px', maxHeight: '110px', overflowY: 'auto' }}>
                  {slots.map((s) => (
                    <button
                      key={s.time}
                      type="button"
                      disabled={!s.available}
                      onClick={() => setSelectedTime(s.time)}
                      style={{
                        padding: '6px 4px',
                        borderRadius: 'var(--radius-sm)',
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        border: selectedTime === s.time ? '2px solid var(--color-primary)' : '1px solid var(--slate-200)',
                        background: !s.available
                          ? 'var(--slate-100)'
                          : selectedTime === s.time
                          ? 'var(--color-primary-light)'
                          : 'var(--surface-white)',
                        color: !s.available
                          ? 'var(--slate-400)'
                          : selectedTime === s.time
                          ? 'var(--color-primary-dark)'
                          : 'var(--slate-800)',
                        cursor: s.available ? 'pointer' : 'not-allowed',
                        textDecoration: !s.available ? 'line-through' : 'none',
                      }}
                    >
                      {s.time_display}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Step 4: Reason */}
          <div className="form-group">
            <label className="form-label">Reason for Consultation / Chief Symptoms</label>
            <textarea
              className="form-textarea"
              rows={2}
              placeholder="e.g. Follow-up blood pressure check, review recent laboratory cholesterol panel..."
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              required
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
            <button type="button" onClick={onClose} className="btn btn-secondary">
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !selectedDoctor || !selectedTime}
              className="btn btn-primary"
            >
              {loading ? 'Confirming with Clinician Agenda...' : 'Confirm Appointment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
