import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, DemoPersona, Tenant } from '../types';
import { api } from '../services/api';

interface AuthContextType {
  currentUser: User | null;
  currentRole: string;
  activeTenant: Tenant | null;
  availablePersonas: DemoPersona[];
  activeTab: string;
  setActiveTab: (tab: string) => void;
  selectedAppointmentId: string | null;
  setSelectedAppointmentId: (id: string | null) => void;
  selectedTelemedicineSessionId: string | null;
  setSelectedTelemedicineSessionId: (id: string | null) => void;
  unreadCount: number;
  refreshUnreadCount: () => Promise<void>;
  switchUser: (username: string) => Promise<void>;
  toastMessage: string | null;
  showToast: (message: string) => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [currentRole, setCurrentRole] = useState<string>('PATIENT');
  const [activeTenant, setActiveTenant] = useState<Tenant | null>(null);
  const [availablePersonas, setAvailablePersonas] = useState<DemoPersona[]>([]);
  const [activeTab, setActiveTab] = useState<string>('patient-dashboard');
  const [selectedAppointmentId, setSelectedAppointmentId] = useState<string | null>(null);
  const [selectedTelemedicineSessionId, setSelectedTelemedicineSessionId] = useState<string | null>(null);
  const [unreadCount, setUnreadCount] = useState<number>(0);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const showToast = (message: string) => {
    setToastMessage(message);
    setTimeout(() => {
      setToastMessage(null);
    }, 4000);
  };

  const refreshUnreadCount = async () => {
    try {
      const res = await api.getUnreadNotificationCount();
      setUnreadCount(res.unread_count);
    } catch (err) {
      console.error("Failed to fetch unread notification count", err);
    }
  };

  const loadUserData = async () => {
    setIsLoading(true);
    try {
      // 1. Fetch current user
      const meRes = await api.getCurrentUser();
      if (meRes.user) {
        setCurrentUser(meRes.user);
        setCurrentRole(meRes.user.role);
        setActiveTenant(meRes.user.tenant || null);
        
        // Default tab based on role
        if (meRes.user.role === 'DOCTOR') {
          setActiveTab('doctor-dashboard');
        } else if (meRes.user.role === 'PATIENT') {
          setActiveTab('patient-dashboard');
        } else {
          setActiveTab('integration-qa');
        }
      }

      // 2. Fetch available personas
      const personasRes = await api.getDemoPersonas();
      setAvailablePersonas(personasRes.personas || []);

      // 3. Unread count
      await refreshUnreadCount();
    } catch (err) {
      console.error("Failed to load auth state", err);
    } finally {
      setIsLoading(false);
    }
  };

  const switchUser = async (username: string) => {
    setIsLoading(true);
    try {
      await api.switchRole(username);
      api.setActiveUser(username);
      await loadUserData();
      showToast(`Switched active persona to ${username}`);
    } catch (err: any) {
      showToast(`Error switching persona: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadUserData();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        currentUser,
        currentRole,
        activeTenant,
        availablePersonas,
        activeTab,
        setActiveTab,
        selectedAppointmentId,
        setSelectedAppointmentId,
        selectedTelemedicineSessionId,
        setSelectedTelemedicineSessionId,
        unreadCount,
        refreshUnreadCount,
        switchUser,
        toastMessage,
        showToast,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
