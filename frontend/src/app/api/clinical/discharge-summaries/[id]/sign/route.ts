import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json();
    const { doctorName, doctorLicense } = body;

    if (!doctorName || !doctorLicense) {
      return NextResponse.json(
        { success: false, error: 'doctorName and doctorLicense are required to sign the discharge summary' },
        { status: 400 }
      );
    }

    const signed = clinicalStore.signDischargeSummary(params.id, doctorName, doctorLicense);

    return NextResponse.json({
      success: true,
      message: 'Discharge summary signed and locked with official physician cryptographic digest',
      data: signed
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 400 }
    );
  }
}
