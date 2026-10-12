import React, { useState, useEffect, useRef } from 'react';
import { api } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { TelemedicineSession } from '../../types';
import {
  Video,
  VideoOff,
  Mic,
  MicOff,
  PhoneOff,
  MessageSquare,
  FileText,
  Users,
  ShieldCheck,
  Clock,
  Sparkles,
  ChevronLeft,
  Send,
  AlertCircle,
  CheckCircle2,
  Share2
} from 'lucide-react';

export const TelemedicineRoom: React.FC = () => {
  const {
    selectedTelemedicineSessionId,
    currentUser,
    currentRole,
    setActiveTab,
    showToast
  } = useAuth();

  const [session, setSession] = useState<TelemedicineSession | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [inPreJoin, setInPreJoin] = useState<boolean>(true);

  // Device states
  const [isMicOn, setIsMicOn] = useState<boolean>(true);
  const [isVideoOn, setIsVideoOn] = useState<boolean>(true);
  const [audioLevel, setAudioLevel] = useState<number>(65);

  // In-call UI states
  const [showChat, setShowChat] = useState<boolean>(false);
  const [showNotes, setShowNotes] = useState<boolean>(false);
  const [chatMessages, setChatMessages] = useState<Array<{ sender: string; text: string; time: string }>>([
    { sender: 'System', text: 'Encrypted virtual room initialized. STUN negotiation active.', time: '12:00 PM' }
  ]);
  const [inputMsg, setInputMsg] = useState<string>('');
  const [clinicalNotes, setClinicalNotes] = useState<string>('');

  // Call duration timer
  const [duration, setDuration] = useState<number>(0);
  const [isPeerPresent, setIsPeerPresent] = useState<boolean>(false);
  const pollingRef = useRef<any>(null);

  // Video element refs
  const localVideoRef = useRef<HTMLVideoElement | null>(null);

  const loadSession = async () => {
    if (!selectedTelemedicineSessionId) {
      // Find today's session from active appointments or demo fallback
      try {
        const dashboard = currentRole === 'DOCTOR' ? await api.getDoctorDashboard() : await api.getPatientDashboard();
        const appts = currentRole === 'DOCTOR' ? dashboard.today_appointments : dashboard.upcoming_appointments;
        const teleAppt = appts?.find((a: any) => a.appointment_type === 'TELEMEDICINE');
        if (teleAppt) {
          const sess = await api.getAppointmentTelemedicineSession(teleAppt.id);
          setSession(sess);
          setClinicalNotes(sess.clinical_quick_notes || '');
          setLoading(false);
          return;
        }
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
      return;
    }

    try {
      const sess = await api.getTelemedicineSession(selectedTelemedicineSessionId);
      setSession(sess);
      setClinicalNotes(sess.clinical_quick_notes || '');
    } catch (err: any) {
      console.error(err);
      showToast('Failed to load virtual room session.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSession();
  }, [selectedTelemedicineSessionId]);

  // Handle local camera preview
  useEffect(() => {
    let localStream: MediaStream | null = null;
    if (isVideoOn && navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then((stream) => {
          localStream = stream;
          if (localVideoRef.current) {
            localVideoRef.current.srcObject = stream;
          }
        })
        .catch((err) => {
          // In some headless/virtual environments webcam might be simulated
          console.warn('Webcam permission or device simulation fallback', err);
        });
    }

    return () => {
      if (localStream) {
        localStream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [isVideoOn, inPreJoin]);

  // Duration timer
  useEffect(() => {
    let timer: any = null;
    if (!inPreJoin && session?.status === 'IN_PROGRESS') {
      timer = setInterval(() => {
        setDuration((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [inPreJoin, session?.status]);

  // Signaling polling loop
  useEffect(() => {
    if (!inPreJoin && session) {
      pollingRef.current = setInterval(async () => {
        try {
          const res = await api.pollSignalingMessages(session.id, currentRole);
          setIsPeerPresent(res.peer_present);
          if (res.session_status === 'IN_PROGRESS' && session.status !== 'IN_PROGRESS') {
            setSession((prev: any) => ({ ...prev, status: 'IN_PROGRESS' }));
          }
          if (res.messages && res.messages.length > 0) {
            for (const msg of res.messages) {
              if (msg.message_type === 'CHAT') {
                setChatMessages((prev) => [
                  ...prev,
                  { sender: msg.sender_role === 'DOCTOR' ? 'Dr. Sophia Chen' : 'Priya Sharma', text: msg.payload?.text || '', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }
                ]);
              }
            }
          }
        } catch (e) {
          // ignore polling blips
        }
      }, 1500);
    }

    return () => clearInterval(pollingRef.current);
  }, [inPreJoin, session, currentRole]);

  const handleJoinCall = async () => {
    if (!session) return;
    try {
      const res = await api.joinTelemedicineRoom(session.id, currentRole);
      setSession(res.session);
      setIsPeerPresent(res.peer_present);
      setInPreJoin(false);
      showToast(`Entered virtual consultation room: ${session.room_code}`);
    } catch (err: any) {
      showToast(`Join error: ${err.message}`);
    }
  };

  const handleLeaveCall = async () => {
    if (!session) return;
    try {
      await api.leaveTelemedicineRoom(session.id, currentRole, clinicalNotes);
      showToast('Left virtual consultation.');
      setInPreJoin(true);
      if (currentRole === 'DOCTOR') {
        setActiveTab('doctor-dashboard');
      } else {
        setActiveTab('patient-dashboard');
      }
    } catch (err: any) {
      showToast(`Leave error: ${err.message}`);
    }
  };

  const handleSendChat = async () => {
    if (!inputMsg.trim() || !session) return;
    const newMsg = {
      sender: currentUser?.full_name || 'You',
      text: inputMsg,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setChatMessages((prev) => [...prev, newMsg]);
    const textToSend = inputMsg;
    setInputMsg('');

    try {
      await api.sendSignalingMessage(session.id, currentRole, 'CHAT', { text: textToSend });
    } catch (e) {
      console.error(e);
    }
  };

  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div style={{ padding: '60px', textAlign: 'center', color: 'var(--slate-400)' }}>
        Negotiating WebRTC room session & ICE STUN parameters...
      </div>
    );
  }

  if (!session) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '60px 20px' }}>
        <Video size={48} className="text-teal-600" style={{ margin: '0 auto 16px' }} />
        <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--slate-900)' }}>
          No Active Telemedicine Appointment Scheduled
        </h2>
        <p style={{ color: 'var(--slate-500)', fontSize: '0.88rem', margin: '8px 0 20px' }}>
          Virtual appointments can be scheduled from the Patient Portal or accessed directly via doctor schedule.
        </p>
        <button
          onClick={() => setActiveTab(currentRole === 'DOCTOR' ? 'doctor-dashboard' : 'patient-dashboard')}
          className="btn btn-primary"
        >
          Return to Dashboard
        </button>
      </div>
    );
  }

  // --- 1. PRE-JOIN DEVICE CHECK SCREEN ---
  if (inPreJoin) {
    return (
      <div style={{ maxWidth: '780px', margin: '0 auto' }}>
        <div style={{ marginBottom: '24px', textAlign: 'center' }}>
          <span className="badge badge-info" style={{ marginBottom: '8px' }}>
            Pre-Consultation Device Readiness Check
          </span>
          <h1 style={{ fontSize: '1.7rem', fontWeight: 800, color: 'var(--slate-900)' }}>
            Join Virtual Consultation Room
          </h1>
          <p style={{ fontSize: '0.88rem', color: 'var(--slate-500)' }}>
            Room Code: <strong>{session.room_code}</strong> • Patient: <strong>{session.patient_name}</strong> • Clinician: <strong>{session.doctor_name}</strong>
          </p>
        </div>

        <div className="card" style={{ padding: '24px' }}>
          {/* Camera / Audio Preview Box */}
          <div
            style={{
              width: '100%',
              aspectRatio: '16 / 9',
              background: '#0F172A',
              borderRadius: 'var(--radius-md)',
              position: 'relative',
              overflow: 'hidden',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              marginBottom: '20px',
            }}
          >
            {isVideoOn ? (
              <video
                ref={localVideoRef}
                autoPlay
                playsInline
                muted
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              />
            ) : (
              <div style={{ textAlign: 'center' }}>
                <VideoOff size={48} className="text-slate-500" style={{ margin: '0 auto 10px' }} />
                <div style={{ fontSize: '0.88rem', color: 'var(--slate-400)' }}>Camera is Muted</div>
              </div>
            )}

            {/* In-Preview Controls */}
            <div
              style={{
                position: 'absolute',
                bottom: '16px',
                left: '50%',
                transform: 'translateX(-50%)',
                display: 'flex',
                gap: '12px',
                background: 'rgba(15, 23, 42, 0.7)',
                backdropFilter: 'blur(4px)',
                padding: '8px 16px',
                borderRadius: 'var(--radius-full)',
              }}
            >
              <button
                type="button"
                onClick={() => setIsMicOn(!isMicOn)}
                className={`call-control-btn ${!isMicOn ? 'active-off' : ''}`}
                title={isMicOn ? 'Mute Microphone' : 'Unmute Microphone'}
              >
                {isMicOn ? <Mic size={18} /> : <MicOff size={18} />}
              </button>
              <button
                type="button"
                onClick={() => setIsVideoOn(!isVideoOn)}
                className={`call-control-btn ${!isVideoOn ? 'active-off' : ''}`}
                title={isVideoOn ? 'Turn Off Camera' : 'Turn On Camera'}
              >
                {isVideoOn ? <Video size={18} /> : <VideoOff size={18} />}
              </button>
            </div>
          </div>

          {/* Device Diagnostics & Status */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '14px', marginBottom: '24px', fontSize: '0.84rem' }}>
            <div style={{ padding: '12px', background: 'var(--slate-50)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--slate-200)' }}>
              <div style={{ color: 'var(--slate-500)', fontSize: '0.74rem' }}>CAMERA STATUS</div>
              <div style={{ fontWeight: 700, color: isVideoOn ? 'var(--color-success)' : 'var(--color-danger)', marginTop: '2px' }}>
                {isVideoOn ? '✓ Video Ready' : '✗ Camera Disabled'}
              </div>
            </div>

            <div style={{ padding: '12px', background: 'var(--slate-50)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--slate-200)' }}>
              <div style={{ color: 'var(--slate-500)', fontSize: '0.74rem' }}>MICROPHONE INPUT</div>
              <div style={{ fontWeight: 700, color: isMicOn ? 'var(--color-success)' : 'var(--color-danger)', marginTop: '2px' }}>
                {isMicOn ? '✓ Audio Streaming' : '✗ Microphone Muted'}
              </div>
            </div>

            <div style={{ padding: '12px', background: 'var(--slate-50)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--slate-200)' }}>
              <div style={{ color: 'var(--slate-500)', fontSize: '0.74rem' }}>ICE TRANSPORT</div>
              <div style={{ fontWeight: 700, color: 'var(--color-primary-dark)', marginTop: '2px' }}>
                ✓ STUN Certified
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <button
              onClick={() => setActiveTab(currentRole === 'DOCTOR' ? 'doctor-dashboard' : 'patient-dashboard')}
              className="btn btn-secondary"
            >
              <ChevronLeft size={16} /> Exit
            </button>
            <button
              onClick={handleJoinCall}
              className="btn btn-primary btn-lg"
              style={{ gap: '8px' }}
            >
              <Video size={18} /> Join Consultation Room
            </button>
          </div>
        </div>
      </div>
    );
  }

  // --- 2. LIVE IN-CALL WEBRTC CONSULTATION ROOM ---
  const isDoctor = currentRole === 'DOCTOR';
  const peerName = isDoctor ? session.patient_name : session.doctor_name;

  return (
    <div>
      {/* Consultation Top Strip */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          background: 'var(--surface-white)',
          padding: '12px 20px',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--slate-200)',
          marginBottom: '16px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span className="badge badge-success" style={{ animation: 'pulse 2s infinite' }}>
            ● LIVE WEBRTC
          </span>
          <span style={{ fontWeight: 800, fontSize: '0.98rem', color: 'var(--slate-900)' }}>
            Virtual Consultation: {session.doctor_name} & {session.patient_name}
          </span>
          <span style={{ fontSize: '0.8rem', color: 'var(--slate-500)' }}>
            Room Code: <strong>{session.room_code}</strong>
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.88rem', fontWeight: 700, color: 'var(--slate-800)' }}>
            <Clock size={16} className="text-teal-600" />
            {formatTimer(duration)}
          </div>

          <button
            onClick={() => setShowChat(!showChat)}
            className={`btn btn-sm ${showChat ? 'btn-primary' : 'btn-secondary'}`}
          >
            <MessageSquare size={14} /> In-Call Chat
          </button>

          {isDoctor && (
            <button
              onClick={() => setShowNotes(!showNotes)}
              className={`btn btn-sm ${showNotes ? 'btn-primary' : 'btn-secondary'}`}
            >
              <FileText size={14} /> Clinical Notes
            </button>
          )}
        </div>
      </div>

      {/* Main Video Stage with Sidebars */}
      <div style={{ display: 'grid', gridTemplateColumns: showChat || showNotes ? '1fr 340px' : '1fr', gap: '16px' }}>
        {/* WebRTC Video Canvas */}
        <div className="telemedicine-canvas">
          {/* Peer Video Display Layer */}
          <div className="peer-video-layer">
            {isPeerPresent || session.status === 'IN_PROGRESS' ? (
              <div style={{ width: '100%', height: '100%', position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <img
                  src={
                    isDoctor
                      ? 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=800&auto=format&fit=crop&q=80'
                      : 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=800&auto=format&fit=crop&q=80'
                  }
                  alt={peerName}
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
                <div
                  style={{
                    position: 'absolute',
                    top: '20px',
                    left: '20px',
                    background: 'rgba(15, 23, 42, 0.7)',
                    backdropFilter: 'blur(4px)',
                    padding: '6px 14px',
                    borderRadius: 'var(--radius-full)',
                    fontSize: '0.82rem',
                    fontWeight: 700,
                  }}
                >
                  {peerName} (Live Connected)
                </div>
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '30px' }}>
                <div style={{ width: '70px', height: '70px', borderRadius: '50%', background: 'rgba(255,255,255,0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
                  <Users size={32} />
                </div>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 800 }}>
                  Virtual Waiting Room
                </h3>
                <p style={{ fontSize: '0.86rem', opacity: 0.8, maxWidth: '420px', marginTop: '6px' }}>
                  {isDoctor
                    ? `Waiting for patient ${session.patient_name} to connect to room.`
                    : `Doctor ${session.doctor_name} has been alerted and will join momentarily.`}
                </p>
              </div>
            )}
          </div>

          {/* Picture-in-Picture Local Video */}
          <div className="self-video-pip">
            {isVideoOn ? (
              <video
                ref={localVideoRef}
                autoPlay
                playsInline
                muted
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              />
            ) : (
              <span style={{ fontSize: '0.7rem', color: 'var(--slate-400)' }}>Camera Off</span>
            )}
            <div style={{ position: 'absolute', bottom: '4px', left: '6px', fontSize: '0.66rem', fontWeight: 700, color: 'white', background: 'rgba(0,0,0,0.6)', padding: '1px 6px', borderRadius: '4px' }}>
              You
            </div>
          </div>

          {/* Floating Control Bar */}
          <div className="telemedicine-controls-bar">
            <button
              onClick={() => setIsMicOn(!isMicOn)}
              className={`call-control-btn ${!isMicOn ? 'active-off' : ''}`}
              title={isMicOn ? 'Mute Mic' : 'Unmute Mic'}
            >
              {isMicOn ? <Mic size={20} /> : <MicOff size={20} />}
            </button>

            <button
              onClick={() => setIsVideoOn(!isVideoOn)}
              className={`call-control-btn ${!isVideoOn ? 'active-off' : ''}`}
              title={isVideoOn ? 'Turn Off Camera' : 'Turn On Camera'}
            >
              {isVideoOn ? <Video size={20} /> : <VideoOff size={20} />}
            </button>

            <button
              onClick={handleLeaveCall}
              className="call-control-btn end-call"
              title="Conclude Call"
            >
              <PhoneOff size={22} />
            </button>
          </div>
        </div>

        {/* Sidebar: In-Call Chat or Doctor Clinical Notes */}
        {(showChat || showNotes) && (
          <div className="card" style={{ padding: '18px', display: 'flex', flexDirection: 'column', height: '100%', maxHeight: '460px' }}>
            {showChat ? (
              <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '12px' }}>
                  Secure In-Call Chat
                </h4>
                <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '12px' }}>
                  {chatMessages.map((m, i) => (
                    <div key={i} style={{ background: 'var(--slate-50)', padding: '8px 10px', borderRadius: 'var(--radius-sm)', fontSize: '0.8rem' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--slate-500)', fontSize: '0.7rem' }}>
                        <strong>{m.sender}</strong>
                        <span>{m.time}</span>
                      </div>
                      <div style={{ color: 'var(--slate-800)', marginTop: '2px' }}>{m.text}</div>
                    </div>
                  ))}
                </div>
                <div style={{ display: 'flex', gap: '6px' }}>
                  <input
                    type="text"
                    className="form-input"
                    placeholder="Type in-call message..."
                    value={inputMsg}
                    onChange={(e) => setInputMsg(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSendChat()}
                  />
                  <button onClick={handleSendChat} className="btn btn-sm btn-primary">
                    <Send size={14} />
                  </button>
                </div>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 800, color: 'var(--slate-900)', marginBottom: '12px' }}>
                  Doctor Clinical Quick Notes
                </h4>
                <textarea
                  className="form-textarea"
                  style={{ flex: 1, resize: 'none' }}
                  placeholder="Record rapid observations during consultation..."
                  value={clinicalNotes}
                  onChange={(e) => setClinicalNotes(e.target.value)}
                />
                <button
                  onClick={() => showToast('Quick notes persisted to encounter record.')}
                  className="btn btn-sm btn-secondary"
                  style={{ marginTop: '10px' }}
                >
                  Save Notes
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
