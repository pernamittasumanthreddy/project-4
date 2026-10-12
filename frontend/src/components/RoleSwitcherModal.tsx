import React from 'react';
import { useAuth } from '../context/AuthContext';
import { X, UserCheck, Shield, Stethoscope, User as UserIcon, Building2 } from 'lucide-react';

interface RoleSwitcherModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const RoleSwitcherModal: React.FC<RoleSwitcherModalProps> = ({ isOpen, onClose }) => {
  const { availablePersonas, currentUser, switchUser } = useAuth();

  if (!isOpen) return null;

  const handleSelect = async (username: string) => {
    await switchUser(username);
    onClose();
  };

  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'DOCTOR':
        return <Stethoscope size={20} className="text-teal-600" />;
      case 'PATIENT':
        return <UserIcon size={20} className="text-blue-600" />;
      case 'HOSPITAL_ADMIN':
      case 'SUPER_ADMIN':
        return <Shield size={20} className="text-indigo-600" />;
      default:
        return <Building2 size={20} className="text-slate-600" />;
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '580px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--slate-900)' }}>
              1-Click Role & Persona Switcher
            </h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--slate-500)' }}>
              Switch instantly between pre-seeded healthcare personas to test role-specific portals.
            </p>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--slate-400)' }}
          >
            <X size={22} />
          </button>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {availablePersonas.map((persona) => {
            const isActive = currentUser?.username === persona.username;
            return (
              <div
                key={persona.id}
                onClick={() => handleSelect(persona.username)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '14px 18px',
                  borderRadius: 'var(--radius-md)',
                  border: isActive ? '2px solid var(--color-primary)' : '1px solid var(--slate-200)',
                  background: isActive ? 'var(--color-primary-light)' : 'var(--surface-white)',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                  <img
                    src={persona.avatar_url || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100'}
                    alt={persona.name}
                    style={{
                      width: '44px',
                      height: '44px',
                      borderRadius: '50%',
                      objectFit: 'cover',
                      border: '2px solid var(--slate-200)',
                    }}
                  />
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--slate-900)' }}>
                        {persona.name}
                      </span>
                      <span className={`badge ${persona.role === 'DOCTOR' ? 'badge-info' : persona.role === 'PATIENT' ? 'badge-success' : 'badge-neutral'}`}>
                        {persona.role_display}
                      </span>
                    </div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--slate-500)', marginTop: '2px' }}>
                      {persona.specialty_or_info} • <span style={{ color: 'var(--slate-700)' }}>{persona.tenant_name}</span>
                    </div>
                  </div>
                </div>

                <div>
                  {isActive ? (
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--color-primary-dark)', fontWeight: 700, fontSize: '0.85rem' }}>
                      <UserCheck size={18} /> Active
                    </span>
                  ) : (
                    <button className="btn btn-sm btn-secondary">
                      Switch
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
