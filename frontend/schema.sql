-- ==============================================================================
-- HOSPITAL ENTERPRISE MANAGEMENT SYSTEM (HMS) & MULTI-RAG DATABASE SCHEMA
-- PostgreSQL 16+ with pgvector extension enabled
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector"; -- pgvector for RAG dense semantic vector indexing

-- ------------------------------------------------------------------------------
-- 1. HOSPITALS (Multi-Tenant Isolation)
-- ------------------------------------------------------------------------------
CREATE TABLE hospitals (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    license_number VARCHAR(100) NOT NULL UNIQUE,
    address TEXT NOT NULL,
    phone VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    tier VARCHAR(50) DEFAULT 'Tertiary Academic Medical Center',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 2. ROLES & PERMISSIONS
-- ------------------------------------------------------------------------------
CREATE TABLE roles (
    id VARCHAR(64) PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(150) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE permissions (
    id VARCHAR(64) PRIMARY KEY,
    permission_key VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE role_permissions (
    role_id VARCHAR(64) REFERENCES roles(id) ON DELETE CASCADE,
    permission_id VARCHAR(64) REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

-- ------------------------------------------------------------------------------
-- 3. USERS (Authentication & Role Assignment)
-- ------------------------------------------------------------------------------
CREATE TABLE users (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    role_id VARCHAR(64) REFERENCES roles(id),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    department VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP WITH TIME ZONE,
    failed_attempts INT DEFAULT 0,
    lockout_until TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_hospital ON users(hospital_id);
CREATE INDEX idx_users_email ON users(email);

-- ------------------------------------------------------------------------------
-- 4. DEPARTMENTS
-- ------------------------------------------------------------------------------
CREATE TABLE departments (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    head_user_id VARCHAR(64) REFERENCES users(id),
    floor_location VARCHAR(100),
    bed_capacity INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 5. PATIENTS (Demographics & Medical Record Numbers)
-- ------------------------------------------------------------------------------
CREATE TABLE patients (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    mrn VARCHAR(64) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(20) NOT NULL,
    blood_type VARCHAR(10),
    phone VARCHAR(50),
    email VARCHAR(100),
    address TEXT,
    emergency_contact JSONB,
    allergies TEXT[],
    chronic_conditions TEXT[],
    primary_physician_id VARCHAR(64) REFERENCES users(id),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patients_hospital ON patients(hospital_id);
CREATE INDEX idx_patients_mrn ON patients(mrn);
CREATE INDEX idx_patients_name ON patients(last_name, first_name);

-- ------------------------------------------------------------------------------
-- 6. WARDS & BEDS
-- ------------------------------------------------------------------------------
CREATE TABLE wards (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    department_id VARCHAR(64) REFERENCES departments(id),
    name VARCHAR(100) NOT NULL,
    ward_type VARCHAR(50) NOT NULL -- ICU, Telemetry, General, Isolation, Pediatric
);

CREATE TABLE beds (
    id VARCHAR(64) PRIMARY KEY,
    ward_id VARCHAR(64) REFERENCES wards(id) ON DELETE CASCADE,
    bed_number VARCHAR(50) NOT NULL,
    status VARCHAR(30) DEFAULT 'Available', -- Available, Occupied, Maintenance
    current_patient_id VARCHAR(64) REFERENCES patients(id),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 7. ADMISSIONS & DISCHARGES
-- ------------------------------------------------------------------------------
CREATE TABLE admissions (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE RESTRICT,
    admitting_doctor_id VARCHAR(64) REFERENCES users(id),
    bed_id VARCHAR(64) REFERENCES beds(id),
    admission_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    discharge_date TIMESTAMP WITH TIME ZONE,
    admission_type VARCHAR(30) NOT NULL, -- Emergency, Elective, Urgent
    admitting_diagnosis TEXT NOT NULL,
    discharge_summary TEXT,
    status VARCHAR(30) DEFAULT 'Admitted' -- Admitted, Discharge Pending, Discharged
);

-- ------------------------------------------------------------------------------
-- 8. APPOINTMENTS
-- ------------------------------------------------------------------------------
CREATE TABLE appointments (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE RESTRICT,
    doctor_id VARCHAR(64) REFERENCES users(id),
    department_id VARCHAR(64) REFERENCES departments(id),
    scheduled_time TIMESTAMP WITH TIME ZONE NOT NULL,
    appointment_type VARCHAR(50) NOT NULL,
    status VARCHAR(30) DEFAULT 'Scheduled', -- Scheduled, In Progress, Completed, Cancelled
    chief_complaint TEXT,
    room_number VARCHAR(50)
);

-- ------------------------------------------------------------------------------
-- 9. MEDICINES & PHARMACY INVENTORY
-- ------------------------------------------------------------------------------
CREATE TABLE medicines (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    brand_name VARCHAR(150) NOT NULL,
    generic_name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    dosage_form VARCHAR(50) NOT NULL,
    strength VARCHAR(50) NOT NULL,
    stock_quantity INT DEFAULT 0,
    reorder_threshold INT DEFAULT 50,
    unit_price DECIMAL(10, 2) NOT NULL,
    batch_number VARCHAR(100) NOT NULL,
    expiry_date DATE NOT NULL,
    storage_temp VARCHAR(100) NOT NULL,
    is_controlled BOOLEAN DEFAULT FALSE,
    manufacturer VARCHAR(150)
);

CREATE TABLE prescriptions (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE RESTRICT,
    doctor_id VARCHAR(64) REFERENCES users(id),
    diagnosis TEXT NOT NULL,
    status VARCHAR(30) DEFAULT 'Pending', -- Pending, Dispensed, Cancelled
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prescription_items (
    id VARCHAR(64) PRIMARY KEY,
    prescription_id VARCHAR(64) REFERENCES prescriptions(id) ON DELETE CASCADE,
    medicine_id VARCHAR(64) REFERENCES medicines(id),
    dosage VARCHAR(50) NOT NULL,
    frequency VARCHAR(50) NOT NULL,
    duration VARCHAR(50) NOT NULL,
    instructions TEXT,
    dispense_status VARCHAR(30) DEFAULT 'Pending'
);

-- ------------------------------------------------------------------------------
-- 10. LABORATORY & RADIOLOGY
-- ------------------------------------------------------------------------------
CREATE TABLE lab_orders (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id),
    doctor_id VARCHAR(64) REFERENCES users(id),
    test_name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    status VARCHAR(30) DEFAULT 'Ordered',
    is_panic_value BOOLEAN DEFAULT FALSE,
    technician_notes TEXT,
    ordered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE lab_results (
    id VARCHAR(64) PRIMARY KEY,
    order_id VARCHAR(64) REFERENCES lab_orders(id) ON DELETE CASCADE,
    parameter VARCHAR(100) NOT NULL,
    measured_value VARCHAR(50) NOT NULL,
    unit VARCHAR(30),
    reference_range VARCHAR(50),
    flag VARCHAR(30) -- Normal, High, Low, Critical High, Critical Low
);

CREATE TABLE radiology_scans (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id),
    doctor_id VARCHAR(64) REFERENCES users(id),
    modality VARCHAR(30) NOT NULL, -- X-Ray, CT, MRI, Ultrasound
    anatomy VARCHAR(100) NOT NULL,
    accession_number VARCHAR(100) UNIQUE NOT NULL,
    findings TEXT,
    impression TEXT,
    status VARCHAR(30) DEFAULT 'Scheduled',
    priority VARCHAR(30) DEFAULT 'Routine',
    radiologist_id VARCHAR(64) REFERENCES users(id)
);

-- ------------------------------------------------------------------------------
-- 11. BILLING & INSURANCE
-- ------------------------------------------------------------------------------
CREATE TABLE invoices (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id),
    invoice_number VARCHAR(100) UNIQUE NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    insurance_discount DECIMAL(12, 2) DEFAULT 0,
    total_amount DECIMAL(12, 2) NOT NULL,
    amount_paid DECIMAL(12, 2) DEFAULT 0,
    outstanding_balance DECIMAL(12, 2) NOT NULL,
    status VARCHAR(30) DEFAULT 'Pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE insurance_claims (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    invoice_id VARCHAR(64) REFERENCES invoices(id),
    patient_id VARCHAR(64) REFERENCES patients(id),
    claim_number VARCHAR(100) UNIQUE NOT NULL,
    provider_name VARCHAR(150) NOT NULL,
    claimed_amount DECIMAL(12, 2) NOT NULL,
    approved_amount DECIMAL(12, 2),
    status VARCHAR(30) DEFAULT 'Submitted',
    treatment_code VARCHAR(100) NOT NULL
);

-- ------------------------------------------------------------------------------
-- 12. KNOWLEDGE BASE & MULTI-RAG SYSTEM
-- ------------------------------------------------------------------------------
CREATE TABLE hospital_documents (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    version VARCHAR(30) NOT NULL,
    effective_date DATE NOT NULL,
    confidentiality VARCHAR(30) NOT NULL,
    role_access TEXT[] NOT NULL,
    patient_id VARCHAR(64) REFERENCES patients(id), -- If patient-specific document
    file_type VARCHAR(20) NOT NULL,
    source_uri TEXT NOT NULL,
    is_archived BOOLEAN DEFAULT FALSE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_category ON hospital_documents(category);
CREATE INDEX idx_documents_confidentiality ON hospital_documents(confidentiality);

CREATE TABLE document_chunks (
    id VARCHAR(64) PRIMARY KEY,
    document_id VARCHAR(64) REFERENCES hospital_documents(id) ON DELETE CASCADE,
    page_number INT DEFAULT 1,
    section_name VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    tags TEXT[],
    embedding vector(1536), -- Vector representation for dense semantic search
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- pgvector cosine similarity index
CREATE INDEX idx_chunks_embedding ON document_chunks USING hnsw (embedding vector_cosine_ops);

CREATE TABLE rag_queries (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    user_id VARCHAR(64) REFERENCES users(id),
    role VARCHAR(50) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    confidence_score DECIMAL(5, 4),
    latency_ms INT,
    sources_count INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 13. AUDIT LOGS (Irrevocable HIPAA Compliance)
-- ------------------------------------------------------------------------------
CREATE TABLE audit_logs (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    user_id VARCHAR(64) REFERENCES users(id),
    user_name VARCHAR(150) NOT NULL,
    role VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(100),
    patient_id VARCHAR(64),
    details TEXT NOT NULL,
    ip_address VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_patient ON audit_logs(patient_id);
CREATE INDEX idx_audit_user ON audit_logs(user_id);

-- ==============================================================================
-- 14. CLINICAL MANAGEMENT & EMR/EHR (MEMBER 3 OWNERSHIP)
-- ==============================================================================

-- 14.1 CLINICAL ENCOUNTERS (Outpatient, Inpatient Rounds, Emergency, Referrals)
CREATE TABLE clinical_encounters (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE RESTRICT,
    doctor_id VARCHAR(64) REFERENCES users(id),
    department VARCHAR(100) NOT NULL,
    encounter_type VARCHAR(64) NOT NULL,
    encounter_date DATE NOT NULL,
    start_time VARCHAR(20) NOT NULL,
    end_time VARCHAR(20),
    status VARCHAR(30) DEFAULT 'In Progress', -- Waiting, In Progress, Completed, Signed, Amended, Cancelled
    sign_status VARCHAR(30) DEFAULT 'Draft', -- Draft, Signed, Amended, Addendum Appended
    chief_complaint TEXT NOT NULL,
    history_of_present_illness TEXT,
    past_medical_history TEXT,
    family_history TEXT,
    social_history TEXT,
    review_of_systems TEXT,
    vitals JSONB,
    examination JSONB,
    subjective_notes TEXT,
    objective_notes TEXT,
    assessment_notes TEXT,
    plan_notes TEXT,
    treatment_plan TEXT,
    patient_instructions TEXT,
    follow_up_date DATE,
    referral_id VARCHAR(64),
    signed_by VARCHAR(255),
    signed_at TIMESTAMP WITH TIME ZONE,
    digital_signature_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_encounters_patient ON clinical_encounters(patient_id);
CREATE INDEX idx_encounters_doctor ON clinical_encounters(doctor_id);
CREATE INDEX idx_encounters_date ON clinical_encounters(encounter_date);
CREATE INDEX idx_encounters_status ON clinical_encounters(status);

-- 14.2 CLINICAL AMENDMENTS & ADDENDA (Preserves amendment history without silent overwrite)
CREATE TABLE clinical_amendments (
    id VARCHAR(64) PRIMARY KEY,
    encounter_id VARCHAR(64) REFERENCES clinical_encounters(id) ON DELETE CASCADE,
    version INT NOT NULL,
    amendment_type VARCHAR(30) NOT NULL, -- Addendum, Correction, Clarification
    amended_by VARCHAR(255) NOT NULL,
    amended_by_role VARCHAR(50) NOT NULL,
    amended_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    reason_for_amendment TEXT NOT NULL,
    amendment_content TEXT NOT NULL,
    previous_content_snapshot TEXT,
    digital_signature_hash VARCHAR(255) NOT NULL
);

CREATE INDEX idx_amendments_encounter ON clinical_amendments(encounter_id);

-- 14.3 CODIFIED DIAGNOSES (ICD-10 Categorization)
CREATE TABLE clinical_diagnoses (
    id VARCHAR(64) PRIMARY KEY,
    encounter_id VARCHAR(64) REFERENCES clinical_encounters(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE CASCADE,
    code VARCHAR(30) NOT NULL, -- e.g. I25.10, E11.9, I10
    description TEXT NOT NULL,
    type VARCHAR(30) NOT NULL, -- Primary, Secondary, Differential, Chronic, Discharge
    certainty VARCHAR(30) DEFAULT 'Confirmed', -- Confirmed, Presumptive, Suspected, Ruled Out
    diagnosed_by VARCHAR(255) NOT NULL,
    diagnosed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_diagnoses_patient ON clinical_diagnoses(patient_id);
CREATE INDEX idx_diagnoses_code ON clinical_diagnoses(code);

-- 14.4 PATIENT ALLERGIES & ADVERSE REACTIONS
CREATE TABLE patient_allergies (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE CASCADE,
    allergen VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL, -- Medication, Food, Environmental, Biological
    reaction TEXT NOT NULL,
    severity VARCHAR(50) NOT NULL, -- Mild, Moderate, Severe, Life Threatening / Anaphylaxis
    verified_date DATE NOT NULL,
    verified_by VARCHAR(255) NOT NULL,
    status VARCHAR(30) DEFAULT 'Active'
);

CREATE INDEX idx_allergies_patient ON patient_allergies(patient_id);

-- 14.5 ELECTRONIC PRESCRIPTIONS (eRx / CPOE with Interaction Safety)
CREATE TABLE electronic_prescriptions (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    encounter_id VARCHAR(64) REFERENCES clinical_encounters(id) ON DELETE SET NULL,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE RESTRICT,
    doctor_id VARCHAR(64) REFERENCES users(id),
    doctor_license VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    prescribed_date DATE NOT NULL,
    status VARCHAR(30) DEFAULT 'Pending', -- Pending, Verified, Dispensed, Cancelled
    clinical_indication TEXT NOT NULL,
    allergies_checked BOOLEAN DEFAULT TRUE,
    refills_allowed INT DEFAULT 1,
    digital_signature VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE electronic_prescription_items (
    id VARCHAR(64) PRIMARY KEY,
    prescription_id VARCHAR(64) REFERENCES electronic_prescriptions(id) ON DELETE CASCADE,
    medicine_id VARCHAR(64) REFERENCES medicines(id),
    medicine_name VARCHAR(255) NOT NULL,
    generic_name VARCHAR(255) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    route VARCHAR(50) NOT NULL, -- Oral, IVPB Infusion, IV Push, Subcutaneous, Inhalation
    frequency VARCHAR(50) NOT NULL, -- QD, BID, TID, QID, PRN, Q8H
    duration_days INT NOT NULL,
    quantity INT NOT NULL,
    instructions TEXT NOT NULL,
    indication TEXT NOT NULL,
    dispense_status VARCHAR(30) DEFAULT 'Pending',
    contraindication_flag BOOLEAN DEFAULT FALSE,
    contraindication_notes TEXT
);

CREATE INDEX idx_erx_patient ON electronic_prescriptions(patient_id);

-- 14.6 NURSING OBSERVATIONS & MEWS FLOWSHEET
CREATE TABLE nursing_observations (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE CASCADE,
    ward VARCHAR(100) NOT NULL,
    bed VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    nurse_id VARCHAR(64) REFERENCES users(id),
    nurse_name VARCHAR(255) NOT NULL,
    systolic_bp INT NOT NULL,
    diastolic_bp INT NOT NULL,
    heart_rate INT NOT NULL,
    respiratory_rate INT NOT NULL,
    spo2 INT NOT NULL,
    temperature DECIMAL(4, 1) NOT NULL,
    pain_score INT DEFAULT 0,
    gcs_score INT DEFAULT 15,
    avpu_consciousness VARCHAR(30) DEFAULT 'Alert',
    blood_sugar_mg_dl INT,
    oxygen_device VARCHAR(100) DEFAULT 'Room Air',
    mews_score INT NOT NULL,
    mews_risk_category VARCHAR(100) NOT NULL,
    nursing_interventions TEXT NOT NULL,
    telemetry_rhythm VARCHAR(50),
    fall_risk_score INT,
    braden_skin_score INT
);

CREATE INDEX idx_observations_patient ON nursing_observations(patient_id);
CREATE INDEX idx_observations_timestamp ON nursing_observations(timestamp);

-- 14.7 FLUID INTAKE & OUTPUT BALANCE FLOWSHEETS
CREATE TABLE fluid_balances (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE CASCADE,
    ward VARCHAR(100) NOT NULL,
    bed VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    nurse_name VARCHAR(255) NOT NULL,
    oral_intake_ml INT DEFAULT 0,
    iv_infusion_ml INT DEFAULT 0,
    enteral_feed_ml INT DEFAULT 0,
    blood_product_ml INT DEFAULT 0,
    total_intake_ml INT NOT NULL,
    urine_output_ml INT DEFAULT 0,
    surgical_drain_ml INT DEFAULT 0,
    ng_aspirate_ml INT DEFAULT 0,
    emesis_ml INT DEFAULT 0,
    total_output_ml INT NOT NULL,
    net_balance_ml INT NOT NULL,
    shift VARCHAR(20) NOT NULL, -- Day, Evening, Night
    cumulative_24h_balance_ml INT NOT NULL,
    notes TEXT
);

CREATE INDEX idx_fluid_patient ON fluid_balances(patient_id);

-- 14.8 eMAR MEDICATION ADMINISTRATION RECORDS
CREATE TABLE emar_administrations (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE CASCADE,
    prescription_id VARCHAR(64) REFERENCES electronic_prescriptions(id) ON DELETE CASCADE,
    medicine_name VARCHAR(255) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    route VARCHAR(50) NOT NULL,
    scheduled_time VARCHAR(50) NOT NULL,
    administered_time VARCHAR(50),
    administered_by VARCHAR(255),
    witness_nurse VARCHAR(255),
    status VARCHAR(30) DEFAULT 'Due', -- Due, Administered, Held, Refused, Omitted
    notes TEXT,
    vitals_before_admin VARCHAR(255)
);

CREATE INDEX idx_emar_patient ON emar_administrations(patient_id);

-- 14.9 SBAR SHIFT HANDOVER CLINICAL NOTES
CREATE TABLE sbar_shift_handovers (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE CASCADE,
    ward VARCHAR(100) NOT NULL,
    bed VARCHAR(50) NOT NULL,
    created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    from_nurse VARCHAR(255) NOT NULL,
    to_nurse VARCHAR(255) NOT NULL,
    shift VARCHAR(50) NOT NULL,
    situation TEXT NOT NULL,
    background TEXT NOT NULL,
    assessment TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    code_status VARCHAR(50) DEFAULT 'Full Code',
    key_tasks TEXT[]
);

-- 14.10 INPATIENT DISCHARGE SUMMARIES
CREATE TABLE discharge_summaries (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    admission_id VARCHAR(64) REFERENCES admissions(id) ON DELETE RESTRICT,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE RESTRICT,
    mrn VARCHAR(64) NOT NULL,
    ward VARCHAR(100) NOT NULL,
    bed VARCHAR(50) NOT NULL,
    admission_date DATE NOT NULL,
    discharge_date DATE NOT NULL,
    admitting_diagnosis TEXT NOT NULL,
    discharge_diagnosis TEXT NOT NULL,
    secondary_diagnoses TEXT[],
    hospital_course TEXT NOT NULL,
    procedures_performed TEXT[],
    significant_findings TEXT,
    condition_at_discharge VARCHAR(100) NOT NULL,
    discharge_medications JSONB NOT NULL,
    diet_instructions TEXT NOT NULL,
    activity_restrictions TEXT NOT NULL,
    wound_care_instructions TEXT,
    warning_signs TEXT[],
    follow_up_appointments JSONB,
    attending_doctor_id VARCHAR(64) REFERENCES users(id),
    attending_doctor_name VARCHAR(255) NOT NULL,
    signed_at TIMESTAMP WITH TIME ZONE,
    digital_signature VARCHAR(255),
    status VARCHAR(30) DEFAULT 'Draft',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_discharge_patient ON discharge_summaries(patient_id);

-- 14.11 CLINICAL REFERRALS
CREATE TABLE clinical_referrals (
    id VARCHAR(64) PRIMARY KEY,
    hospital_id VARCHAR(64) REFERENCES hospitals(id) ON DELETE CASCADE,
    patient_id VARCHAR(64) REFERENCES patients(id) ON DELETE CASCADE,
    encounter_id VARCHAR(64) REFERENCES clinical_encounters(id) ON DELETE SET NULL,
    referring_doctor_id VARCHAR(64) REFERENCES users(id),
    referring_doctor_name VARCHAR(255) NOT NULL,
    referring_department VARCHAR(100) NOT NULL,
    target_department VARCHAR(100) NOT NULL,
    target_doctor_name VARCHAR(255),
    urgency VARCHAR(50) NOT NULL, -- Routine, Urgent (<24h), Emergency / Stat
    referral_reason TEXT NOT NULL,
    clinical_summary TEXT NOT NULL,
    requested_investigations TEXT[],
    status VARCHAR(30) DEFAULT 'Submitted', -- Draft, Submitted, Accepted, In Consultation, Completed, Declined
    scheduled_date DATE,
    consultant_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_referrals_patient ON clinical_referrals(patient_id);
CREATE INDEX idx_referrals_target ON clinical_referrals(target_department);

-- 14.12 CLINICAL DOCUMENTATION TEMPLATES
CREATE TABLE clinical_templates (
    id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    department VARCHAR(100) NOT NULL,
    encounter_type VARCHAR(64) NOT NULL,
    description TEXT,
    default_chief_complaint TEXT,
    subjective_template TEXT NOT NULL,
    objective_template TEXT NOT NULL,
    assessment_template TEXT NOT NULL,
    plan_template TEXT NOT NULL,
    common_diagnoses JSONB
);

