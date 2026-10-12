import { 
  Patient, Doctor, Nurse, Appointment, AdmissionRecord, Bed, 
  Prescription, Medicine, LabTest, RadiologyScan, Invoice, 
  InsuranceClaim, EmergencyCase, AuditLogEntry, NotificationItem 
} from '../types/hms';
import { DepartmentType, HospitalRole, UserProfile } from '../types/roles';

// 15 Departments
export const DEPARTMENTS: { name: DepartmentType; head: string; floor: string; bedCapacity: number }[] = [
  { name: 'Cardiology', head: 'Dr. Marcus Vance, MD, FACC', floor: 'Wing B, Floor 3', bedCapacity: 45 },
  { name: 'Neurology', head: 'Dr. Sarah Lin, MD, PhD', floor: 'Wing C, Floor 4', bedCapacity: 30 },
  { name: 'Emergency', head: 'Dr. Robert Thorne, MD, FACEP', floor: 'Ground Floor, Trauma Bay', bedCapacity: 40 },
  { name: 'Oncology', head: 'Dr. David Reynolds, MD', floor: 'Wing D, Floor 5', bedCapacity: 35 },
  { name: 'Pediatrics', head: 'Dr. Emily Watson, MD, FAAP', floor: 'Wing A, Floor 2', bedCapacity: 50 },
  { name: 'Orthopedics', head: 'Dr. James Mitchell, MD', floor: 'Wing B, Floor 2', bedCapacity: 40 },
  { name: 'General Surgery', head: 'Dr. Anthony Rossi, MD, FACS', floor: 'Surgical Tower, Floor 4', bedCapacity: 55 },
  { name: 'Intensive Care Unit (ICU)', head: 'Dr. Rachel Green, MD, FCCM', floor: 'Critical Tower, Floor 2', bedCapacity: 28 },
  { name: 'Internal Medicine', head: 'Dr. Thomas Hayes, MD, FACP', floor: 'Wing C, Floor 3', bedCapacity: 60 },
  { name: 'Radiology', head: 'Dr. Jonathan Blake, MD', floor: 'Basement Level 1', bedCapacity: 10 },
  { name: 'Pathology & Laboratory', head: 'Dr. Karen White, MD, FCAP', floor: 'Basement Level 2', bedCapacity: 5 },
  { name: 'Pharmacy', head: 'PharmD. Samuel Miller, RPh', floor: 'Ground Floor Main Atrium', bedCapacity: 0 },
  { name: 'Billing & Finance', head: 'Claire Henderson, MBA', floor: 'Admin Annex, Floor 2', bedCapacity: 0 },
  { name: 'Insurance Services', head: 'Michael Chang, CPA', floor: 'Admin Annex, Floor 2', bedCapacity: 0 },
  { name: 'Human Resources', head: 'Eleanor Davis, SPHR', floor: 'Executive Suite, Floor 6', bedCapacity: 0 },
  { name: 'Hospital Administration', head: 'Dr. Arthur Pendelton, CEO', floor: 'Executive Suite, Floor 6', bedCapacity: 0 },
  { name: 'Executive Board', head: 'Board of Governors', floor: 'Executive Suite, Floor 7', bedCapacity: 0 },
  { name: 'Outpatient Department', head: 'Dr. Lisa Morales, MD', floor: 'Ambulatory Pavilion', bedCapacity: 20 },
];

