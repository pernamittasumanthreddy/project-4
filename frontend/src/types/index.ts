export interface Tenant {
  id: string;
  name: string;
  slug: string;
  domain: string;
  tier: 'COMMUNITY' | 'REGIONAL' | 'ENTERPRISE';
  primary_color: string;
  contact_email: string;
  contact_phone: string;
  is_active: boolean;
}

export interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: 'SUPER_ADMIN' | 'HOSPITAL_ADMIN' | 'DOCTOR' | 'PATIENT' | 'NURSE' | 'PHARMACIST' | 'LAB_TECH';
  phone?: string;
  avatar_url?: string;
  tenant?: Tenant;
  doctor_profile_id?: string;
  patient_profile_id?: string;
}

export interface DemoPersona {
  id: string;
  username: string;
  name: string;
  role: string;
  role_display: string;
  specialty_or_info: string;
  tenant_name: string;
  avatar_url?: string;
}

export interface Department {
  id: string;
  name: string;
  code: string;
  description: string;
  icon_name: string;
  is_active: boolean;
}

export interface DoctorProfile {
  id: string;
  name: string;
  license_number: string;
  specialization: string;
  experience_years: number;
  qualification: string;
  consultation_fee: number | string;
  slot_duration_minutes: number;
  is_available_telemedicine: boolean;
  rating: number | string;
  review_count: number;
  bio: string;
  office_room: string;
  department: string;
  department_name?: string;
  avatar_url?: string;
  email?: string;
}

export interface PatientProfile {
  id: string;
  mrn: string;
  full_name: string;
  email: string;
  phone: string;
  date_of_birth?: string;
  gender: string;
  blood_group: string;
  emergency_contact_name: string;
  emergency_contact_phone: string;
  emergency_contact_relation: string;
  address_line: string;
  city: string;
  state: string;
  postal_code: string;
  insurance_provider: string;
  insurance_policy_number: string;
}

export interface Appointment {
  id: string;
  appointment_number: string;
  patient: string;
  patient_name: string;
  patient_mrn: string;
  doctor: string;
  doctor_name: string;
  doctor_specialization: string;
  doctor_avatar?: string;
  doctor_fee: string | number;
  appointment_date: string;
  start_time: string;
  end_time: string;
  appointment_type: 'IN_PERSON' | 'TELEMEDICINE';
  status: 'PENDING' | 'CONFIRMED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED' | 'NO_SHOW';
  reason_for_visit: string;
  notes?: string;
  cancellation_reason?: string;
  checked_in_at?: string;
  created_at: string;
}

export interface TimeSlot {
  time: string;
  time_display: string;
  available: boolean;
  duration_minutes: number;
}

export interface LabResultMetric {
  name: string;
  value: string;
  unit: string;
  reference_range: string;
  flag: 'NORMAL' | 'HIGH' | 'LOW' | 'CRITICAL';
}

export interface LabReport {
  id: string;
  report_number: string;
  test_name: string;
  test_code: string;
  category: string;
  patient: string;
  patient_name: string;
  patient_mrn: string;
  ordering_doctor?: string;
  ordering_doctor_name?: string;
  status: 'ORDERED' | 'COLLECTED' | 'ANALYZED' | 'APPROVED' | 'REJECTED';
  order_date: string;
  collected_at?: string;
  specimen_type: string;
  results: LabResultMetric[];
  conclusion?: string;
  approved_by?: string;
  approved_at?: string;
  document_url?: string;
}

export interface RadiologyReport {
  id: string;
  study_number: string;
  study_name: string;
  modality: 'X_RAY' | 'CT_SCAN' | 'MRI' | 'ULTRASOUND' | 'ECHOCARDIOGRAM';
  body_part: string;
  patient: string;
  patient_name: string;
  patient_mrn: string;
  ordering_doctor_name?: string;
  radiologist_name: string;
  study_date: string;
  status: 'ORDERED' | 'CAPTURED' | 'APPROVED';
  clinical_history?: string;
  findings?: string;
  impression?: string;
  key_images?: string[];
  approved_at?: string;
}

