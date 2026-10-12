import { NextResponse } from 'next/server';
import { generateEnterprisePatients, SEED_PATIENTS } from '@/lib/data/mockDatabase';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const search = searchParams.get('search')?.toLowerCase() || '';
    const limit = parseInt(searchParams.get('limit') || '50', 10);

    const allPatients = generateEnterprisePatients();
    
    let filtered = allPatients;
    if (search) {
      filtered = allPatients.filter(p => 
        p.firstName.toLowerCase().includes(search) ||
        p.lastName.toLowerCase().includes(search) ||
        p.mrn.toLowerCase().includes(search) ||
        p.id.toLowerCase().includes(search) ||
        p.phone.includes(search)
      );
    }

    return NextResponse.json({
      total: filtered.length,
      patients: filtered.slice(0, limit)
    });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to retrieve patients' }, { status: 500 });
  }
}
