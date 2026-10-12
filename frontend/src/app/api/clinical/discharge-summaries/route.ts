import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const patientId = searchParams.get('patientId') || undefined;

    const summaries = clinicalStore.getDischargeSummaries(patientId);

    return NextResponse.json({
      success: true,
      count: summaries.length,
      data: summaries
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    if (!body.patientId || !body.admittingDiagnosis || !body.dischargeDiagnosis || !body.attendingDoctorId) {
      return NextResponse.json(
        { success: false, error: 'patientId, admittingDiagnosis, dischargeDiagnosis, and attendingDoctorId are required' },
        { status: 400 }
      );
    }

    const created = clinicalStore.createDischargeSummary(body);

    return NextResponse.json({
      success: true,
      message: 'Inpatient discharge summary drafted successfully',
      data: created
    }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}
