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
      encounterId: encounter.id,
      amendmentsCount: encounter.amendments.length,
      amendments: encounter.amendments
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json();
    const { amendmentType, amendedBy, amendedByRole, reasonForAmendment, amendmentContent } = body;

    if (!amendedBy || !reasonForAmendment || !amendmentContent) {
      return NextResponse.json(
        { success: false, error: 'amendedBy, reasonForAmendment, and amendmentContent are required' },
        { status: 400 }
      );
    }

    const updatedEncounter = clinicalStore.addAmendment(params.id, {
      amendmentType: amendmentType || 'Addendum',
      amendedBy,
      amendedByRole: amendedByRole || 'DOCTOR',
      reasonForAmendment,
      amendmentContent
    });

    return NextResponse.json({
      success: true,
      message: 'Clinical amendment / addendum successfully appended with audit timestamp',
      data: updatedEncounter
    }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 400 }
    );
  }
}
