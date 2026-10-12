import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { PatientProfile } from '../../types';
import {
  User,
  Shield,
  Phone,
  Mail,
  Home,
  AlertCircle,
  CheckCircle,
  Save,
  Lock
} from 'lucide-react';

export const PatientProfileSettings: React.FC = () => {
  const { showToast } = useAuth();
  const [profile, setProfile] = useState<PatientProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);

  // Form states
  const [phone, setPhone] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [emergencyName, setEmergencyName] = useState<string>('');
  const [emergencyPhone, setEmergencyPhone] = useState<string>('');
  const [emergencyRelation, setEmergencyRelation] = useState<string>('');
  const [address, setAddress] = useState<string>('');
  const [city, setCity] = useState<string>('');
  const [state, setState] = useState<string>('');
  const [postalCode, setPostalCode] = useState<string>('');

  useEffect(() => {
    setLoading(true);
    api.getPatientProfile()
      .then((data) => {
        setProfile(data);
        setPhone(data.phone || '');
        setEmail(data.email || '');
        setEmergencyName(data.emergency_contact_name || '');
        setEmergencyPhone(data.emergency_contact_phone || '');
        setEmergencyRelation(data.emergency_contact_relation || '');
        setAddress(data.address_line || '');
        setCity(data.city || '');
        setState(data.state || '');
        setPostalCode(data.postal_code || '');
      })
      .catch((err) => {
        console.error(err);
        showToast('Failed to load profile.');
      })
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await api.updatePatientProfile({
        phone,
        email,
        emergency_contact_name: emergencyName,
        emergency_contact_phone: emergencyPhone,
        emergency_contact_relation: emergencyRelation,
        address_line: address,
        city,
        state,
        postal_code: postalCode,
      });
      showToast(res.message || 'Profile updated successfully.');
      setProfile(res.profile);
    } catch (err: any) {
      showToast(`Update error: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '60px', textAlign: 'center', color: 'var(--slate-400)' }}>
        Loading patient profile details...
      </div>
    );
  }

  if (!profile) return null;

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--slate-900)' }}>
          Patient Profile & Personal Info
        </h1>
        <p style={{ fontSize: '0.88rem', color: 'var(--slate-500)' }}>
          Manage your verified contact details and emergency contacts. Clinical identifiers are locked for medical safety.
        </p>
      </div>

      <form onSubmit={handleSave}>
        {/* Clinician-Controlled Locked Demographics */}
        <div className="card" style={{ marginBottom: '20px', background: 'var(--slate-50)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
            <Lock className="text-slate-500" size={18} />
            <h3 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--slate-800)' }}>
              Medical Records Identifiers (Clinician-Verified • Read-Only)
            </h3>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '14px', fontSize: '0.85rem' }}>
            <div>
              <span style={{ color: 'var(--slate-500)' }}>Full Name:</span>
              <div style={{ fontWeight: 700, color: 'var(--slate-900)' }}>{profile.full_name}</div>
            </div>
            <div>
              <span style={{ color: 'var(--slate-500)' }}>Medical Record # (MRN):</span>
              <div style={{ fontWeight: 700, color: 'var(--color-primary-dark)' }}>{profile.mrn}</div>
            </div>
            <div>
              <span style={{ color: 'var(--slate-500)' }}>Blood Group:</span>
              <div style={{ fontWeight: 700, color: 'var(--slate-900)' }}>{profile.blood_group}</div>
            </div>
            <div>
              <span style={{ color: 'var(--slate-500)' }}>Date of Birth:</span>
              <div style={{ fontWeight: 700, color: 'var(--slate-900)' }}>{profile.date_of_birth || '1988-06-14'}</div>
            </div>
            <div>
              <span style={{ color: 'var(--slate-500)' }}>Gender:</span>
              <div style={{ fontWeight: 700, color: 'var(--slate-900)' }}>{profile.gender}</div>
            </div>
            <div>
              <span style={{ color: 'var(--slate-500)' }}>Insurance Policy:</span>
              <div style={{ fontWeight: 700, color: 'var(--slate-900)' }}>{profile.insurance_provider} ({profile.insurance_policy_number})</div>
            </div>
          </div>
        </div>

        {/* Editable Contact Information */}
        <div className="card" style={{ marginBottom: '20px' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '16px' }}>
            Contact & Address Details
          </h3>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '14px' }}>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Phone Number</label>
              <input
                type="text"
                className="form-input"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
              />
            </div>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Email Address</label>
              <input
                type="email"
                className="form-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Street Address</label>
            <input
              type="text"
              className="form-input"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: '14px' }}>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">City</label>
              <input
                type="text"
                className="form-input"
                value={city}
                onChange={(e) => setCity(e.target.value)}
              />
            </div>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">State</label>
              <input
                type="text"
                className="form-input"
                value={state}
                onChange={(e) => setState(e.target.value)}
              />
            </div>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Postal Code</label>
              <input
                type="text"
                className="form-input"
                value={postalCode}
                onChange={(e) => setPostalCode(e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* Emergency Contact */}
        <div className="card" style={{ marginBottom: '24px' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '16px' }}>
            Designated Emergency Contact
          </h3>

          <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr 1fr', gap: '14px' }}>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Emergency Contact Name</label>
              <input
                type="text"
                className="form-input"
                value={emergencyName}
                onChange={(e) => setEmergencyName(e.target.value)}
              />
            </div>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Phone</label>
              <input
                type="text"
                className="form-input"
                value={emergencyPhone}
                onChange={(e) => setEmergencyPhone(e.target.value)}
              />
            </div>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Relationship</label>
              <input
                type="text"
                className="form-input"
                value={emergencyRelation}
                onChange={(e) => setEmergencyRelation(e.target.value)}
              />
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button type="submit" disabled={saving} className="btn btn-primary" style={{ minWidth: '160px' }}>
            <Save size={16} /> {saving ? 'Saving...' : 'Save Profile Changes'}
          </button>
        </div>
      </form>
    </div>
  );
};
