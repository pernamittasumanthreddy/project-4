import { NextRequest, NextResponse } from 'next/server';
import { clinicalStore } from '@/lib/data/clinicalStore';

export async function GET(request: NextRequest) {
  try {
    const templates = clinicalStore.getTemplates();
    const icd10Catalog = clinicalStore.getICD10Catalog();

    return NextResponse.json({
      success: true,
      templates,
      icd10Catalog
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message },
      { status: 500 }
    );
  }
}
