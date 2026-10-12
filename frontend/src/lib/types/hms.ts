import { HospitalRole, DepartmentType } from './roles';
export * from './clinical';

export interface Patient {
  id: string; // e.g. "PT-10042"
  mrn: string; // Medical Record Number e.g. "MRN-884920"
  firstName: string;
  lastName: string;
  dateOfBirth: string;
  age: number;
  gender: 'Male' | 'Female' | 'Other';
  bloodType: 'A+' | 'A-' | 'B+' | 'B-' | 'AB+' | 'AB-' | 'O+' | 'O-';
  phone: string;
  email: string;
  address: string;
  emergencyContact: {
    name: string;
    relationship: string;
    phone: string;
  };
  allergies: string[];
  chronicConditions: string[];
  assignedDoctorId?: string;
  assignedDoctorName?: string;
  currentWard?: string;
  currentBed?: string;
  admissionStatus: 'Outpatient' | 'Admitted' | 'Discharged' | 'Emergency';
  admissionDate?: string;
  dischargeDate?: string;
  insuranceProvider?: string;
  insurancePolicyNumber?: string;
  hospitalId: string;
}

export interface Doctor {
  id: string; // e.g. "DOC-401"
  userId: string;
  name: string;
  specialty: string;
  department: DepartmentType;
  licenseNumber: string;
  phone: string;
  email: string;
  onDuty: boolean;
  activePatientsCount: number;
  consultingRoom: string;
  rating: number;
}

export interface Nurse {
  id: string;
  userId: string;
  name: string;
  department: DepartmentType;
  assignedWard: string;
  shift: 'Day' | 'Evening' | 'Night';
  licenseNumber: string;
  phone: string;
}

export interface Appointment {
  id: string;
  patientId: string;
  patientName: string;
  patientMrn: string;
  doctorId: string;
  doctorName: string;
  department: DepartmentType;
  date: string;
  time: string;
  type: 'General Consultation' | 'Follow-up' | 'Pre-Op' | 'Emergency Review' | 'Specialist Consultation';
  status: 'Scheduled' | 'In Progress' | 'Completed' | 'Cancelled' | 'No Show';
  symptoms: string;
  priority: 'Routine' | 'Urgent' | 'Emergency';
  roomNumber: string;
}

export interface AdmissionRecord {
  id: string;
  patientId: string;
  patientName: string;
  mrn: string;
  admittingDoctorId: string;
  admittingDoctorName: string;
  department: DepartmentType;
  ward: string;
  bed: string;
  admissionDate: string;
  expectedDischargeDate?: string;
  actualDischargeDate?: string;
  reasonForAdmission: string;
  diagnosis: string;
  status: 'Admitted' | 'Discharge Pending' | 'Discharged';
}

export interface Bed {
  id: string;
  bedNumber: string;
  ward: string;
  department: DepartmentType;
  type: 'ICU' | 'Standard' | 'Semi-Private' | 'Isolation' | 'Pediatric' | 'Emergency Bay';
  status: 'Available' | 'Occupied' | 'Maintenance' | 'Reserved';
  patientId?: string;
  patientName?: string;
}

export interface Prescription {
  id: string;
  patientId: string;
  patientName: string;
  doctorId: string;
  doctorName: string;
  date: string;
  medications: {
    medicineId: string;
    name: string;
    dosage: string;
    frequency: string;
    duration: string;
    instructions: string;
    dispensedStatus: 'Pending' | 'Dispensed' | 'Substituted' | 'Cancelled';
  }[];
  clinicalDiagnosis: string;
  status: 'Pending' | 'Partially Dispensed' | 'Dispensed' | 'Cancelled';
}

export interface Medicine {
  id: string;
  brandName: string;
  genericName: string;
  category: 'Antibiotic' | 'Cardiovascular' | 'Analgesic' | 'Antidiabetic' | 'Anticoagulant' | 'Psychiatric' | 'Respiratory' | 'Steroid' | 'Emergency';
  dosageForm: 'Tablet' | 'Capsule' | 'IV Injection' | 'Syrup' | 'Inhaler' | 'Ointment';
  strength: string;
  stockQuantity: number;
  reorderLevel: number;
  unitPrice: number;
  batchNumber: string;
  expiryDate: string;
  storageRequirement: 'Room Temperature (15-25°C)' | 'Refrigerated (2-8°C)' | 'Controlled Room Temp' | 'Strict Cold Chain (-20°C)';
  controlledDrug: boolean;
  manufacturer: string;
}

