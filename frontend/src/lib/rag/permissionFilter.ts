import { DocumentChunk } from '../types/rag';
import { UserProfile } from '../types/roles';
import { ROLE_CONFIGS } from '../data/roleConfigs';

export interface PermissionFilterResult {
  authorizedChunkIds: Set<string>;
  totalCandidateCount: number;
  filteredCount: number;
  rejectionReasons: Record<string, string>;
}

export class PermissionFilterEngine {
  public filterChunks(chunks: DocumentChunk[], user: UserProfile): PermissionFilterResult {
    const roleConfig = ROLE_CONFIGS[user.role];
    const authorized = new Set<string>();
    const rejectionReasons: Record<string, string> = {};

    for (const chunk of chunks) {
      // 1. Role Access Check
      if (chunk.roleAccess && !chunk.roleAccess.includes(user.role)) {
        rejectionReasons[chunk.id] = `Role '${user.role}' not permitted on document '${chunk.documentTitle}'.`;
        continue;
      }

      // 2. Category Check according to Role RAG Config
      if (roleConfig && !roleConfig.allowedCategories.includes(chunk.category)) {
        rejectionReasons[chunk.id] = `Document category '${chunk.category}' is outside knowledge scope for ${roleConfig.displayName}.`;
        continue;
      }

      // 3. Confidentiality Level Check
      if (roleConfig && !roleConfig.allowedConfidentiality.includes(chunk.confidentiality)) {
        rejectionReasons[chunk.id] = `Confidentiality '${chunk.confidentiality}' exceeds role authorization level.`;
        continue;
      }

      // 4. Patient Isolation Security Check
      if (chunk.patientId) {
        if (user.role === 'PATIENT') {
          // Patient can ONLY view their own records
          if (user.patientId !== chunk.patientId) {
            rejectionReasons[chunk.id] = `Patient isolation: cannot access other patient (${chunk.patientId}) health records.`;
            continue;
          }
        } else if (user.role === 'DOCTOR' || user.role === 'NURSE') {
          // Clinicians can only view assigned patients
          const assigned = user.assignedPatients || [];
          if (!assigned.includes(chunk.patientId)) {
            rejectionReasons[chunk.id] = `Clinician access restricted: patient ${chunk.patientId} is not assigned to ${user.name}.`;
            continue;
          }
        } else if (user.role === 'EMERGENCY_STAFF' || user.role === 'PHARMACIST') {
          // Emergency staff can view acute patient records
        } else {
          // Administrative, HR, billing, or general staff cannot view raw patient medical charts
          rejectionReasons[chunk.id] = `Role '${user.role}' is not authorized to retrieve identifiable patient clinical records.`;
          continue;
        }
      }

      authorized.add(chunk.id);
    }

    return {
      authorizedChunkIds: authorized,
      totalCandidateCount: chunks.length,
      filteredCount: authorized.size,
      rejectionReasons
    };
  }
}