export interface PrescriptionItem {
  id?: string;
  medication_name: string;
  dosage: string;
  route: string;
  frequency: string;
  duration_days: number;
  quantity: number;
  instructions: string;
}

export interface Prescription {
  id: string;
  prescription_number: string;
  patient_name: string;
  doctor_name: string;
  status: 'ACTIVE' | 'COMPLETED' | 'DISPENSED' | 'DISCONTINUED';
  issued_date: string;
  valid_until: string;
  special_instructions?: string;
  items: PrescriptionItem[];
}

export interface Allergy {
  id: string;
  allergen: string;
  reaction: string;
  severity: 'MILD' | 'MODERATE' | 'SEVERE';
  identified_date?: string;
}

export interface MedicalHistory {
  id: string;
  condition: string;
  onset_year: number;
  status: string;
  notes?: string;
}

export interface Encounter {
  id: string;
  encounter_number: string;
  appointment?: string;
  patient: string;
  patient_name: string;
  patient_mrn: string;
  doctor: string;
  doctor_name: string;
  doctor_specialization: string;
  encounter_date: string;
  encounter_type: 'OUTPATIENT' | 'TELEMEDICINE' | 'INPATIENT' | 'EMERGENCY';
  status: 'DRAFT' | 'SIGNED' | 'AMENDED';
  chief_complaint: string;
  vitals: {
    bp_systolic?: number;
    bp_diastolic?: number;
    heart_rate?: number;
    temp_c?: number;
    spo2?: number;
    weight_kg?: number;
    height_cm?: number;
    bmi?: number;
  };
  subjective_notes?: string;
  physical_examination?: string;
  assessment?: string;
  clinical_plan?: string;
  signed_by_name?: string;
  signed_at?: string;
  diagnoses?: Diagnosis[];
  prescriptions?: Prescription[];
  created_at: string;
}

export interface Diagnosis {
  id: string;
  icd10_code: string;
  description: string;
  severity: string;
  is_primary: boolean;
  diagnosed_date: string;
}

export interface InvoiceLineItem {
  description: string;
  quantity: number;
  unit_price: number;
  total: number;
}

export interface Payment {
  id: string;
  payment_reference: string;
  receipt_number: string;
  amount: number | string;
  payment_method: string;
  status: string;
  transaction_date: string;
  is_sandbox_simulation: boolean;
  notes?: string;
}

export interface Invoice {
  id: string;
  invoice_number: string;
  patient_name: string;
  patient_mrn: string;
  issue_date: string;
  due_date: string;
  status: 'UNPAID' | 'PARTIALLY_PAID' | 'PAID' | 'VOID';
  subtotal: number | string;
  tax_amount: number | string;
  discount_amount: number | string;
  total_amount: number | string;
  paid_amount: number | string;
  balance_due: number | string;
  line_items: InvoiceLineItem[];
  payments: Payment[];
  notes?: string;
}

export interface TelemedicineSession {
  id: string;
  room_code: string;
  appointment: string;
  appointment_details?: Appointment;
  patient_name: string;
  doctor_name: string;
  status: 'SCHEDULED' | 'WAITING_ROOM' | 'IN_PROGRESS' | 'ENDED' | 'EXPIRED' | 'CANCELLED';
  doctor_present: boolean;
  patient_present: boolean;
  doctor_joined_at?: string;
  patient_joined_at?: string;
  started_at?: string;
  ended_at?: string;
  duration_seconds: number;
  recording_enabled: boolean;
  clinical_quick_notes?: string;
}

export interface Notification {
  id: string;
  recipient: string;
  category: 'APPOINTMENT' | 'CLINICAL' | 'LAB_REPORT' | 'RADIOLOGY' | 'PRESCRIPTION' | 'BILLING' | 'TELEMEDICINE' | 'ANNOUNCEMENT' | 'SYSTEM';
  category_display: string;
  priority: 'LOW' | 'NORMAL' | 'HIGH' | 'URGENT';
  priority_display: string;
  title: string;
  message: string;
  action_url: string;
  is_read: boolean;
  read_at?: string;
  created_at: string;
}
