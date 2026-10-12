import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const patientId = searchParams.get('patientId') || undefined;
    const ward = searchParams.get('ward') || undefined;

    const observations = clinicalStore.getNursingObservations({ patientId, ward });

    return NextResponse.json({
      success: true,
      count: observations.length,
      data: observations
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

    if (!body.patientId || !body.systolicBp || !body.heartRate || !body.nurseName) {
      return NextResponse.json(
        { success: false, error: 'patientId, systolicBp, heartRate, and nurseName are required' },
        { status: 400 }
      );
    }

    const created = clinicalStore.recordNursingObservation(body);

    return NextResponse.json({
      success: true,
      message: 'Nursing observation & MEWS score recorded',
      data: created,
      mewsAlert: created.mews.score >= 4
    }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}
