import { NextResponse } from 'next/server';
import { HOSPITAL_BEDS, DOCTORS, SAMPLE_EMERGENCY_CASES } from '@/lib/data/mockDatabase';

export async function GET() {
  const occupiedBeds = HOSPITAL_BEDS.filter(b => b.status === 'Occupied').length;
  const availableBeds = HOSPITAL_BEDS.filter(b => b.status === 'Available').length;
  const doctorsOnDuty = DOCTORS.filter(d => d.onDuty).length;

  return NextResponse.json({
    totalPatients: 524,
    todayAppointments: 48,
    todayAdmissions: 14,
    todayDischarges: 9,
    occupiedBeds,
    availableBeds,
    totalBeds: HOSPITAL_BEDS.length,
    bedOccupancyPercent: Math.round((occupiedBeds / HOSPITAL_BEDS.length) * 100),
    doctorsOnDuty,
    pendingBillsCount: 19,
    pendingBillsAmount: 48320,
    pendingInsuranceClaimsCount: 12,
    pendingInsuranceClaimsAmount: 94600,
    emergencyCasesActive: SAMPLE_EMERGENCY_CASES.length,
    criticalLabAlerts: 1,
    infectionControlCompliance: 99.4,
    patientSatisfactionRate: 94.8,
  });
}
