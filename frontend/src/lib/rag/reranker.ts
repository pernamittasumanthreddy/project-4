import { DocumentChunk } from '../types/rag';

export interface ScoredChunk {
  chunk: DocumentChunk;
  score: number;
  bm25Score: number;
  vectorScore: number;
  rrfScore: number;
}

export class HybridReranker {
  private rrfK: number;

  constructor(rrfK: number = 60) {
    this.rrfK = rrfK;
  }

  public rerank(
    bm25Results: { chunk: DocumentChunk; score: number }[],
    vectorResults: { chunk: DocumentChunk; similarity: number }[],
    userDepartment?: string,
    topK: number = 4
  ): ScoredChunk[] {
    const chunkScores = new Map<string, {
      chunk: DocumentChunk;
      bm25Rank: number;
      vectorRank: number;
      bm25Score: number;
      vectorScore: number;
    }>();

    // Map BM25 ranks
    bm25Results.forEach((res, rank) => {
      chunkScores.set(res.chunk.id, {
        chunk: res.chunk,
        bm25Rank: rank + 1,
        vectorRank: 9999,
        bm25Score: res.score,
        vectorScore: 0
      });
    });

    // Map Vector ranks
    vectorResults.forEach((res, rank) => {
      if (chunkScores.has(res.chunk.id)) {
        const item = chunkScores.get(res.chunk.id)!;
        item.vectorRank = rank + 1;
        item.vectorScore = res.similarity;
      } else {
        chunkScores.set(res.chunk.id, {
          chunk: res.chunk,
          bm25Rank: 9999,
          vectorRank: rank + 1,
          bm25Score: 0,
          vectorScore: res.similarity
        });
      }
    });

    // Compute Reciprocal Rank Fusion (RRF) score: 1 / (k + rank1) + 1 / (k + rank2)
    const fused: ScoredChunk[] = [];

    for (const [_, item] of chunkScores.entries()) {
      let rrfScore = 0;
      if (item.bm25Rank <= 100) {
        rrfScore += 1 / (this.rrfK + item.bm25Rank);
      }
      if (item.vectorRank <= 100) {
        rrfScore += 1 / (this.rrfK + item.vectorRank);
      }

      // Department alignment boost
      if (userDepartment && item.chunk.department === userDepartment) {
        rrfScore *= 1.25;
      }

      // Normalized final score (0.0 to 1.0)
      const combinedScore = Math.min(1.0, rrfScore * 35);

      fused.push({
        chunk: item.chunk,
        score: combinedScore,
        bm25Score: item.bm25Score,
        vectorScore: item.vectorScore,
        rrfScore
      });
    }

    fused.sort((a, b) => b.score - a.score);
    return fused.slice(0, topK);
  }
}
