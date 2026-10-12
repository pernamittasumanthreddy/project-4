import { NextResponse } from 'next/server';
import { RAGEngine } from '@/lib/rag/ragEngine';
import { HospitalDocument } from '@/lib/types/rag';

export async function GET() {
  try {
    const ragEngine = RAGEngine.getInstance();
    const documents = ragEngine.getDocuments();
    return NextResponse.json({ documents });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch documents' }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { title, category, department, content, roleAccess, confidentiality, version = 'v1.0' } = body;

    if (!title || !content || !category) {
      return NextResponse.json({ error: 'Title, category, and content are required' }, { status: 400 });
    }

    const docId = `DOC-NEW-${Date.now().toString().slice(-4)}`;
    const newDoc: HospitalDocument = {
      id: docId,
      title,
      category,
      department: department || 'Hospital Administration',
      version,
      effectiveDate: new Date().toISOString().substring(0, 10),
      lastUpdated: new Date().toISOString().substring(0, 10),
      confidentiality: confidentiality || 'INTERNAL',
      roleAccess: roleAccess || ['HOSPITAL_ADMIN', 'DOCTOR', 'NURSE'],
      fileType: 'PDF',
      fileSize: `${Math.round(content.length / 1024) || 1} KB`,
      sourceUri: `/documents/${docId.toLowerCase()}.pdf`,
      isArchived: false,
      content,
      sections: [
        {
          heading: 'Core Directive',
          page: 1,
          text: content.substring(0, 300)
        }
      ]
    };

    const ragEngine = RAGEngine.getInstance();
    ragEngine.addDocument(newDoc);

    return NextResponse.json({ success: true, document: newDoc });
  } catch (error: any) {
    return NextResponse.json({ error: 'Failed to upload document' }, { status: 500 });
  }
}
