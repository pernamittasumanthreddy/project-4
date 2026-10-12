import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const patientId = searchParams.get('patientId') || undefined;
    const doctorId = searchParams.get('doctorId') || undefined;
    const status = searchParams.get('status') || undefined;
    const department = searchParams.get('department') || undefined;
    const hospitalId = searchParams.get('hospitalId') || undefined;

    const encounters = clinicalStore.getEncounters({
      patientId,
      doctorId,
      status,
      department,
      hospitalId
    });

    return NextResponse.json({
      success: true,
      count: encounters.length,
      data: encounters
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to fetch encounters' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    if (!body.patientId || !body.doctorId || !body.chiefComplaint) {
      return NextResponse.json(
        { success: false, error: 'patientId, doctorId, and chiefComplaint are required' },
        { status: 400 }
      );
    }

    const created = clinicalStore.createEncounter(body);

    return NextResponse.json(
      {
        success: true,
        message: 'Clinical encounter created successfully',
        data: created
      },
      { status: 201 }
    );
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message || 'Failed to create clinical encounter' },
      { status: 500 }
    );
  }
}
