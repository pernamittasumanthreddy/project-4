import { NextResponse } from 'next/server';
import { DEMO_USERS } from '@/lib/data/mockDatabase';
import { HospitalRole } from '@/lib/types/roles';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const role: HospitalRole = body.role || 'DOCTOR';

    const user = DEMO_USERS[role];
    if (!user) {
      return NextResponse.json({ error: 'Invalid role specified' }, { status: 400 });
    }

    return NextResponse.json({
      success: true,
      token: `jwt_token_${user.id}_${Date.now()}`,
      user
    });
  } catch (error) {
    return NextResponse.json({ error: 'Authentication failed' }, { status: 500 });
  }
}
