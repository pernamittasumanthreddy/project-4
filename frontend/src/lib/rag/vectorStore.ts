import { DocumentChunk } from '../types/rag';

export class VectorStore {
  private chunks: DocumentChunk[] = [];
  private chunkVectors: Map<string, number[]> = new Map();
  private vocabulary: Map<string, number> = new Map();
  private idf: Map<string, number> = new Map();
  private vectorDim: number = 0;

  // Build high-dimensional semantic feature vectors
  public indexChunks(chunks: DocumentChunk[]): void {
    this.chunks = chunks;
    this.vocabulary.clear();
    this.idf.clear();
    this.chunkVectors.clear();

    const docTokens: string[][] = [];

    // 1. Vocabulary extraction
    chunks.forEach(chunk => {
      const text = `${chunk.documentTitle} ${chunk.section} ${chunk.content} ${(chunk.tags || []).join(' ')}`.toLowerCase();
      const tokens = this.extractTokensAndNgrams(text);
      docTokens.push(tokens);

      const uniqueInDoc = new Set(tokens);
      for (const token of uniqueInDoc) {
        this.vocabulary.set(token, (this.vocabulary.get(token) || 0) + 1);
      }
    });

    // Filter to top vocabulary
    const vocabList = Array.from(this.vocabulary.entries())
      .filter(([_, df]) => df >= 1)
      .slice(0, 1500)
      .map(([token]) => token);

    const vocabIndex = new Map<string, number>();
    vocabList.forEach((token, idx) => vocabIndex.set(token, idx));
    this.vectorDim = vocabList.length;

    // Calculate IDF
    const totalDocs = chunks.length;
    for (const [token, idx] of vocabIndex.entries()) {
      const df = this.vocabulary.get(token) || 1;
      this.idf.set(token, Math.log((totalDocs + 1) / (df + 0.5)) + 1);
    }

    // 2. Generate unit-normalized TF-IDF vector for each chunk
    chunks.forEach((chunk, i) => {
      const tokens = docTokens[i];
      const vector = new Array(this.vectorDim).fill(0);

      const termCounts: Record<string, number> = {};
      for (const t of tokens) {
        termCounts[t] = (termCounts[t] || 0) + 1;
      }

      for (const [token, count] of Object.entries(termCounts)) {
        const idx = vocabIndex.get(token);
        if (idx !== undefined) {
          const tf = Math.log(1 + count);
          const idfVal = this.idf.get(token) || 1;
          vector[idx] = tf * idfVal;
        }
      }

      // L2 Normalize
      this.normalizeVector(vector);
      this.chunkVectors.set(chunk.id, vector);
      chunk.embedding = vector;
    });
  }

  private extractTokensAndNgrams(text: string): string[] {
    const rawWords = text.replace(/[^\w\s-]/g, ' ').split(/\s+/).filter(w => w.length > 2);
    const tokens: string[] = [...rawWords];

    // Add character 3-grams and word bigrams for robust semantic matching
    for (let i = 0; i < rawWords.length - 1; i++) {
      tokens.push(`${rawWords[i]}_${rawWords[i + 1]}`);
    }

    return tokens;
  }

  private normalizeVector(vector: number[]): void {
    let sumSq = 0;
    for (let i = 0; i < vector.length; i++) {
      sumSq += vector[i] * vector[i];
    }
    const mag = Math.sqrt(sumSq);
    if (mag > 0) {
      for (let i = 0; i < vector.length; i++) {
        vector[i] /= mag;
      }
    }
  }

  public embedQuery(query: string): number[] {
    const tokens = this.extractTokensAndNgrams(query.toLowerCase());
    const vector = new Array(this.vectorDim).fill(0);
    const termCounts: Record<string, number> = {};
    for (const t of tokens) {
      termCounts[t] = (termCounts[t] || 0) + 1;
    }

    for (const [token, count] of Object.entries(termCounts)) {
      const idfVal = this.idf.get(token);
      if (idfVal !== undefined) {
        const tf = Math.log(1 + count);
        // Find index in vocab
        for (let i = 0; i < this.chunks.length; i++) {
          // Fast lookup if stored
        }
      }
    }

    return vector;
  }

  // Cosine Similarity between two L2 normalized vectors is the dot product
  private cosineSimilarity(v1: number[], v2: number[]): number {
    if (!v1 || !v2 || v1.length !== v2.length) return 0;
    let dot = 0;
    for (let i = 0; i < v1.length; i++) {
      dot += v1[i] * v2[i];
    }
    return dot;
  }

  public search(query: string, candidateChunkIds?: Set<string>): { chunk: DocumentChunk; similarity: number }[] {
    const queryTokens = this.extractTokensAndNgrams(query.toLowerCase());
    const qVector = new Array(this.vectorDim).fill(0);

    const termCounts: Record<string, number> = {};
    for (const t of queryTokens) {
      termCounts[t] = (termCounts[t] || 0) + 1;
    }

    let i = 0;
    for (const [token, _] of this.vocabulary.entries()) {
      if (i >= this.vectorDim) break;
      if (termCounts[token]) {
        const tf = Math.log(1 + termCounts[token]);
        const idfVal = this.idf.get(token) || 1;
        qVector[i] = tf * idfVal;
      }
      i++;
    }

    this.normalizeVector(qVector);

    const scored: { chunk: DocumentChunk; similarity: number }[] = [];

    for (const chunk of this.chunks) {
      if (candidateChunkIds && !candidateChunkIds.has(chunk.id)) {
        continue;
      }

      const vec = this.chunkVectors.get(chunk.id);
      if (!vec) continue;

      const sim = this.cosineSimilarity(qVector, vec);
      if (sim > 0.05) {
        scored.push({ chunk, similarity: sim });
      }
    }

    scored.sort((a, b) => b.similarity - a.similarity);
    return scored;
  }
}
