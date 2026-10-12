import { NextResponse } from 'next/server';
import { RAGEngine } from '@/lib/rag/ragEngine';
import { DEMO_USERS } from '@/lib/data/mockDatabase';
import { HospitalRole } from '@/lib/types/roles';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { question, role = 'DOCTOR', userId } = body;

    if (!question || typeof question !== 'string') {
      return NextResponse.json({ error: 'Question is required' }, { status: 400 });
    }

    const user = DEMO_USERS[role as HospitalRole] || DEMO_USERS['DOCTOR'];
    const ragEngine = RAGEngine.getInstance();
    const result = await ragEngine.query(user, question);

    return NextResponse.json(result);
  } catch (error: any) {
    console.error('RAG Query Error:', error);
    return NextResponse.json({ error: error.message || 'Internal RAG query error' }, { status: 500 });
  }
}
