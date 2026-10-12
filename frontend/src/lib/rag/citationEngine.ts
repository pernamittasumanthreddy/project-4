import { Citation, DocumentChunk } from '../types/rag';
import { ScoredChunk } from './reranker';

export class CitationEngine {
  public generateCitations(scoredChunks: ScoredChunk[]): Citation[] {
    return scoredChunks.map(sc => {
      const chunk = sc.chunk;
      const snippet = chunk.content.length > 280 
        ? chunk.content.substring(0, 280) + '...' 
        : chunk.content;

      return {
        documentId: chunk.documentId,
        documentTitle: chunk.documentTitle,
        category: chunk.category,
        section: chunk.section,
        pageNumber: chunk.pageNumber,
        lastUpdated: chunk.lastUpdated,
        version: chunk.version,
        relevanceScore: Math.round(sc.score * 100) / 100,
        snippet
      };
    });
  }

  // Generate grounded synthesis from approved chunks
  public synthesizeGroundedAnswer(
    question: string,
    scoredChunks: ScoredChunk[],
    role: string,
    safetyNotice?: string
  ): { answer: string; confidence: number; confidenceLevel: 'High' | 'Moderate' | 'Low' | 'Uncertain' } {
    if (safetyNotice) {
      return {
        answer: safetyNotice,
        confidence: 0.99,
        confidenceLevel: 'High'
      };
    }

    if (scoredChunks.length === 0 || scoredChunks[0].score < 0.15) {
      return {
        answer: "I couldn't find this information in the hospital's approved documents.",
        confidence: 0.1,
        confidenceLevel: 'Uncertain'
      };
    }

    const topScore = scoredChunks[0].score;
    const confidenceLevel: 'High' | 'Moderate' | 'Low' | 'Uncertain' = 
      topScore >= 0.65 ? 'High' :
      topScore >= 0.40 ? 'Moderate' : 'Low';

    // Build grounded synthesis from verified document chunks
    const primary = scoredChunks[0].chunk;
    const secondary = scoredChunks.length > 1 ? scoredChunks[1].chunk : null;

    let response = `Based on the hospital's approved documentation in **${primary.documentTitle}** (Section: *${primary.section}*, rev. ${primary.version}):\n\n`;

    // Extract core actionable sentences from the chunk
    const lines = primary.content.split('\n').filter(l => l.trim().length > 0 && !l.startsWith('[Full Context]'));
    const relevantBulletPoints = lines.slice(1, 4).map(l => `• ${l.trim()}`).join('\n');

    response += relevantBulletPoints || `• ${lines[0] || primary.content.substring(0, 200)}`;

    if (secondary && secondary.documentId !== primary.documentId) {
      response += `\n\nAdditionally, reference **${secondary.documentTitle}** (Section: *${secondary.section}*):\n`;
      const secLines = secondary.content.split('\n').filter(l => l.trim().length > 0 && !l.startsWith('[Full Context]'));
      if (secLines.length > 1) {
        response += `• ${secLines[1].trim()}`;
      }
    }

    return {
      answer: response,
      confidence: Math.min(0.99, Math.round((0.75 + topScore * 0.24) * 100) / 100),
      confidenceLevel
    };
  }
}