// Sample Initial Users for quick role-switching / testing
export const DEMO_USERS: Record<HospitalRole, UserProfile> = {
  SUPER_ADMIN: {
    id: 'USR-SA-01',
    name: 'Alexander Sterling',
    email: 'superadmin@hopkins-health.org',
    role: 'SUPER_ADMIN',
    department: 'Hospital Administration',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'EMP-0001'
  },
  HOSPITAL_ADMIN: {
    id: 'USR-HA-02',
    name: 'Dr. Arthur Pendelton',
    email: 'admin@hopkins-health.org',
    role: 'HOSPITAL_ADMIN',
    department: 'Hospital Administration',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'EMP-0010'
  },
  DOCTOR: {
    id: 'USR-DOC-03',
    name: 'Dr. Marcus Vance, MD',
    email: 'marcus.vance@hopkins-health.org',
    role: 'DOCTOR',
    department: 'Cardiology',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'DOC-401',
    licenseNumber: 'MD-88392-CA',
    assignedPatients: ['PT-10023', 'PT-10045', 'PT-10089', 'PT-10112'],
    shift: 'Day'
  },
  NURSE: {
    id: 'USR-NUR-04',
    name: 'Sarah Jenkins, BSN, RN',
    email: 'sarah.jenkins@hopkins-health.org',
    role: 'NURSE',
    department: 'Cardiology',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'NUR-204',
    licenseNumber: 'RN-99201-CA',
    assignedPatients: ['PT-10023', 'PT-10045'],
    shift: 'Day'
  },
  RECEPTIONIST: {
    id: 'USR-REC-05',
    name: 'Jessica Gomez',
    email: 'reception@hopkins-health.org',
    role: 'RECEPTIONIST',
    department: 'Outpatient Department',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'REC-102',
    shift: 'Day'
  },
  PATIENT: {
    id: 'USR-PT-06',
    name: 'John Anderson',
    email: 'john.anderson@patient.org',
    role: 'PATIENT',
    department: 'Cardiology',
    patientId: 'PT-10023',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center'
  },
  PHARMACIST: {
    id: 'USR-PH-07',
    name: 'Dr. Samuel Miller, PharmD',
    email: 'samuel.miller@hopkins-health.org',
    role: 'PHARMACIST',
    department: 'Pharmacy',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'PH-302',
    licenseNumber: 'RPH-77401-CA',
    shift: 'Day'
  },
  LABORATORY_STAFF: {
    id: 'USR-LAB-08',
    name: 'David Chen, MLS (ASCP)',
    email: 'david.chen@hopkins-health.org',
    role: 'LABORATORY_STAFF',
    department: 'Pathology & Laboratory',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'LAB-503',
    licenseNumber: 'MLS-33019',
    shift: 'Day'
  },
  RADIOLOGY_STAFF: {
    id: 'USR-RAD-09',
    name: 'Dr. Jonathan Blake, MD',
    email: 'jonathan.blake@hopkins-health.org',
    role: 'RADIOLOGY_STAFF',
    department: 'Radiology',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'RAD-601',
    licenseNumber: 'MD-55209-CA',
    shift: 'Day'
  },
  BILLING_STAFF: {
    id: 'USR-BIL-10',
    name: 'Claire Henderson',
    email: 'claire.h@hopkins-health.org',
    role: 'BILLING_STAFF',
    department: 'Billing & Finance',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'BIL-701'
  },
  INSURANCE_STAFF: {
    id: 'USR-INS-11',
    name: 'Michael Chang',
    email: 'michael.chang@hopkins-health.org',
    role: 'INSURANCE_STAFF',
    department: 'Insurance Services',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'INS-802'
  },
  HR_STAFF: {
    id: 'USR-HR-12',
    name: 'Eleanor Davis, SPHR',
    email: 'eleanor.davis@hopkins-health.org',
    role: 'HR_STAFF',
    department: 'Human Resources',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'HR-901'
  },
  DEPARTMENT_MANAGER: {
    id: 'USR-DM-13',
    name: 'Dr. Gregory House, Clinical Chief',
    email: 'gregory.house@hopkins-health.org',
    role: 'DEPARTMENT_MANAGER',
    department: 'Internal Medicine',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'MGR-101'
  },
  MANAGEMENT_EXECUTIVE: {
    id: 'USR-EXEC-14',
    name: 'Victoria Hastings, COO',
    email: 'victoria.hastings@hopkins-health.org',
    role: 'MANAGEMENT_EXECUTIVE',
    department: 'Executive Board',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'EXEC-002'
  },
  EMERGENCY_STAFF: {
    id: 'USR-ED-15',
    name: 'Dr. Robert Thorne, MD',
    email: 'robert.thorne@hopkins-health.org',
    role: 'EMERGENCY_STAFF',
    department: 'Emergency',
    hospitalId: 'HOSP-01',
    hospitalName: 'St. Jude Metropolitan Medical Center',
    employeeId: 'ED-112',
    licenseNumber: 'MD-99120-CA',
    shift: 'Day'
  }
};

// Realistic Seed Patients
export const SEED_PATIENTS: Patient[] = [
  {
    id: 'PT-10023',
    mrn: 'MRN-884920',
    firstName: 'John',
    lastName: 'Anderson',
    dateOfBirth: '1968-05-14',
    age: 58,
    gender: 'Male',
    bloodType: 'A+',
    phone: '+1 (555) 234-8891',
    email: 'john.anderson@patient.org',
    address: '742 Evergreen Terrace, San Francisco, CA',
    emergencyContact: {
      name: 'Mary Anderson',
      relationship: 'Spouse',
      phone: '+1 (555) 234-8892'
    },
    allergies: ['Penicillin', 'Shellfish'],
    chronicConditions: ['Coronary Artery Disease', 'Hypertension', 'Type 2 Diabetes'],
    assignedDoctorId: 'DOC-401',
    assignedDoctorName: 'Dr. Marcus Vance, MD',
    currentWard: 'Cardiac Step-Down',
    currentBed: 'Bed 304-B',
    admissionStatus: 'Admitted',
    admissionDate: '2026-10-01',
    insuranceProvider: 'Blue Cross Shield',
    insurancePolicyNumber: 'BCS-9920192',
    hospitalId: 'HOSP-01'
  },
  {
    id: 'PT-10045',
    mrn: 'MRN-449182',
    firstName: 'Elena',
    lastName: 'Rostova',
    dateOfBirth: '1984-11-20',
    age: 41,
    gender: 'Female',
    bloodType: 'O-',
    phone: '+1 (555) 839-1120',
    email: 'elena.rostova@mail.com',
    address: '104 Ocean View Blvd, San Francisco, CA',
    emergencyContact: {
      name: 'Igor Rostov',
      relationship: 'Brother',
      phone: '+1 (555) 839-1121'
    },
    allergies: ['Sulfa Drugs', 'Codeine'],
    chronicConditions: ['Asthma'],
    assignedDoctorId: 'DOC-401',
    assignedDoctorName: 'Dr. Marcus Vance, MD',
    currentWard: 'General Medical Ward 2',
    currentBed: 'Bed 212-A',
    admissionStatus: 'Admitted',
    admissionDate: '2026-10-02',
    insuranceProvider: 'Aetna Health',
    insurancePolicyNumber: 'AET-3301982',
    hospitalId: 'HOSP-01'
  },
  {
    id: 'PT-10089',
    mrn: 'MRN-192083',
    firstName: 'Marcus',
    lastName: 'Vance-Carter',
    dateOfBirth: '1992-03-12',
    age: 34,
    gender: 'Male',
    bloodType: 'B+',
    phone: '+1 (555) 472-9901',
    email: 'marcus.vc@mail.com',
    address: '350 Mission St, San Francisco, CA',
    emergencyContact: {
      name: 'Chloe Carter',
      relationship: 'Partner',
      phone: '+1 (555) 472-9902'
    },
    allergies: ['None known (NKDA)'],
    chronicConditions: ['None'],
    assignedDoctorId: 'DOC-401',
    assignedDoctorName: 'Dr. Marcus Vance, MD',
    admissionStatus: 'Outpatient',
    insuranceProvider: 'UnitedHealthcare',
    insurancePolicyNumber: 'UHC-8812903',
    hospitalId: 'HOSP-01'
  },
  {
    id: 'PT-10112',
    mrn: 'MRN-773910',
    firstName: 'Sophia',
    lastName: 'Martinez',
    dateOfBirth: '1955-08-30',
    age: 71,
    gender: 'Female',
    bloodType: 'AB+',
    phone: '+1 (555) 612-4433',
    email: 'sophia.m@mail.com',
    address: '120 Valencia St, San Francisco, CA',
    emergencyContact: {
      name: 'Carlos Martinez',
      relationship: 'Son',
      phone: '+1 (555) 612-4434'
    },
    allergies: ['Latex', 'NSAIDs (Aspirin/Ibuprofen)'],
    chronicConditions: ['Atrial Fibrillation', 'Osteoarthritis', 'Chronic Kidney Disease Stage 3'],
    assignedDoctorId: 'DOC-401',
    assignedDoctorName: 'Dr. Marcus Vance, MD',
    currentWard: 'Intensive Care Unit (ICU)',
    currentBed: 'ICU Bay 06',
    admissionStatus: 'Admitted',
    admissionDate: '2026-10-03',
    insuranceProvider: 'Medicare',
    insurancePolicyNumber: 'MED-1002931',
    hospitalId: 'HOSP-01'
  }
];

