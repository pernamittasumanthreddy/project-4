import { DocumentChunk } from '../types/rag';

export class BM25Engine {
  private k1: number;
  private b: number;
  private docLengths: Map<string, number> = new Map();
  private avgDocLength: number = 0;
  private invertedIndex: Map<string, Map<string, number>> = new Map(); // term -> (chunkId -> freq)
  private chunkMap: Map<string, DocumentChunk> = new Map();
  private totalDocs: number = 0;

  constructor(k1: number = 1.5, b: number = 0.75) {
    this.k1 = k1;
    this.b = b;
  }

  private tokenize(text: string): string[] {
    return text
      .toLowerCase()
      .replace(/[^\w\s-]/g, ' ')
      .split(/\s+/)
      .filter(w => w.length > 2 && !STOP_WORDS.has(w));
  }

  public indexChunks(chunks: DocumentChunk[]): void {
    this.totalDocs = chunks.length;
    let totalLength = 0;

    this.invertedIndex.clear();
    this.docLengths.clear();
    this.chunkMap.clear();

    for (const chunk of chunks) {
      this.chunkMap.set(chunk.id, chunk);
      const text = `${chunk.documentTitle} ${chunk.section} ${chunk.content} ${(chunk.tags || []).join(' ')}`;
      const tokens = this.tokenize(text);
      const len = tokens.length;
      this.docLengths.set(chunk.id, len);
      totalLength += len;

      const termCounts: Map<string, number> = new Map();
      for (const token of tokens) {
        termCounts.set(token, (termCounts.get(token) || 0) + 1);
      }

      for (const [term, count] of termCounts.entries()) {
        if (!this.invertedIndex.has(term)) {
          this.invertedIndex.set(term, new Map());
        }
        this.invertedIndex.get(term)!.set(chunk.id, count);
      }
    }

    this.avgDocLength = this.totalDocs > 0 ? totalLength / this.totalDocs : 1;
  }

  public search(query: string, candidateChunkIds?: Set<string>): { chunk: DocumentChunk; score: number }[] {
    const queryTokens = this.tokenize(query);
    if (queryTokens.length === 0 || this.totalDocs === 0) return [];

    const scores: Map<string, number> = new Map();

    for (const term of queryTokens) {
      const posting = this.invertedIndex.get(term);
      if (!posting) continue;

      const docFreq = posting.size;
      // IDF formula
      const idf = Math.log(1 + (this.totalDocs - docFreq + 0.5) / (docFreq + 0.5));

      for (const [chunkId, tf] of posting.entries()) {
        if (candidateChunkIds && !candidateChunkIds.has(chunkId)) {
          continue;
        }

        const docLen = this.docLengths.get(chunkId) || this.avgDocLength;
        const normFactor = 1 - this.b + this.b * (docLen / this.avgDocLength);
        const scoreIncrement = idf * ((tf * (this.k1 + 1)) / (tf + this.k1 * normFactor));

        scores.set(chunkId, (scores.get(chunkId) || 0) + scoreIncrement);
      }
    }

    const results = Array.from(scores.entries())
      .map(([chunkId, score]) => ({
        chunk: this.chunkMap.get(chunkId)!,
        score
      }))
      .filter(item => item.chunk !== undefined)
      .sort((a, b) => b.score - a.score);

    return results;
  }
}

const STOP_WORDS = new Set([
  'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'in', 'to', 'for', 'of', 'or', 'by',
  'with', 'as', 'that', 'this', 'it', 'from', 'be', 'are', 'was', 'were', 'has', 'have',
  'had', 'not', 'but', 'what', 'all', 'were', 'when', 'can', 'your', 'about'
]);
