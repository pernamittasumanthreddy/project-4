import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const patientId = searchParams.get('patientId') || undefined;

    const notes = clinicalStore.getSBARNotes(patientId);

    return NextResponse.json({
      success: true,
      count: notes.length,
      data: notes
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

    if (!body.patientId || !body.fromNurse || !body.toNurse || !body.situation || !body.recommendation) {
      return NextResponse.json(
        { success: false, error: 'patientId, fromNurse, toNurse, situation, and recommendation are required' },
        { status: 400 }
      );
    }

    const created = clinicalStore.recordSBARHandover(body);

    return NextResponse.json({
      success: true,
      message: 'SBAR shift handover recorded',
      data: created
    }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}