// Helper to generate up to 500 realistic patients for the enterprise scale requirement
export function generateEnterprisePatients(): Patient[] {
  const firstNames = ['James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 'Michael', 'Linda', 'David', 'Elizabeth', 'William', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen'];
  const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin'];
  const bloodTypes: ('A+' | 'A-' | 'B+' | 'B-' | 'AB+' | 'AB-' | 'O+' | 'O-')[] = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];
  const providers = ['Blue Cross Shield', 'Aetna Health', 'UnitedHealthcare', 'Cigna Global', 'Medicare', 'MetLife Care'];

  const patients: Patient[] = [...SEED_PATIENTS];

  for (let i = 5; i <= 520; i++) {
    const fn = firstNames[i % firstNames.length];
    const ln = lastNames[(i * 3) % lastNames.length];
    const age = 18 + (i * 7) % 75;
    const isAdmitted = i % 5 === 0;

    patients.push({
      id: `PT-${10000 + i}`,
      mrn: `MRN-${900000 + i}`,
      firstName: fn,
      lastName: ln,
      dateOfBirth: `19${90 - Math.floor(age / 2)}-0${(i % 9) + 1}-15`,
      age,
      gender: i % 2 === 0 ? 'Male' : 'Female',
      bloodType: bloodTypes[i % bloodTypes.length],
      phone: `+1 (555) ${100 + (i % 899)}-${1000 + (i % 8999)}`,
      email: `${fn.toLowerCase()}.${ln.toLowerCase()}${i}@patientmail.org`,
      address: `${100 + i} Medical Blvd, Suite ${(i % 20) + 1}`,
      emergencyContact: {
        name: `Relative of ${fn}`,
        relationship: 'Family Member',
        phone: `+1 (555) 999-${1000 + i}`
      },
      allergies: i % 4 === 0 ? ['Penicillin'] : i % 7 === 0 ? ['Sulfa'] : ['NKDA'],
      chronicConditions: i % 3 === 0 ? ['Hypertension'] : i % 6 === 0 ? ['Type 2 Diabetes'] : ['None'],
      assignedDoctorId: `DOC-${401 + (i % 12)}`,
      assignedDoctorName: `Dr. Specialist ${((i % 12) + 1)}`,
      admissionStatus: isAdmitted ? 'Admitted' : 'Outpatient',
      currentWard: isAdmitted ? `Ward ${(i % 5) + 1}` : undefined,
      currentBed: isAdmitted ? `Bed ${100 + (i % 20)}` : undefined,
      admissionDate: isAdmitted ? '2026-10-02' : undefined,
      insuranceProvider: providers[i % providers.length],
      insurancePolicyNumber: `POL-${800000 + i}`,
      hospitalId: 'HOSP-01'
    });
  }

  return patients;
}

