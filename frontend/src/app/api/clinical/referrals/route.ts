import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const patientId = searchParams.get('patientId') || undefined;
    const targetDepartment = searchParams.get('targetDepartment') || undefined;
    const referringDoctorId = searchParams.get('referringDoctorId') || undefined;
    const status = searchParams.get('status') || undefined;

    const referrals = clinicalStore.getReferrals({
      patientId,
      targetDepartment,
      referringDoctorId,
      status
    });

    return NextResponse.json({
      success: true,
      count: referrals.length,
      data: referrals
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

    if (!body.patientId || !body.referringDoctorId || !body.referringDepartment || !body.targetDepartment || !body.referralReason) {
      return NextResponse.json(
        { success: false, error: 'patientId, referringDoctorId, referringDepartment, targetDepartment, and referralReason are required' },
        { status: 400 }
      );
    }

    const created = clinicalStore.createReferral(body);

    return NextResponse.json({
      success: true,
      message: 'Clinical referral created and submitted to destination department',
      data: created
    }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}

export async function PATCH(request: NextRequest) {
  try {
    const body = await request.json();
    const { id, status, consultantNotes, scheduledDate } = body;

    if (!id || !status) {
      return NextResponse.json(
        { success: false, error: 'id and status are required to update a referral' },
        { status: 400 }
      );
    }

    const updated = clinicalStore.updateReferralStatus(id, status, consultantNotes, scheduledDate);

    return NextResponse.json({
      success: true,
      message: `Referral status updated to ${status}`,
      data: updated
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 400 }
    );
  }
}
