import {
  User,
  DemoPersona,
  Department,
  DoctorProfile,
  PatientProfile,
  Appointment,
  TimeSlot,
  LabReport,
  RadiologyReport,
  Invoice,
  TelemedicineSession,
  Notification,
  Encounter
} from '../types';

const API_BASE = '/api/v1';

class ApiService {
  private currentUsername: string = localStorage.getItem('hms_active_user') || 'patient_priya';
  private tenantSlug: string = localStorage.getItem('hms_active_tenant') || 'caretrust-health';

  public setActiveUser(username: string) {
    this.currentUsername = username;
    localStorage.setItem('hms_active_user', username);
  }

  public getActiveUser(): string {
    return this.currentUsername;
  }

  public setTenant(slug: string) {
    this.tenantSlug = slug;
    localStorage.setItem('hms_active_tenant', slug);
  }

  public getTenant(): string {
    return this.tenantSlug;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const headers = {
      'Content-Type': 'application/json',
      'X-Impersonate-User': this.currentUsername,
      'X-Tenant-ID': this.tenantSlug,
      ...(options.headers || {}),
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      let errorMessage = `HTTP Error ${response.status}: ${response.statusText}`;
      try {
        const errorData = await response.json();
        if (errorData.error) {
          errorMessage = typeof errorData.error === 'string' ? errorData.error : errorData.error.message || errorMessage;
        } else if (errorData.detail) {
          errorMessage = errorData.detail;
        } else {
          errorMessage = JSON.stringify(errorData);
        }
      } catch (e) {
        // use default message
      }
      throw new Error(errorMessage);
    }

    return response.json();
  }

  // --- Auth & Personas ---
  public async getCurrentUser(): Promise<{ authenticated: boolean; user: User; tenant: any }> {
    return this.request('/core/me/');
  }

  public async getDemoPersonas(): Promise<{ personas: DemoPersona[] }> {
    return this.request('/core/demo-personas/');
  }

  public async switchRole(username: string): Promise<any> {
    this.setActiveUser(username);
    return this.request('/core/switch-role/', {
      method: 'POST',
      body: JSON.stringify({ username }),
    });
  }

  // --- Patient Portal ---
  public async getPatientDashboard(): Promise<any> {
    return this.request('/patient-portal/dashboard/');
  }

  public async getPatientProfile(): Promise<PatientProfile> {
    return this.request('/patient-portal/profile/');
  }