// 50+ Doctors across all departments
export const DOCTORS: Doctor[] = [
  { id: 'DOC-401', userId: 'USR-DOC-03', name: 'Dr. Marcus Vance, MD', specialty: 'Interventional Cardiology', department: 'Cardiology', licenseNumber: 'MD-88392-CA', phone: '+1 (555) 401-0001', email: 'marcus.vance@hopkins-health.org', onDuty: true, activePatientsCount: 14, consultingRoom: 'Room 310, Wing B', rating: 4.9 },
  { id: 'DOC-402', userId: 'USR-DOC-04', name: 'Dr. Sarah Lin, MD, PhD', specialty: 'Vascular Neurology & Stroke', department: 'Neurology', licenseNumber: 'MD-77192-CA', phone: '+1 (555) 401-0002', email: 'sarah.lin@hopkins-health.org', onDuty: true, activePatientsCount: 11, consultingRoom: 'Room 412, Wing C', rating: 4.95 },
  { id: 'DOC-403', userId: 'USR-DOC-05', name: 'Dr. Robert Thorne, MD', specialty: 'Emergency & Trauma Medicine', department: 'Emergency', licenseNumber: 'MD-99120-CA', phone: '+1 (555) 401-0003', email: 'robert.thorne@hopkins-health.org', onDuty: true, activePatientsCount: 22, consultingRoom: 'Trauma Bay 1', rating: 4.8 },
  { id: 'DOC-404', userId: 'USR-DOC-06', name: 'Dr. David Reynolds, MD', specialty: 'Medical Oncology', department: 'Oncology', licenseNumber: 'MD-66291-CA', phone: '+1 (555) 401-0004', email: 'david.reynolds@hopkins-health.org', onDuty: false, activePatientsCount: 8, consultingRoom: 'Room 501, Wing D', rating: 4.7 },
  { id: 'DOC-405', userId: 'USR-DOC-07', name: 'Dr. Emily Watson, MD', specialty: 'Pediatric Critical Care', department: 'Pediatrics', licenseNumber: 'MD-44391-CA', phone: '+1 (555) 401-0005', email: 'emily.watson@hopkins-health.org', onDuty: true, activePatientsCount: 9, consultingRoom: 'Room 205, Wing A', rating: 5.0 },
  { id: 'DOC-406', userId: 'USR-DOC-08', name: 'Dr. James Mitchell, MD', specialty: 'Orthopedic Joint Reconstruction', department: 'Orthopedics', licenseNumber: 'MD-55891-CA', phone: '+1 (555) 401-0006', email: 'james.mitchell@hopkins-health.org', onDuty: true, activePatientsCount: 16, consultingRoom: 'Room 220, Wing B', rating: 4.85 },
  { id: 'DOC-407', userId: 'USR-DOC-09', name: 'Dr. Anthony Rossi, MD', specialty: 'Minimally Invasive General Surgery', department: 'General Surgery', licenseNumber: 'MD-33291-CA', phone: '+1 (555) 401-0007', email: 'anthony.rossi@hopkins-health.org', onDuty: true, activePatientsCount: 18, consultingRoom: 'OR Suite 4', rating: 4.9 },
  { id: 'DOC-408', userId: 'USR-DOC-10', name: 'Dr. Rachel Green, MD', specialty: 'Intensive Critical Care Medicine', department: 'Intensive Care Unit (ICU)', licenseNumber: 'MD-22191-CA', phone: '+1 (555) 401-0008', email: 'rachel.green@hopkins-health.org', onDuty: true, activePatientsCount: 12, consultingRoom: 'ICU Station Central', rating: 4.95 },
  { id: 'DOC-409', userId: 'USR-DOC-11', name: 'Dr. Thomas Hayes, MD', specialty: 'Internal Medicine & Geriatrics', department: 'Internal Medicine', licenseNumber: 'MD-11991-CA', phone: '+1 (555) 401-0009', email: 'thomas.hayes@hopkins-health.org', onDuty: true, activePatientsCount: 20, consultingRoom: 'Room 315, Wing C', rating: 4.75 },
];
export const SAMPLE_DOCTORS = DOCTORS;

export const SAMPLE_APPOINTMENTS: Appointment[] = [
  { id: 'APT-101', patientId: 'PT-10023', patientName: 'John Anderson', patientMrn: 'MRN-884920', doctorId: 'DOC-401', doctorName: 'Dr. Marcus Vance, MD', department: 'Cardiology', date: '2026-10-04', time: '09:30 AM', type: 'Specialist Consultation', status: 'In Progress', symptoms: 'Post-stenting chest follow-up', priority: 'Urgent', roomNumber: 'Room 310, Wing B' },
  { id: 'APT-102', patientId: 'PT-10045', patientName: 'Elena Rostova', patientMrn: 'MRN-449182', doctorId: 'DOC-401', doctorName: 'Dr. Marcus Vance, MD', department: 'Cardiology', date: '2026-10-04', time: '10:45 AM', type: 'Follow-up', status: 'Scheduled', symptoms: 'Dyspnea upon moderate exertion', priority: 'Routine', roomNumber: 'Room 310, Wing B' },
  { id: 'APT-103', patientId: 'PT-10089', patientName: 'Marcus Vance-Carter', patientMrn: 'MRN-192083', doctorId: 'DOC-401', doctorName: 'Dr. Marcus Vance, MD', department: 'Cardiology', date: '2026-10-04', time: '02:15 PM', type: 'General Consultation', status: 'Scheduled', symptoms: 'Routine annual cardiovascular screening', priority: 'Routine', roomNumber: 'Room 310, Wing B' },
  { id: 'APT-104', patientId: 'PT-10112', patientName: 'Sophia Martinez', patientMrn: 'MRN-773910', doctorId: 'DOC-408', doctorName: 'Dr. Rachel Green, MD', department: 'Intensive Care Unit (ICU)', date: '2026-10-04', time: '11:00 AM', type: 'Emergency Review', status: 'In Progress', symptoms: 'Sepsis escalation and ICU bedside round', priority: 'Emergency', roomNumber: 'ICU Bay 06' },
];

