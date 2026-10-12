import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const encounter = clinicalStore.getEncounterById(params.id);
    if (!encounter) {
      return NextResponse.json(
        { success: false, error: `Encounter ${params.id} not found` },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      data: encounter
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json();
    const updated = clinicalStore.updateEncounter(params.id, body);

    return NextResponse.json({
      success: true,
      message: 'Encounter updated successfully',
      data: updated
    });
  } catch (err: any) {
    // Catch immutability violation
    const status = err.message.includes('IMMUTABILITY VIOLATION') ? 403 : 400;
    return NextResponse.json(
      { success: false, error: err.message },
      { status }
    );
  }
}
