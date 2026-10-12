import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const patientId = searchParams.get('patientId') || undefined;

    const records = clinicalStore.getFluidBalances(patientId);

    return NextResponse.json({
      success: true,
      count: records.length,
      data: records
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

    if (!body.patientId || !body.nurseName) {
      return NextResponse.json(
        { success: false, error: 'patientId and nurseName are required' },
        { status: 400 }
      );
    }

    const created = clinicalStore.recordFluidBalance({
      patientId: body.patientId,
      patientName: body.patientName || 'Patient',
      ward: body.ward || 'General Ward',
      bed: body.bed || 'Bed',
      nurseName: body.nurseName,
      oralIntakeMl: Number(body.oralIntakeMl || 0),
      ivInfusionMl: Number(body.ivInfusionMl || 0),
      enteralFeedMl: Number(body.enteralFeedMl || 0),
      bloodProductMl: Number(body.bloodProductMl || 0),
      urineOutputMl: Number(body.urineOutputMl || 0),
      surgicalDrainMl: Number(body.surgicalDrainMl || 0),
      ngAspirateMl: Number(body.ngAspirateMl || 0),
      emesisMl: Number(body.emesisMl || 0),
      shift: body.shift || 'Day',
      cumulative24hBalanceMl: Number(body.cumulative24hBalanceMl || 0),
      notes: body.notes
    });

    return NextResponse.json({
      success: true,
      message: 'Fluid intake and output recorded with balance reconciliation',
      data: created
    }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}
