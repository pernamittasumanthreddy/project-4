import { NextResponse } from 'next/server';
import { RAGEngine } from '@/lib/rag/ragEngine';

export async function GET() {
  try {
    const ragEngine = RAGEngine.getInstance();
    const metrics = ragEngine.getEvaluator().getMetrics();
    return NextResponse.json(metrics);
  } catch (error: any) {
    return NextResponse.json({ error: 'Failed to fetch RAG evaluation metrics' }, { status: 500 });
  }
}