// Hospital Beds
export const HOSPITAL_BEDS: Bed[] = [
  { id: 'BED-101', bedNumber: 'Bed 304-A', ward: 'Cardiac Step-Down', department: 'Cardiology', type: 'Telemetry' as any, status: 'Available' },
  { id: 'BED-102', bedNumber: 'Bed 304-B', ward: 'Cardiac Step-Down', department: 'Cardiology', type: 'Telemetry' as any, status: 'Occupied', patientId: 'PT-10023', patientName: 'John Anderson' },
  { id: 'BED-103', bedNumber: 'Bed 212-A', ward: 'General Medical Ward 2', department: 'Internal Medicine', type: 'Standard', status: 'Occupied', patientId: 'PT-10045', patientName: 'Elena Rostova' },
  { id: 'BED-104', bedNumber: 'Bed 212-B', ward: 'General Medical Ward 2', department: 'Internal Medicine', type: 'Standard', status: 'Available' },
  { id: 'BED-105', bedNumber: 'ICU Bay 01', ward: 'Intensive Care Unit (ICU)', department: 'Intensive Care Unit (ICU)', type: 'ICU', status: 'Occupied', patientName: 'Robert Vance' },
  { id: 'BED-106', bedNumber: 'ICU Bay 02', ward: 'Intensive Care Unit (ICU)', department: 'Intensive Care Unit (ICU)', type: 'ICU', status: 'Available' },
  { id: 'BED-107', bedNumber: 'ICU Bay 06', ward: 'Intensive Care Unit (ICU)', department: 'Intensive Care Unit (ICU)', type: 'ICU', status: 'Occupied', patientId: 'PT-10112', patientName: 'Sophia Martinez' },
  { id: 'BED-108', bedNumber: 'Trauma Bay 1', ward: 'Emergency Trauma', department: 'Emergency', type: 'Emergency Bay', status: 'Occupied', patientName: 'Stat Arrival (MVA)' },
  { id: 'BED-109', bedNumber: 'Trauma Bay 2', ward: 'Emergency Trauma', department: 'Emergency', type: 'Emergency Bay', status: 'Available' },
  { id: 'BED-110', bedNumber: 'Trauma Bay 3', ward: 'Emergency Trauma', department: 'Emergency', type: 'Emergency Bay', status: 'Available' },
  { id: 'BED-111', bedNumber: 'Pediatric Bed 04', ward: 'Pediatric Ward', department: 'Pediatrics', type: 'Pediatric', status: 'Occupied', patientName: 'Liam Chen' },
  { id: 'BED-112', bedNumber: 'Pediatric Bed 05', ward: 'Pediatric Ward', department: 'Pediatrics', type: 'Pediatric', status: 'Available' },
];

// Prescriptions
export const SAMPLE_PRESCRIPTIONS: Prescription[] = [
  {
    id: 'RX-9901',
    patientId: 'PT-10023',
    patientName: 'John Anderson',
    doctorId: 'DOC-401',
    doctorName: 'Dr. Marcus Vance, MD',
    date: '2026-10-02',
    clinicalDiagnosis: 'Acute Coronary Syndrome post DES stenting of LAD',
    status: 'Dispensed',
    medications: [
      { medicineId: 'MED-001', name: 'Aspirin EC', dosage: '81 mg', frequency: 'Once daily oral', duration: 'Lifetime', instructions: 'Take with food in morning', dispensedStatus: 'Dispensed' },
      { medicineId: 'MED-002', name: 'Ticagrelor (Brilinta)', dosage: '90 mg', frequency: 'Twice daily oral', duration: '12 Months', instructions: 'Do not discontinue without cardiologist approval', dispensedStatus: 'Dispensed' },
      { medicineId: 'MED-003', name: 'Atorvastatin (Lipitor)', dosage: '80 mg', frequency: 'Once daily at bedtime', duration: 'Long term', instructions: 'Take at night', dispensedStatus: 'Dispensed' },
      { medicineId: 'MED-004', name: 'Metoprolol Tartrate', dosage: '25 mg', frequency: 'Twice daily oral', duration: 'Ongoing', instructions: 'Monitor heart rate and blood pressure', dispensedStatus: 'Dispensed' },
    ]
  },
  {
    id: 'RX-9902',
    patientId: 'PT-10045',
    patientName: 'Elena Rostova',
    doctorId: 'DOC-401',
    doctorName: 'Dr. Marcus Vance, MD',
    date: '2026-10-03',
    clinicalDiagnosis: 'Exacerbation of Asthma / Bronchospasm',
    status: 'Pending',
    medications: [
      { medicineId: 'MED-010', name: 'Albuterol Sulfate Inhaler', dosage: '90 mcg/actuation', frequency: '2 puffs Q4H PRN', duration: '30 Days', instructions: 'Use spacer device; rinse mouth after use', dispensedStatus: 'Pending' },
      { medicineId: 'MED-011', name: 'Prednisone Oral', dosage: '40 mg', frequency: 'Once daily with breakfast', duration: '5 Days taper', instructions: 'Take with full glass of water', dispensedStatus: 'Pending' },
    ]
  }
];

