export type HospitalRole =
  | 'SUPER_ADMIN'
  | 'HOSPITAL_ADMIN'
  | 'DOCTOR'
  | 'NURSE'
  | 'RECEPTIONIST'
  | 'PATIENT'
  | 'PHARMACIST'
  | 'LABORATORY_STAFF'
  | 'RADIOLOGY_STAFF'
  | 'BILLING_STAFF'
  | 'INSURANCE_STAFF'
  | 'HR_STAFF'
  | 'DEPARTMENT_MANAGER'
  | 'MANAGEMENT_EXECUTIVE'
  | 'EMERGENCY_STAFF';

export type DepartmentType =
  | 'Cardiology'
  | 'Neurology'
  | 'Emergency'
  | 'Oncology'
  | 'Pediatrics'
  | 'Orthopedics'
  | 'General Surgery'
  | 'Intensive Care Unit (ICU)'
  | 'Internal Medicine'
  | 'Radiology'
  | 'Pathology & Laboratory'
  | 'Pharmacy'
  | 'Billing & Finance'
  | 'Insurance Services'
  | 'Human Resources'
  | 'Hospital Administration'
  | 'Executive Board'
  | 'Outpatient Department';

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: HospitalRole;
  department: DepartmentType;
  avatar?: string;
  employeeId?: string;
  licenseNumber?: string;
  patientId?: string; // For patient role
  assignedPatients?: string[]; // IDs of assigned patients
  hospitalId: string;
  hospitalName: string;
  shift?: 'Day' | 'Evening' | 'Night' | 'On-Call';
}

export type Permission =
  | 'read:all_patients'
  | 'read:assigned_patients'
  | 'read:own_patient_record'
  | 'write:patient_records'
  | 'write:clinical_notes'
  | 'write:prescriptions'
  | 'dispense:prescriptions'
  | 'execute:lab_tests'
  | 'execute:radiology_scans'
  | 'manage:billing'
  | 'manage:insurance_claims'
  | 'manage:employees'
  | 'manage:departments'
  | 'manage:system'
  | 'manage:documents'
  | 'query:rag_clinical'
  | 'query:rag_pharmacy'
  | 'query:rag_lab'
  | 'query:rag_radiology'
  | 'query:rag_billing'
  | 'query:rag_insurance'
  | 'query:rag_hr'
  | 'query:rag_admin'
  | 'query:rag_emergency'
  | 'query:rag_patient'
  | 'query:rag_executive';
