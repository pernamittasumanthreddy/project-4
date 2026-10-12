import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { Notification } from '../types';
import { X, CheckCheck, Bell, ExternalLink, Mail, MessageSquare, Clock } from 'lucide-react';

interface NotificationDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export const NotificationDrawer: React.FC<NotificationDrawerProps> = ({ isOpen, onClose }) => {
  const { unreadCount, refreshUnreadCount, setActiveTab, setSelectedTelemedicineSessionId, showToast } = useAuth();
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeFilter, setActiveFilter] = useState<string>('ALL');

  const loadNotifications = async () => {
    setLoading(true);
    try {
      const categoryParam = activeFilter === 'ALL' ? undefined : activeFilter;
      const res = await api.getNotifications(categoryParam);
      setNotifications(res.notifications || []);
    } catch (err) {
      console.error('Failed to load notifications', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      loadNotifications();
    }
  }, [isOpen, activeFilter]);

  if (!isOpen) return null;

  const handleMarkRead = async (id: string) => {
    try {
      await api.markNotificationRead(id);
      await refreshUnreadCount();
      loadNotifications();
    } catch (err: any) {
      showToast(err.message);
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await api.markAllNotificationsRead();
      await refreshUnreadCount();
      loadNotifications();
      showToast('All notifications marked as read');
    } catch (err: any) {
      showToast(err.message);
    }
  };

  const handleActionClick = (notif: Notification) => {
    handleMarkRead(notif.id);
    onClose();
    if (notif.action_url.includes('/patient/appointments')) {
      setActiveTab('patient-appointments');
    } else if (notif.action_url.includes('/patient/records')) {
      setActiveTab('patient-records');
    } else if (notif.action_url.includes('/patient/billing')) {
      setActiveTab('patient-billing');
    } else if (notif.action_url.includes('/telemedicine/room/')) {
      const parts = notif.action_url.split('/telemedicine/room/');
      if (parts[1]) {
        setSelectedTelemedicineSessionId(parts[1]);
        setActiveTab('telemedicine-room');
      }
    } else if (notif.action_url.includes('/doctor/schedule')) {
      setActiveTab('doctor-schedule');
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
        style={{
          maxWidth: '520px',
          height: '85vh',
          display: 'flex',
          flexDirection: 'column',
          padding: '24px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Bell className="text-teal-600" size={22} />
            <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--slate-900)' }}>
              Notification Center
            </h3>
            {unreadCount > 0 && (
              <span className="badge badge-danger">
                {unreadCount} Unread
              </span>
            )}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            {unreadCount > 0 && (
              <button
                onClick={handleMarkAllRead}
                className="btn btn-sm btn-secondary"
                style={{ fontSize: '0.78rem' }}
              >
                <CheckCheck size={14} /> Mark All Read
              </button>
            )}
            <button
              onClick={onClose}
              style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--slate-400)' }}
            >
              <X size={22} />
            </button>
          </div>
        </div>

        {/* Category Filter Pills */}
        <div style={{ display: 'flex', gap: '6px', overflowX: 'auto', paddingBottom: '12px', borderBottom: '1px solid var(--slate-200)', marginBottom: '14px' }}>
          {['ALL', 'APPOINTMENT', 'LAB_REPORT', 'BILLING', 'TELEMEDICINE', 'CLINICAL'].map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveFilter(cat)}
              style={{
                padding: '4px 10px',
                borderRadius: 'var(--radius-full)',
                fontSize: '0.75rem',
                fontWeight: 700,
                border: activeFilter === cat ? '1px solid var(--color-primary)' : '1px solid var(--slate-200)',
                background: activeFilter === cat ? 'var(--color-primary-light)' : 'var(--slate-50)',
                color: activeFilter === cat ? 'var(--color-primary-dark)' : 'var(--slate-600)',
                cursor: 'pointer',
                whiteSpace: 'nowrap',
              }}
            >
              {cat.replace('_', ' ')}
            </button>
          ))}
        </div>

        {/* Notification Items List */}
        <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {loading ? (
            <div style={{ padding: '40px', textAlign: 'center', color: 'var(--slate-400)' }}>
              Loading notification updates...
            </div>
          ) : notifications.length === 0 ? (
            <div style={{ padding: '40px', textAlign: 'center', color: 'var(--slate-400)' }}>
              No notifications found for this category.
            </div>
          ) : (
            notifications.map((n) => (
              <div
                key={n.id}
                style={{
                  padding: '14px',
                  borderRadius: 'var(--radius-md)',
                  border: n.is_read ? '1px solid var(--slate-200)' : '1px solid var(--color-primary-border)',
                  background: n.is_read ? 'var(--surface-white)' : 'var(--color-primary-light)',
                  position: 'relative',
                  transition: 'all 0.15s ease',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '6px' }}>
                  <span className={`badge ${n.priority === 'URGENT' || n.priority === 'HIGH' ? 'badge-danger' : 'badge-info'}`}>
                    {n.category_display}
                  </span>
                  <span style={{ fontSize: '0.72rem', color: 'var(--slate-400)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Clock size={12} /> {new Date(n.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>

                <h4 style={{ fontSize: '0.92rem', fontWeight: 700, color: 'var(--slate-900)', marginBottom: '4px' }}>
                  {n.title}
                </h4>
                <p style={{ fontSize: '0.82rem', color: 'var(--slate-600)', lineHeight: '1.4', marginBottom: '10px' }}>
                  {n.message}
                </p>

                {/* Delivery Channel Verification Badges */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingTop: '8px', borderTop: '1px solid rgba(0,0,0,0.05)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.72rem', color: 'var(--slate-500)' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '2px' }} title="Simulated HIPAA-safe email dispatched">
                      <Mail size={12} className="text-teal-600" /> Email Sent
                    </span>
                    <span>•</span>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '2px' }} title="Masked SMS alert dispatched">
                      <MessageSquare size={12} className="text-blue-600" /> SMS Alert
                    </span>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    {!n.is_read && (
                      <button
                        onClick={() => handleMarkRead(n.id)}
                        className="btn btn-sm btn-secondary"
                        style={{ padding: '3px 8px', fontSize: '0.72rem' }}
                      >
                        Mark Read
                      </button>
                    )}
                    {n.action_url && (
                      <button
                        onClick={() => handleActionClick(n)}
                        className="btn btn-sm btn-primary"
                        style={{ padding: '3px 10px', fontSize: '0.75rem' }}
                      >
                        View <ExternalLink size={12} />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
