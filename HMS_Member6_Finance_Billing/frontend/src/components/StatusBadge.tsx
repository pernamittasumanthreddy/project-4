import React from 'react';

interface StatusBadgeProps {
  status: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const getBadgeClass = (s: string) => {
    switch (s?.toUpperCase()) {
      case 'PAID':
      case 'SUCCESS':
      case 'APPROVED':
      case 'SETTLED':
      case 'RECONCILED':
      case 'HEALTHY':
        return 'badge-success';
      case 'PARTIALLY_PAID':
      case 'PARTIALLY_APPROVED':
      case 'PARTIALLY_REFUNDED':
      case 'PENDING':
      case 'PENDING_REVIEW':
      case 'PRE_AUTH_PENDING':
      case 'SUBMITTED':
      case 'RESUBMITTED':
      case 'IN_REVIEW':
      case 'NEEDS_ATTENTION':
        return 'badge-warning';
      case 'OVERDUE':
      case 'CANCELLED':
      case 'FAILED':
      case 'REJECTED':
      case 'DISCREPANCY_DETECTED':
      case 'ACTION_REQUIRED':
        return 'badge-danger';
      case 'ISSUED':
      case 'POSTED':
        return 'badge-info';
      default:
        return 'badge-neutral';
    }
  };

  const formatText = (s: string) => {
    return s?.replace(/_/g, ' ') || 'UNKNOWN';
  };

  return (
    <span className={`badge ${getBadgeClass(status)}`}>
      {formatText(status)}
    </span>
  );
};