// Medicines Inventory
export const MEDICINES_INVENTORY: Medicine[] = [
  { id: 'MED-001', brandName: 'Aspirin Cardio', genericName: 'Acetylsalicylic Acid EC', category: 'Cardiovascular', dosageForm: 'Tablet', strength: '81 mg', stockQuantity: 4200, reorderLevel: 500, unitPrice: 0.15, batchNumber: 'BAT-ASP-2026', expiryDate: '2028-04-30', storageRequirement: 'Room Temperature (15-25°C)', controlledDrug: false, manufacturer: 'Bayer Healthcare' },
  { id: 'MED-002', brandName: 'Brilinta', genericName: 'Ticagrelor', category: 'Cardiovascular', dosageForm: 'Tablet', strength: '90 mg', stockQuantity: 840, reorderLevel: 200, unitPrice: 6.80, batchNumber: 'BAT-TIC-8831', expiryDate: '2027-11-15', storageRequirement: 'Room Temperature (15-25°C)', controlledDrug: false, manufacturer: 'AstraZeneca' },
  { id: 'MED-003', brandName: 'Lipitor', genericName: 'Atorvastatin Calcium', category: 'Cardiovascular', dosageForm: 'Tablet', strength: '80 mg', stockQuantity: 1650, reorderLevel: 300, unitPrice: 1.25, batchNumber: 'BAT-ATO-9901', expiryDate: '2028-01-10', storageRequirement: 'Room Temperature (15-25°C)', controlledDrug: false, manufacturer: 'Pfizer' },
  { id: 'MED-004', brandName: 'Lopressor', genericName: 'Metoprolol Tartrate', category: 'Cardiovascular', dosageForm: 'Tablet', strength: '25 mg', stockQuantity: 2200, reorderLevel: 400, unitPrice: 0.40, batchNumber: 'BAT-MET-1120', expiryDate: '2027-09-20', storageRequirement: 'Room Temperature (15-25°C)', controlledDrug: false, manufacturer: 'Novartis' },
  { id: 'MED-005', brandName: 'Lovenox', genericName: 'Enoxaparin Sodium', category: 'Anticoagulant', dosageForm: 'IV Injection', strength: '40 mg / 0.4 mL', stockQuantity: 340, reorderLevel: 100, unitPrice: 28.50, batchNumber: 'BAT-ENOX-441', expiryDate: '2027-06-18', storageRequirement: 'Room Temperature (15-25°C)', controlledDrug: false, manufacturer: 'Sanofi' },
  { id: 'MED-006', brandName: 'Humalog U-100', genericName: 'Insulin Lispro recombinant', category: 'Antidiabetic', dosageForm: 'IV Injection', strength: '100 units/mL (10mL vial)', stockQuantity: 180, reorderLevel: 50, unitPrice: 52.00, batchNumber: 'BAT-INS-8812', expiryDate: '2027-03-30', storageRequirement: 'Refrigerated (2-8°C)', controlledDrug: false, manufacturer: 'Eli Lilly' },
  { id: 'MED-007', brandName: 'Sublimaze', genericName: 'Fentanyl Citrate', category: 'Analgesic', dosageForm: 'IV Injection', strength: '100 mcg / 2 mL', stockQuantity: 45, reorderLevel: 30, unitPrice: 14.00, batchNumber: 'BAT-FENT-009', expiryDate: '2027-08-12', storageRequirement: 'Controlled Room Temp', controlledDrug: true, manufacturer: 'Hospira' },
  { id: 'MED-008', brandName: 'Zosyn', genericName: 'Piperacillin and Tazobactam', category: 'Antibiotic', dosageForm: 'IV Injection', strength: '4.5 g vial', stockQuantity: 420, reorderLevel: 150, unitPrice: 34.00, batchNumber: 'BAT-ZOS-3310', expiryDate: '2027-10-01', storageRequirement: 'Room Temperature (15-25°C)', controlledDrug: false, manufacturer: 'Pfizer' },
  { id: 'MED-009', brandName: 'Vancocin', genericName: 'Vancomycin Hydrochloride', category: 'Antibiotic', dosageForm: 'IV Injection', strength: '1 g vial', stockQuantity: 310, reorderLevel: 80, unitPrice: 22.00, batchNumber: 'BAT-VAN-9081', expiryDate: '2027-12-14', storageRequirement: 'Room Temperature (15-25°C)', controlledDrug: false, manufacturer: 'Baxter' },
  { id: 'MED-010', brandName: 'ProAir HFA', genericName: 'Albuterol Sulfate Inhalation Aerosol', category: 'Respiratory', dosageForm: 'Inhaler', strength: '90 mcg/actuation (200 doses)', stockQuantity: 140, reorderLevel: 40, unitPrice: 48.00, batchNumber: 'BAT-ALB-7721', expiryDate: '2028-02-28', storageRequirement: 'Room Temperature (15-25°C)', controlledDrug: false, manufacturer: 'Teva Respiratory' },
];

// Lab Tests
export const SAMPLE_LAB_TESTS: LabTest[] = [
  {
    id: 'LAB-2001',
    orderNumber: 'ORD-LAB-8812',
    patientId: 'PT-10023',
    patientName: 'John Anderson',
    patientMrn: 'MRN-884920',
    doctorId: 'DOC-401',
    doctorName: 'Dr. Marcus Vance, MD',
    testName: 'Cardiac Markers & Comprehensive Metabolic Panel (CMP)',
    category: 'Biochemistry',
    status: 'Completed',
    orderDate: '2026-10-03 07:15',
    collectionDate: '2026-10-03 07:45',
    resultDate: '2026-10-03 09:10',
    isCritical: false,
    results: [
      { parameter: 'Troponin I High-Sensitivity', value: '0.08', unit: 'ng/mL', referenceRange: '< 0.04', flag: 'High' },
      { parameter: 'Creatine Kinase-MB (CK-MB)', value: '3.1', unit: 'ng/mL', referenceRange: '0.0 - 5.0', flag: 'Normal' },
      { parameter: 'Serum Potassium (K+)', value: '4.2', unit: 'mmol/L', referenceRange: '3.5 - 5.1', flag: 'Normal' },
      { parameter: 'Serum Sodium (Na+)', value: '139', unit: 'mmol/L', referenceRange: '135 - 145', flag: 'Normal' },
      { parameter: 'Serum Creatinine', value: '1.05', unit: 'mg/dL', referenceRange: '0.70 - 1.30', flag: 'Normal' },
      { parameter: 'eGFR (CKD-EPI)', value: '78', unit: 'mL/min/1.73m²', referenceRange: '> 60', flag: 'Normal' },
      { parameter: 'Fasting Blood Glucose', value: '124', unit: 'mg/dL', referenceRange: '70 - 99', flag: 'High' },
    ],
    technicianNotes: 'Verified on Roche Cobas 8000 analyzer. Downward delta confirmed on Troponin I from peak of 1.45 on Oct 2.'
  },
  {
    id: 'LAB-2002',
    orderNumber: 'ORD-LAB-8819',
    patientId: 'PT-10112',
    patientName: 'Sophia Martinez',
    patientMrn: 'MRN-773910',
    doctorId: 'DOC-408',
    doctorName: 'Dr. Rachel Green, MD',
    testName: 'Complete Blood Count (CBC) with Differential',
    category: 'Hematology',
    status: 'Completed',
    orderDate: '2026-10-04 06:30',
    collectionDate: '2026-10-04 06:50',
    resultDate: '2026-10-04 07:40',
    isCritical: true,
    results: [
      { parameter: 'White Blood Cell (WBC)', value: '18.4', unit: 'x10³/uL', referenceRange: '4.5 - 11.0', flag: 'Critical High' },
      { parameter: 'Hemoglobin (Hgb)', value: '9.1', unit: 'g/dL', referenceRange: '12.0 - 16.0', flag: 'Low' },
      { parameter: 'Platelets', value: '88', unit: 'x10³/uL', referenceRange: '150 - 450', flag: 'Low' },
      { parameter: 'Neutrophils %', value: '86', unit: '%', referenceRange: '40 - 70', flag: 'High' },
    ],
    technicianNotes: 'PANIC VALUE: WBC 18.4 x10³/uL reported via telephone to ICU Charge Nurse at 07:42. Read-back verified.'
  }
];

