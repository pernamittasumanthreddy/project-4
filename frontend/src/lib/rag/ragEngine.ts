import { DocumentChunk, HospitalDocument, RAGQueryResult } from '../types/rag';
import { UserProfile } from '../types/roles';
import { BM25Engine } from './bm25';
import { VectorStore } from './vectorStore';
import { PermissionFilterEngine } from './permissionFilter';
import { QueryClassifier } from './queryClassifier';
import { HybridReranker } from './reranker';
import { CitationEngine } from './citationEngine';
import { RAGEvaluator } from './ragEvaluator';
import { HOSPITAL_DOCUMENTS, generateDocumentChunks } from '../data/hospitalDocuments';
import { INITIAL_AUDIT_LOGS } from '../data/mockDatabase';

export class RAGEngine {
  private static instance: RAGEngine;
  private bm25: BM25Engine;
  private vectorStore: VectorStore;
  private permissionFilter: PermissionFilterEngine;
  private queryClassifier: QueryClassifier;
  private reranker: HybridReranker;
  private citationEngine: CitationEngine;
  private evaluator: RAGEvaluator;
  private chunks: DocumentChunk[] = [];
  private documents: HospitalDocument[] = [];

  private constructor() {
    this.bm25 = new BM25Engine();
    this.vectorStore = new VectorStore();
    this.permissionFilter = new PermissionFilterEngine();
    this.queryClassifier = new QueryClassifier();
    this.reranker = new HybridReranker();
    this.citationEngine = new CitationEngine();
    this.evaluator = new RAGEvaluator();

    this.initializeKnowledgeBase();
  }

  public static getInstance(): RAGEngine {
    if (!RAGEngine.instance) {
      RAGEngine.instance = new RAGEngine();
    }
    return RAGEngine.instance;
  }

  public initializeKnowledgeBase(): void {
    this.documents = [...HOSPITAL_DOCUMENTS];
    this.chunks = generateDocumentChunks();
    this.bm25.indexChunks(this.chunks);
    this.vectorStore.indexChunks(this.chunks);
  }

  public addDocument(doc: HospitalDocument): void {
    this.documents.push(doc);
    this.initializeKnowledgeBase();
  }

  public getDocuments(): HospitalDocument[] {
    return this.documents;
  }

  public getEvaluator(): RAGEvaluator {
    return this.evaluator;
  }

  public async query(user: UserProfile, question: string): Promise<RAGQueryResult> {
    const startTime = performance.now();

    // 1. Intent Classification & Safety Filtering
    const classification = this.queryClassifier.classify(question);

    // 2. Permission Engine: filter chunks by user role, department, confidentiality & patient-scope
    const permResult = this.permissionFilter.filterChunks(this.chunks, user);
    const authorizedIds = permResult.authorizedChunkIds;

    // 3. Retrieval
    const retrievalStart = performance.now();
    const bm25Results = this.bm25.search(question, authorizedIds);
    const vectorResults = this.vectorStore.search(question, authorizedIds);
    const retrievalLatency = Math.round(performance.now() - retrievalStart);

    // 4. Reranking
    const scoredChunks = this.reranker.rerank(bm25Results, vectorResults, user.department, 4);

    // 5. Grounded Synthesis & Citations
    const genStart = performance.now();
    const { answer, confidence, confidenceLevel } = this.citationEngine.synthesizeGroundedAnswer(
      question,
      scoredChunks,
      user.role,
      classification.safetyNotice
    );
    const citations = this.citationEngine.generateCitations(scoredChunks);
    const generationLatency = Math.round(performance.now() - genStart);
    const totalLatency = Math.round(performance.now() - startTime);

    // Record evaluation metric
    this.evaluator.recordQuery(user.role);

    // 6. Audit Logging
    const queryId = `QRY-${Date.now().toString().slice(-6)}`;
    INITIAL_AUDIT_LOGS.unshift({
      id: `AUD-${Date.now().toString().slice(-6)}`,
      userId: user.id,
      userName: user.name,
      role: user.role,
      action: 'RAG_QUERY',
      resourceType: 'RAG_KB',
      resourceId: citations.length > 0 ? citations[0].documentId : undefined,
      patientId: user.patientId,
      details: `User (${user.role}) asked: "${question.substring(0, 70)}..." -> Retrieved ${citations.length} sources (${confidenceLevel} confidence)`,
      timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
      ipAddress: '10.240.10.1',
      hospitalId: user.hospitalId
    });

    return {
      queryId,
      question,
      role: user.role,
      answer,
      citations,
      confidenceScore: confidence,
      confidenceLevel,
      isGrounded: scoredChunks.length > 0 && !classification.safetyNotice,
      sourceCount: citations.length,
      retrievalLatencyMs: retrievalLatency,
      generationLatencyMs: generationLatency,
      totalLatencyMs: totalLatency,
      verificationBadge: 'This answer is based on hospital documents',
      safetyNotice: classification.safetyNotice,
      evaluatedAt: new Date().toISOString()
    };
  }
}
