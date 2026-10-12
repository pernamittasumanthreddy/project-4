import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json();
    const { signedBy, licenseNumber } = body;

    if (!signedBy || !licenseNumber) {
      return NextResponse.json(
        { success: false, error: 'signedBy and licenseNumber are required to digitally sign this record' },
        { status: 400 }
      );
    }

    const signed = clinicalStore.signEncounter(params.id, signedBy, licenseNumber);

    return NextResponse.json({
      success: true,
      message: 'Clinical record digitally signed and locked against further edits',
      data: signed
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 400 }
    );
  }
}