// Radiology Scans
export const SAMPLE_RADIOLOGY_SCANS: RadiologyScan[] = [
  {
    id: 'RAD-3001',
    accessionNumber: 'ACC-XR-4910',
    patientId: 'PT-10023',
    patientName: 'John Anderson',
    doctorId: 'DOC-401',
    doctorName: 'Dr. Marcus Vance, MD',
    modality: 'X-Ray',
    anatomy: 'Chest',
    status: 'Report Verified',
    scheduledTime: '2026-10-02 14:00',
    radiologistName: 'Dr. Jonathan Blake, MD',
    findings: 'Lungs are clear of focal consolidation, pneumothorax, or large pleural effusion. Cardiothoracic ratio is borderline upper normal at 0.52. Mediastinal contours unremarkable. Post-interventional wire trajectory intact.',
    impression: 'No acute pulmonary edema or focal infiltrates. Stable cardiac silhouette following percutaneous intervention.',
    priority: 'Routine'
  },
  {
    id: 'RAD-3002',
    accessionNumber: 'ACC-CT-9912',
    patientId: 'PT-10045',
    patientName: 'Elena Rostova',
    doctorId: 'DOC-401',
    doctorName: 'Dr. Marcus Vance, MD',
    modality: 'CT Scan',
    anatomy: 'Chest',
    status: 'Scheduled',
    scheduledTime: '2026-10-04 15:30',
    priority: 'Urgent'
  }
];

// Invoices
export const SAMPLE_INVOICES: Invoice[] = [
  {
    id: 'INV-7001',
    invoiceNumber: 'INV-2026-10023',
    patientId: 'PT-10023',
    patientName: 'John Anderson',
    mrn: 'MRN-884920',
    issueDate: '2026-10-03',
    dueDate: '2026-10-24',
    items: [
      { description: 'Cardiac Step-Down Bed Tariff (3 nights @ $750)', category: 'Bed Charges', amount: 2250 },
      { description: 'Diagnostic Coronary Angiogram & DES Stenting', category: 'Surgery', amount: 14800 },
      { description: 'Cardiology Attending Consultation & Daily Rounds', category: 'Consultation', amount: 1200 },
      { description: 'Post-Op Pharmacy Medications (Aspirin, Ticagrelor, Atorvastatin)', category: 'Pharmacy', amount: 485 },
      { description: 'Cardiac Enzyme & CMP Laboratory Battery', category: 'Laboratory', amount: 620 },
      { description: 'Portable Digital Chest Radiography', category: 'Radiology', amount: 280 }
    ],
    subtotal: 19635,
    tax: 0,
    insuranceDiscount: 15708, // 80% coverage
    totalAmount: 3927,
    amountPaid: 3500,
    outstandingBalance: 427,
    status: 'Partially Paid'
  }
];

// Insurance Claims
export const SAMPLE_CLAIMS: InsuranceClaim[] = [
  {
    id: 'CLM-5001',
    claimNumber: 'CLM-BCS-99201',
    invoiceId: 'INV-7001',
    patientId: 'PT-10023',
    patientName: 'John Anderson',
    provider: 'Blue Cross Shield',
    policyNumber: 'BCS-9920192',
    claimedAmount: 15708,
    approvedAmount: 15708,
    status: 'Approved',
    submissionDate: '2026-10-03',
    adjudicationDate: '2026-10-04',
    treatmentCode: 'ICD-10 I21.09 / CPT 92928'
  },
  {
    id: 'CLM-5002',
    claimNumber: 'CLM-AET-33019',
    invoiceId: 'INV-7002',
    patientId: 'PT-10045',
    patientName: 'Elena Rostova',
    provider: 'Aetna Health',
    policyNumber: 'AET-3301982',
    claimedAmount: 3420,
    status: 'Under Review',
    submissionDate: '2026-10-04',
    treatmentCode: 'ICD-10 J45.901'
  }
];

