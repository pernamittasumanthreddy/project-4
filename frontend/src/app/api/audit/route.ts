import { NextResponse } from 'next/server';
import { INITIAL_AUDIT_LOGS } from '@/lib/data/mockDatabase';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '50', 10);
    return NextResponse.json({ logs: INITIAL_AUDIT_LOGS.slice(0, limit) });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to retrieve audit logs' }, { status: 500 });
  }
}