export interface LabTest {
  id: string;
  orderNumber: string;
  patientId: string;
  patientName: string;
  patientMrn: string;
  doctorId: string;
  doctorName: string;
  testName: string;
  category: 'Hematology' | 'Biochemistry' | 'Microbiology' | 'Immunology' | 'Urinalysis' | 'Pathology';
  status: 'Ordered' | 'Sample Collected' | 'Analyzing' | 'Completed' | 'Critical Review';
  orderDate: string;
  collectionDate?: string;
  resultDate?: string;
  results?: {
    parameter: string;
    value: string;
    unit: string;
    referenceRange: string;
    flag?: 'Normal' | 'High' | 'Low' | 'Critical High' | 'Critical Low';
  }[];
  isCritical: boolean;
  technicianNotes?: string;
}

export interface RadiologyScan {
  id: string;
  accessionNumber: string;
  patientId: string;
  patientName: string;
  doctorId: string;
  doctorName: string;
  modality: 'X-Ray' | 'CT Scan' | 'MRI' | 'Ultrasound' | 'PET-CT';
  anatomy: 'Chest' | 'Brain' | 'Abdomen & Pelvis' | 'Spine' | 'Extremity' | 'Cardiac';
  status: 'Scheduled' | 'In Scanning' | 'Awaiting Report' | 'Report Verified';
  scheduledTime: string;
  radiologistName?: string;
  findings?: string;
  impression?: string;
  priority: 'Routine' | 'Urgent' | 'Stat (Emergency)';
}

export interface Invoice {
  id: string;
  invoiceNumber: string;
  patientId: string;
  patientName: string;
  mrn: string;
  issueDate: string;
  dueDate: string;
  items: {
    description: string;
    category: 'Consultation' | 'Bed Charges' | 'Pharmacy' | 'Laboratory' | 'Radiology' | 'Procedure' | 'Surgery';
    amount: number;
  }[];
  subtotal: number;
  tax: number;
  insuranceDiscount: number;
  totalAmount: number;
  amountPaid: number;
  outstandingBalance: number;
  status: 'Paid' | 'Partially Paid' | 'Pending' | 'Overdue' | 'Claim Processing';
}

export interface InsuranceClaim {
  id: string;
  claimNumber: string;
  invoiceId: string;
  patientId: string;
  patientName: string;
  provider: 'Blue Cross Shield' | 'Aetna Health' | 'UnitedHealthcare' | 'Cigna Global' | 'Medicare' | 'MetLife Care';
  policyNumber: string;
  claimedAmount: number;
  approvedAmount?: number;
  status: 'Submitted' | 'Under Review' | 'Pre-Authorized' | 'Approved' | 'Partially Approved' | 'Rejected';
  submissionDate: string;
  adjudicationDate?: string;
  denialReason?: string;
  treatmentCode: string;
}

export interface EmergencyCase {
  id: string;
  patientName: string;
  age: number;
  gender: string;
  triageLevel: 'ESI-1 Resuscitation (Immediate)' | 'ESI-2 Emergent (<15m)' | 'ESI-3 Urgent (<30m)' | 'ESI-4 Less Urgent' | 'ESI-5 Non-urgent';
  vitals: {
    bp: string;
    heartRate: number;
    spo2: number;
    temp: number;
    respRate: number;
  };
  chiefComplaint: string;
  arrivalTime: string;
  assignedBay: string;
  assignedDoctor: string;
  assignedNurse: string;
  status: 'Triage Pending' | 'Under Evaluation' | 'Stabilizing' | 'Admitted to ICU' | 'Transferred to OR' | 'Discharged';
}

export interface AuditLogEntry {
  id: string;
  userId: string;
  userName: string;
  role: HospitalRole;
  action: 'VIEW' | 'CREATE' | 'UPDATE' | 'DELETE' | 'DISPENSE' | 'RAG_QUERY' | 'DOCUMENT_ACCESS' | 'LOGIN' | 'LOGOUT';
  resourceType: 'PATIENT' | 'DOCUMENT' | 'RAG_KB' | 'PRESCRIPTION' | 'BILLING' | 'LAB_REPORT' | 'SECURITY';
  resourceId?: string;
  patientId?: string;
  details: string;
  timestamp: string;
  ipAddress: string;
  hospitalId: string;
}

export interface NotificationItem {
  id: string;
  targetRole?: HospitalRole;
  userId?: string;
  type: 'APPOINTMENT' | 'LAB_RESULT' | 'CRITICAL_ALERT' | 'MED_RESTOCK' | 'INSURANCE_CLAIM' | 'POLICY_UPDATE';
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
  severity: 'info' | 'warning' | 'urgent';
  actionUrl?: string;
}
