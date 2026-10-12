import { NextResponse } from 'next/server';
import { Appointment } from '@/lib/types/hms';

const SAMPLE_APPOINTMENTS: Appointment[] = [
  { id: 'APT-101', patientId: 'PT-10023', patientName: 'John Anderson', patientMrn: 'MRN-884920', doctorId: 'DOC-401', doctorName: 'Dr. Marcus Vance, MD', department: 'Cardiology', date: '2026-10-04', time: '09:30 AM', type: 'Specialist Consultation', status: 'In Progress', symptoms: 'Post-stenting chest follow-up', priority: 'Urgent', roomNumber: 'Room 310, Wing B' },
  { id: 'APT-102', patientId: 'PT-10045', patientName: 'Elena Rostova', patientMrn: 'MRN-449182', doctorId: 'DOC-401', doctorName: 'Dr. Marcus Vance, MD', department: 'Cardiology', date: '2026-10-04', time: '10:45 AM', type: 'Follow-up', status: 'Scheduled', symptoms: 'Dyspnea upon moderate exertion', priority: 'Routine', roomNumber: 'Room 310, Wing B' },
  { id: 'APT-103', patientId: 'PT-10089', patientName: 'Marcus Vance-Carter', patientMrn: 'MRN-192083', doctorId: 'DOC-401', doctorName: 'Dr. Marcus Vance, MD', department: 'Cardiology', date: '2026-10-04', time: '02:15 PM', type: 'General Consultation', status: 'Scheduled', symptoms: 'Routine annual cardiovascular screening', priority: 'Routine', roomNumber: 'Room 310, Wing B' },
  { id: 'APT-104', patientId: 'PT-10112', patientName: 'Sophia Martinez', patientMrn: 'MRN-773910', doctorId: 'DOC-408', doctorName: 'Dr. Rachel Green, MD', department: 'Intensive Care Unit (ICU)', date: '2026-10-04', time: '11:00 AM', type: 'Emergency Review', status: 'In Progress', symptoms: 'Sepsis escalation and ICU bedside round', priority: 'Emergency', roomNumber: 'ICU Bay 06' },
];

export async function GET() {
  return NextResponse.json({ appointments: SAMPLE_APPOINTMENTS });
}
