import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { Appointment } from '../../types';
import {
  Calendar as CalendarIcon,
  Clock,
  Video,
  Stethoscope,
  ChevronLeft,
  ChevronRight,
  Filter
} from 'lucide-react';

export const DoctorSchedule: React.FC = () => {
  const { setActiveTab, setSelectedAppointmentId, setSelectedTelemedicineSessionId, showToast } = useAuth();
  const [selectedDate, setSelectedDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [viewMode, setViewMode] = useState<'day' | 'week'>('day');
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadSchedule = async () => {
    setLoading(true);
    try {
      const res = await api.getDoctorSchedule(selectedDate, viewMode);
      setAppointments(res.appointments || []);
    } catch (err: any) {
      console.error(err);
      showToast('Failed to load doctor schedule.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSchedule();
  }, [selectedDate, viewMode]);

  const handleOpenWorkspace = (appointmentId: string) => {
    setSelectedAppointmentId(appointmentId);
    setActiveTab('doctor-consultation');
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--slate-900)' }}>
            Physician Consultation Agenda
          </h1>
          <p style={{ fontSize: '0.88rem', color: 'var(--slate-500)' }}>
            Daily clinic timetable, telemedicine bookings, and patient check-in records.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {/* Day / Week Toggle */}
          <div style={{ display: 'flex', background: 'var(--slate-200)', borderRadius: 'var(--radius-sm)', padding: '2px' }}>
            <button
              onClick={() => setViewMode('day')}
              className={`btn btn-sm ${viewMode === 'day' ? 'btn-primary' : 'btn-secondary'}`}
              style={{ border: 'none', borderRadius: 'var(--radius-sm)' }}
            >
              Day Agenda
            </button>
            <button
              onClick={() => setViewMode('week')}
              className={`btn btn-sm ${viewMode === 'week' ? 'btn-primary' : 'btn-secondary'}`}
              style={{ border: 'none', borderRadius: 'var(--radius-sm)' }}
            >
              Weekly Overview
            </button>
          </div>

          {/* Date Picker */}
          <input
            type="date"
            className="form-input"
            style={{ width: 'auto' }}
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
          />
        </div>
      </div>

      {/* Agenda Card */}
      <div className="card">
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--slate-400)' }}>
            Retrieving schedule agenda...
          </div>
        ) : appointments.length === 0 ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--slate-400)' }}>
            No appointments scheduled on {selectedDate}.
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Appt #</th>
                  <th>Patient Name</th>
                  <th>MRN</th>
                  <th>Consultation Type</th>
                  <th>Status</th>
                  <th>Chief Reason</th>
                  <th>Workspace</th>
                </tr>
              </thead>
              <tbody>
                {appointments.map((a) => (
                  <tr key={a.id}>
                    <td style={{ fontWeight: 800, color: 'var(--slate-900)' }}>
                      {a.start_time.slice(0, 5)} - {a.end_time?.slice(0, 5)}
                    </td>
                    <td style={{ fontWeight: 700 }}>{a.appointment_number}</td>
                    <td style={{ fontWeight: 700, color: 'var(--slate-900)' }}>{a.patient_name}</td>
                    <td>{a.patient_mrn}</td>
                    <td>
                      <span className={`badge ${a.appointment_type === 'TELEMEDICINE' ? 'badge-info' : 'badge-neutral'}`}>
                        {a.appointment_type === 'TELEMEDICINE' ? 'Virtual Video' : 'In-Person'}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${a.status === 'CONFIRMED' ? 'badge-success' : a.status === 'COMPLETED' ? 'badge-info' : 'badge-danger'}`}>
                        {a.status}
                      </span>
                    </td>
                    <td>{a.reason_for_visit}</td>
                    <td>
                      <button
                        onClick={() => handleOpenWorkspace(a.id)}
                        className="btn btn-sm btn-primary"
                        style={{ padding: '4px 10px', fontSize: '0.78rem' }}
                      >
                        <Stethoscope size={13} /> Open
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
