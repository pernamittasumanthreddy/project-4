import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const patientId = searchParams.get('patientId') || undefined;
    const doctorId = searchParams.get('doctorId') || undefined;
    const status = searchParams.get('status') || undefined;

    const prescriptions = clinicalStore.getPrescriptions({ patientId, doctorId, status });

    return NextResponse.json({
      success: true,
      count: prescriptions.length,
      data: prescriptions
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

    if (!body.patientId || !body.doctorId || !body.items || !body.items.length) {
      return NextResponse.json(
        { success: false, error: 'patientId, doctorId, and at least one medication item are required' },
        { status: 400 }
      );
    }

    const { prescription, allergyWarnings } = clinicalStore.createPrescription(body);

    return NextResponse.json({
      success: true,
      message: 'Electronic prescription created successfully',
      data: prescription,
      allergyWarnings,
      hasAllergyConflict: allergyWarnings.length > 0
    }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}