  public async updatePatientProfile(data: Partial<PatientProfile>): Promise<any> {
    return this.request('/patient-portal/profile/', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  public async getPatientMedicalRecords(): Promise<any> {
    return this.request('/patient-portal/medical-records/');
  }

  public async getPatientBilling(): Promise<any> {
    return this.request('/patient-portal/billing/');
  }

  // --- Doctor Portal ---
  public async getDoctorDashboard(): Promise<any> {
    return this.request('/doctor-portal/dashboard/');
  }

  public async getDoctorSchedule(date?: string, viewMode: 'day' | 'week' = 'day'): Promise<any> {
    const params = new URLSearchParams();
    if (date) params.append('date', date);
    params.append('view', viewMode);
    return this.request(`/doctor-portal/schedule/?${params.toString()}`);
  }

  public async getConsultationWorkspace(appointmentId: string): Promise<any> {
    return this.request(`/doctor-portal/consultation/${appointmentId}/`);
  }

  public async updateConsultationNotes(appointmentId: string, data: any): Promise<any> {
    return this.request(`/doctor-portal/consultation/${appointmentId}/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  public async signEncounter(encounterId: string): Promise<any> {
    return this.request(`/clinical/encounters/${encounterId}/sign/`, {
      method: 'POST',
    });
  }

  // --- Appointments ---
  public async getDepartments(): Promise<Department[]> {
    return this.request('/appointments/departments/');
  }

  public async getDoctors(departmentId?: string, telemedicineOnly?: boolean): Promise<DoctorProfile[]> {
    const params = new URLSearchParams();
    if (departmentId) params.append('department', departmentId);
    if (telemedicineOnly) params.append('telemedicine', 'true');
    return this.request(`/appointments/doctors/?${params.toString()}`);
  }

  public async getDoctorAvailableSlots(doctorId: string, date: string): Promise<{ slots: TimeSlot[]; available_count: number }> {
    return this.request(`/appointments/doctors/${doctorId}/available-slots/?date=${date}`);
  }

  public async bookAppointment(data: { doctor_id: string; appointment_date: string; start_time: string; appointment_type: string; reason_for_visit: string }): Promise<Appointment> {
    return this.request('/appointments/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  public async cancelAppointment(appointmentId: string, reason: string): Promise<any> {
    return this.request(`/appointments/${appointmentId}/cancel/`, {
      method: 'POST',
      body: JSON.stringify({ cancellation_reason: reason }),
    });
  }

  // --- Diagnostics ---
  public async getLabReports(): Promise<LabReport[]> {
    return this.request('/diagnostics/lab-reports/');
  }

  public async approveLabReport(reportId: string): Promise<any> {
    return this.request(`/diagnostics/lab-reports/${reportId}/approve/`, {
      method: 'POST',
    });
  }

  public async getRadiologyReports(): Promise<RadiologyReport[]> {
    return this.request('/diagnostics/radiology-reports/');
  }

  // --- Billing ---
  public async payInvoiceSandbox(invoiceId: string, paymentMethod: string = 'CREDIT_CARD'): Promise<any> {
    return this.request(`/billing/invoices/${invoiceId}/pay-sandbox/`, {
      method: 'POST',
      body: JSON.stringify({ payment_method: paymentMethod }),
    });
  }

  // --- Telemedicine & WebRTC ---
  public async getTelemedicineIceConfig(): Promise<any> {
    return this.request('/telemedicine/ice-config/');
  }

  public async getAppointmentTelemedicineSession(appointmentId: string): Promise<TelemedicineSession> {
    return this.request(`/telemedicine/appointment/${appointmentId}/`);
  }

  public async getTelemedicineSession(sessionId: string): Promise<TelemedicineSession> {
    return this.request(`/telemedicine/sessions/${sessionId}/`);
  }

  public async joinTelemedicineRoom(sessionId: string, role: string): Promise<any> {
    return this.request(`/telemedicine/sessions/${sessionId}/join/`, {
      method: 'POST',
      body: JSON.stringify({ role }),
    });
  }

  public async pollSignalingMessages(sessionId: string, role: string): Promise<any> {
    return this.request(`/telemedicine/sessions/${sessionId}/signaling/?role=${role}`);
  }

  public async sendSignalingMessage(sessionId: string, senderRole: string, messageType: string, payload: any): Promise<any> {
    return this.request(`/telemedicine/sessions/${sessionId}/signaling/`, {
      method: 'POST',
      body: JSON.stringify({
        sender_role: senderRole,
        message_type: messageType,
        payload,
      }),
    });
  }

  public async leaveTelemedicineRoom(sessionId: string, role: string, notes?: string): Promise<any> {
    return this.request(`/telemedicine/sessions/${sessionId}/leave/`, {
      method: 'POST',
      body: JSON.stringify({
        role,
        clinical_quick_notes: notes,
      }),
    });
  }

  // --- Notification Center ---
  public async getNotifications(category?: string, isRead?: boolean): Promise<{ unread_count: number; total_count: number; notifications: Notification[] }> {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (isRead !== undefined) params.append('is_read', String(isRead));
    return this.request(`/notifications/?${params.toString()}`);
  }

  public async getUnreadNotificationCount(): Promise<{ unread_count: number }> {
    return this.request('/notifications/unread-count/');
  }

  public async markNotificationRead(id: string): Promise<any> {
    return this.request(`/notifications/${id}/read/`, {
      method: 'POST',
    });
  }

  public async markAllNotificationsRead(): Promise<any> {
    return this.request('/notifications/mark-all-read/', {
      method: 'POST',
    });
  }

  public async getDeliveryLogs(): Promise<any[]> {
    return this.request('/notifications/delivery-logs/');
  }

  // --- System Health & Integration ---
  public async getSystemHealth(): Promise<any> {
    return this.request('/health/');
  }
}

export const api = new ApiService();
