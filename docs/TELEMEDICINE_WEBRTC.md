# Telemedicine & WebRTC Virtual Consultation Architecture

## 1. Overview
The CareTrust Telemedicine module provides encrypted, browser-to-browser peer-to-peer virtual clinical encounters between authorized physicians and patients.

## 2. Key Architecture Components
1. **Peer Connection Transport**: Standard HTML5 `RTCPeerConnection` API for real-time bi-directional audio/video transport.
2. **Interactive Connectivity Establishment (ICE)**:
   - Configured with public Google STUN fallback servers:
     - `stun:stun.l.google.com:19302`
     - `stun:stun1.l.google.com:19302`
   - Zero external paid video cloud API keys required (eliminates Twilio, Agora, or Vonage expenses).
3. **Session Signaling Protocol**:
   - HTTP Polling signaling engine operating over `/api/v1/telemedicine/sessions/{id}/signaling/`.
   - Participants publish SDP Offers, SDP Answers, and ICE Candidates as structured JSON payloads.
   - Evaluates lazy Django querysets into memory before flipping delivery status flags to prevent dropped packets.
4. **Room Lifecycle & Authorization**:
   - `SCHEDULED` — Appointment created and virtual room code generated.
   - `WAITING_ROOM` — Patient joined before doctor or vice versa; status displays waiting room screen.
   - `IN_PROGRESS` — Both participants active in room; call duration timer begins.
   - `ENDED` — Doctor concludes call or both parties leave; duration saved to database.

## 3. Pre-Join Diagnostic Screen
Before entering a live call, participants undergo an automated pre-join device check:
- Video camera stream preview with hardware mute toggle.
- Audio microphone input meter with hardware mute toggle.
- STUN transport connectivity verification.

## 4. Compliance & Privacy
- Zero call recordings enabled by default in adherence with HIPAA/HITECH regulations.
- Ephemeral in-call chat messages and clinician quick notes stored strictly under tenant-scoped records.
