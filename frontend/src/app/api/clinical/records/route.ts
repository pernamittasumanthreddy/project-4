import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const patientId = searchParams.get('patientId');

    if (!patientId) {
      return NextResponse.json(
        { success: false, error: 'patientId parameter is required to retrieve clinical records' },
        { status: 400 }
      );
    }

    const chart = clinicalStore.getPatientEMRChart(patientId);

    if (!chart) {
      return NextResponse.json(
        { success: false, error: `Patient ${patientId} not found` },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      data: chart
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}