// Emergency Cases
export const SAMPLE_EMERGENCY_CASES: EmergencyCase[] = [
  {
    id: 'ED-901',
    patientName: 'David K. Miller',
    age: 49,
    gender: 'Male',
    triageLevel: 'ESI-1 Resuscitation (Immediate)',
    vitals: { bp: '82/46', heartRate: 138, spo2: 89, temp: 37.1, respRate: 32 },
    chiefComplaint: 'Acute diaphoresis, severe crushing chest pain, witnessed syncope',
    arrivalTime: '11:15 AM',
    assignedBay: 'Trauma Bay 1',
    assignedDoctor: 'Dr. Robert Thorne, MD',
    assignedNurse: 'Sarah Jenkins, RN',
    status: 'Stabilizing'
  },
  {
    id: 'ED-902',
    patientName: 'Rachel Vance',
    age: 28,
    gender: 'Female',
    triageLevel: 'ESI-2 Emergent (<15m)',
    vitals: { bp: '110/72', heartRate: 114, spo2: 94, temp: 38.9, respRate: 24 },
    chiefComplaint: 'Right lower quadrant abdominal rebound tenderness, fever',
    arrivalTime: '11:05 AM',
    assignedBay: 'Acute Bay 3',
    assignedDoctor: 'Dr. Robert Thorne, MD',
    assignedNurse: 'Mark Stevens, RN',
    status: 'Under Evaluation'
  },
  {
    id: 'ED-903',
    patientName: 'Henry Cooper',
    age: 63,
    gender: 'Male',
    triageLevel: 'ESI-3 Urgent (<30m)',
    vitals: { bp: '148/92', heartRate: 84, spo2: 97, temp: 36.8, respRate: 18 },
    chiefComplaint: 'Left wrist deformity and intense swelling following fall on ice',
    arrivalTime: '10:48 AM',
    assignedBay: 'Fast Track 2',
    assignedDoctor: 'Dr. Emily Watson, MD',
    assignedNurse: 'Laura Croft, RN',
    status: 'Under Evaluation'
  }
];

// Audit Log initial entries
export const INITIAL_AUDIT_LOGS: AuditLogEntry[] = [
  {
    id: 'AUD-001',
    userId: 'USR-DOC-03',
    userName: 'Dr. Marcus Vance, MD',
    role: 'DOCTOR',
    action: 'VIEW',
    resourceType: 'PATIENT',
    resourceId: 'PT-10023',
    patientId: 'PT-10023',
    details: 'Viewed clinical summary and angiogram procedure notes',
    timestamp: '2026-10-04 11:12:04',
    ipAddress: '10.240.12.84',
    hospitalId: 'HOSP-01'
  },
  {
    id: 'AUD-002',
    userId: 'USR-DOC-03',
    userName: 'Dr. Marcus Vance, MD',
    role: 'DOCTOR',
    action: 'RAG_QUERY',
    resourceType: 'RAG_KB',
    resourceId: 'DOC-CLIN-SEP-02',
    patientId: 'PT-10023',
    details: 'Queried clinical guidelines for ICU sepsis resuscitation and antibiotic timing',
    timestamp: '2026-10-04 11:15:30',
    ipAddress: '10.240.12.84',
    hospitalId: 'HOSP-01'
  },
  {
    id: 'AUD-003',
    userId: 'USR-PH-07',
    userName: 'Dr. Samuel Miller, PharmD',
    role: 'PHARMACIST',
    action: 'DISPENSE',
    resourceType: 'PRESCRIPTION',
    resourceId: 'RX-9901',
    patientId: 'PT-10023',
    details: 'Dispensed Aspirin 81mg, Ticagrelor 90mg, Atorvastatin 80mg',
    timestamp: '2026-10-04 10:45:12',
    ipAddress: '10.240.14.22',
    hospitalId: 'HOSP-01'
  },
  {
    id: 'AUD-004',
    userId: 'USR-HA-02',
    userName: 'Dr. Arthur Pendelton',
    role: 'HOSPITAL_ADMIN',
    action: 'DOCUMENT_ACCESS',
    resourceType: 'DOCUMENT',
    resourceId: 'DOC-ADMIT-01',
    details: 'Reviewed Hospital Admission Policy v2.4 revision',
    timestamp: '2026-10-04 09:30:19',
    ipAddress: '10.240.10.15',
    hospitalId: 'HOSP-01'
  }
];

// In-app notifications
export const INITIAL_NOTIFICATIONS: NotificationItem[] = [
  {
    id: 'NOTIF-01',
    targetRole: 'DOCTOR',
    type: 'CRITICAL_ALERT',
    title: 'Panic Value Reported: Sophia Martinez',
    message: 'WBC 18.4 x10³/uL in ICU Bay 06. Immediate clinical review advised.',
    timestamp: '15 mins ago',
    read: false,
    severity: 'urgent'
  },
  {
    id: 'NOTIF-02',
    targetRole: 'PHARMACIST',
    type: 'MED_RESTOCK',
    title: 'Low Stock Alert: Fentanyl Citrate',
    message: 'Current inventory is 45 units (Reorder threshold: 30 units).',
    timestamp: '42 mins ago',
    read: false,
    severity: 'warning'
  },
  {
    id: 'NOTIF-03',
    targetRole: 'PATIENT',
    userId: 'USR-PT-06',
    type: 'LAB_RESULT',
    title: 'Lab Report Available',
    message: 'Your recent Cardiac & Metabolic Blood Panel has been verified by the lab.',
    timestamp: '2 hours ago',
    read: false,
    severity: 'info'
  },
  {
    id: 'NOTIF-04',
    targetRole: 'HOSPITAL_ADMIN',
    type: 'POLICY_UPDATE',
    title: 'Infection Control Manual Updated',
    message: 'Manual v4.5 has been published to the Enterprise Knowledge Base.',
    timestamp: '3 hours ago',
    read: true,
    severity: 'info'
  }
];
