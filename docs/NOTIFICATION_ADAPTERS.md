# Multi-Channel Notification Engine & Delivery Adapters

## 1. Architectural Design
The Notification Center coordinates real-time alerts across all 7 platform member modules through a single, unified `NotificationDispatcher`.

## 2. Notification Categories & Triggers
- `APPOINTMENT`: Appointment booking confirmations, reschedules, and cancellations.
- `LAB_REPORT`: Immediate alerts when pathologist approves and releases laboratory results.
- `RADIOLOGY`: Notification when diagnostic imaging reports are published.
- `PRESCRIPTION`: Alerts when a physician signs a new prescription order.
- `BILLING`: Invoices issued and payment receipts generated.
- `TELEMEDICINE`: Virtual consultation room invitations when appointment is ready.
- `CLINICAL`: Clinician sign-off on consultation summaries.

## 3. Privacy & HIPAA Compliance Guardrails
- **Zero Sensitive Data in Plain Messages**: Raw blood test metrics, diagnostic conclusions, or diagnoses are NEVER included in SMS or plain email payloads.
- **Deep-Link Protocol**: Messages contain safe notifications directing patients to authenticate securely into the portal.
- **Phone Number Masking**: SMS delivery logs automatically mask recipient telephone numbers (e.g., `+1 (***) ***-8834`).

## 4. Delivery Adapters
1. **In-App Adapter**: Persists notifications to database with unread badges, mark-read state, and category filtering.
2. **Console Email Adapter (`ConsoleEmailAdapter`)**: Formats safe HTML/text email and appends to local audit delivery logs without requiring SendGrid or AWS SES credentials.
3. **Console SMS Adapter (`ConsoleSMSAdapter`)**: Enforces 160-character limits, formats masked phone numbers, and records simulation logs without requiring Twilio credentials.

## 5. Event Deduplication
All events are assigned an `event_dedup_key` (derived from hash of recipient, category, and action). When background tasks or network retries re-trigger an event, the dispatcher looks up the deduplication key and returns the existing notification without creating duplicates.
