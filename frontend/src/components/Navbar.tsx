import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { RoleSwitcherModal } from './RoleSwitcherModal';
import { NotificationDrawer } from './NotificationDrawer';
import {
  Activity,
  Calendar,
  FileText,
  CreditCard,
  User as UserIcon,
  Video,
  Bell,
  Stethoscope,
  ChevronDown,
  Layers,
  Hospital,
  ShieldCheck
} from 'lucide-react';

export const Navbar: React.FC = () => {
  const {
    currentUser,
    currentRole,
    activeTenant,
    activeTab,
    setActiveTab,
    unreadCount,
  } = useAuth();

  const [isRoleModalOpen, setIsRoleModalOpen] = useState(false);
  const [isNotifDrawerOpen, setIsNotifDrawerOpen] = useState(false);

  return (
    <>
      <header className="navbar">
        <div className="navbar-inner">
          {/* Brand */}
          <div className="navbar-brand">
            <div className="brand-icon">
              <Activity size={22} />
            </div>
            <div>
              <div className="brand-title">
                {activeTenant?.name || 'CareTrust Health System'}
              </div>
              <div className="brand-subtitle">
                Enterprise Multi-Tenant SaaS • Member 7 Suite
              </div>
            </div>
          </div>

          {/* Navigation Links based on active role */}
          <nav className="nav-links">
            {currentRole === 'PATIENT' ? (
              <>
                <button
                  className={`nav-item ${activeTab === 'patient-dashboard' ? 'active' : ''}`}
                  onClick={() => setActiveTab('patient-dashboard')}
                >
                  <Activity size={16} /> Dashboard
                </button>
                <button
                  className={`nav-item ${activeTab === 'patient-appointments' ? 'active' : ''}`}
                  onClick={() => setActiveTab('patient-appointments')}
                >
                  <Calendar size={16} /> Appointments
                </button>
                <button
                  className={`nav-item ${activeTab === 'patient-records' ? 'active' : ''}`}
                  onClick={() => setActiveTab('patient-records')}
                >
                  <FileText size={16} /> Medical Records
                </button>
                <button
                  className={`nav-item ${activeTab === 'patient-billing' ? 'active' : ''}`}
                  onClick={() => setActiveTab('patient-billing')}
                >
                  <CreditCard size={16} /> Billing
                </button>
                <button
                  className={`nav-item ${activeTab === 'patient-profile' ? 'active' : ''}`}
                  onClick={() => setActiveTab('patient-profile')}
                >
                  <UserIcon size={16} /> Profile
                </button>
              </>
            ) : currentRole === 'DOCTOR' ? (
              <>
                <button
                  className={`nav-item ${activeTab === 'doctor-dashboard' ? 'active' : ''}`}
                  onClick={() => setActiveTab('doctor-dashboard')}
                >
                  <Stethoscope size={16} /> Doctor Dashboard
                </button>
                <button
                  className={`nav-item ${activeTab === 'doctor-schedule' ? 'active' : ''}`}
                  onClick={() => setActiveTab('doctor-schedule')}
                >
                  <Calendar size={16} /> Schedule & Agenda
                </button>
              </>
            ) : null}

            {/* Common Universal Navigation */}
            <button
              className={`nav-item ${activeTab === 'telemedicine-room' ? 'active' : ''}`}
              onClick={() => setActiveTab('telemedicine-room')}
            >
              <Video size={16} /> Telemedicine
            </button>
            <button
              className={`nav-item ${activeTab === 'integration-qa' ? 'active' : ''}`}
              onClick={() => setActiveTab('integration-qa')}
            >
              <ShieldCheck size={16} /> QA & Integration Hub
            </button>
          </nav>

          {/* Right Action Controls */}
          <div className="user-controls">
            {/* Notification Bell */}
            <button
              className="notification-bell-btn"
              onClick={() => setIsNotifDrawerOpen(true)}
              title="Notification Center"
            >
              <Bell size={20} />
              {unreadCount > 0 && <span className="unread-badge">{unreadCount}</span>}
            </button>

            {/* 1-Click Role Switcher Trigger */}
            <div
              className="role-switcher-badge"
              onClick={() => setIsRoleModalOpen(true)}
              title="Click to Switch Personas & Roles"
            >
              <img
                src={currentUser?.avatar_url || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=80'}
                alt={currentUser?.full_name || 'User'}
                className="avatar-img"
              />
              <div style={{ textAlign: 'left', lineHeight: '1.2' }}>
                <div style={{ fontWeight: 700, fontSize: '0.84rem', color: 'var(--slate-900)' }}>
                  {currentUser?.full_name || 'Sign In'}
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--slate-500)' }}>
                  {currentRole === 'DOCTOR' ? 'Physician' : currentRole === 'PATIENT' ? 'Patient' : 'Administrator'}
                </div>
              </div>
              <ChevronDown size={14} className="text-slate-400" />
            </div>
          </div>
        </div>
      </header>

      {/* Role Switcher Modal */}
      <RoleSwitcherModal
        isOpen={isRoleModalOpen}
        onClose={() => setIsRoleModalOpen(false)}
      />

      {/* Notification Drawer */}
      <NotificationDrawer
        isOpen={isNotifDrawerOpen}
        onClose={() => setIsNotifDrawerOpen(false)}
      />
    </>
  );
};
