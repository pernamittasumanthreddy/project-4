import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const patientId = searchParams.get('patientId') || undefined;

    const emar = clinicalStore.getEMARRecords(patientId);

    return NextResponse.json({
      success: true,
      count: emar.length,
      data: emar
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
    const { emarId, administeredBy, witnessNurse, status, vitalsBeforeAdmin, notes } = body;

    if (!emarId || !administeredBy || !status) {
      return NextResponse.json(
        { success: false, error: 'emarId, administeredBy, and status are required' },
        { status: 400 }
      );
    }

    const updated = clinicalStore.administerMedication(emarId, {
      administeredBy,
      witnessNurse,
      status,
      vitalsBeforeAdmin,
      notes
    });

    return NextResponse.json({
      success: true,
      message: `Medication status updated to ${status} with 5-rights verification`,
      data: updated
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 400 }
    );
  }
}
