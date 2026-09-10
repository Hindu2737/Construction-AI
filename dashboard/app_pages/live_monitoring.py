import threading

import av
import cv2
import streamlit as st
from ultralytics import YOLO
from streamlit_webrtc import WebRtcMode, VideoProcessorBase, webrtc_streamer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.title("📹 Real-Time Site Monitoring")

st.caption(
    "AI-powered real-time construction site safety monitoring "
    "using the trained YOLO model."
)


# ============================================================
# LOAD YOLO MODEL
# ============================================================

@st.cache_resource
def load_yolo_model():
    model_path = "runs/detect/models/safety_yolo-2/weights/best.pt"

    return YOLO(model_path)


try:
    model = load_yolo_model()
except Exception as e:
    st.error("❌ Unable to load the YOLO safety model.")
    st.code(str(e))
    st.stop()


# ============================================================
# SHARED MONITORING STATE
# ============================================================

class MonitoringState:

    def __init__(self):
        self.lock = threading.Lock()

        self.workers_detected = 0

        self.violations = {
            "NO-Hardhat": 0,
            "NO-Mask": 0,
            "NO-Safety Vest": 0,
        }

        self.total_detections = 0

        self.site_status = "SAFE"


if (
    "live_monitoring_state" not in st.session_state
    or st.session_state["live_monitoring_state"] is None
    or not isinstance(
        st.session_state["live_monitoring_state"],
        MonitoringState,
    )
):
    st.session_state["live_monitoring_state"] = MonitoringState()

monitoring_state = st.session_state["live_monitoring_state"]


# ============================================================
# YOLO VIDEO PROCESSOR
# ============================================================

class SafetyVideoProcessor(VideoProcessorBase):

    def __init__(self):

        self.model = model

        self.frame_count = 0

        self.last_results = {
            "workers": 0,
            "violations": {
                "NO-Hardhat": 0,
                "NO-Mask": 0,
                "NO-Safety Vest": 0,
            },
            "detections": 0,
            "status": "SAFE",
        }

    def recv(self, frame):

        # Convert WebRTC frame to OpenCV image
        image = frame.to_ndarray(format="bgr24")

        self.frame_count += 1

        # ----------------------------------------------------
        # Run YOLO
        # ----------------------------------------------------

        try:

            results = self.model(
                image,
                verbose=False,
                conf=0.50,
                imgsz=640,
            )

        except Exception:
            return av.VideoFrame.from_ndarray(
                image,
                format="bgr24"
            )


        # ----------------------------------------------------
        # Current frame statistics
        # ----------------------------------------------------

        workers_detected = 0

        current_violations = {
            "NO-Hardhat": 0,
            "NO-Mask": 0,
            "NO-Safety Vest": 0,
        }

        total_detections = 0


        # ----------------------------------------------------
        # Process detections
        # ----------------------------------------------------

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                class_id = int(box.cls[0])

                confidence = float(box.conf[0])

                if confidence < 0.50:
                    continue

                label = result.names[class_id]

                total_detections += 1


                # --------------------------------------------
                # Count workers
                # --------------------------------------------

                if label == "Person":
                    workers_detected += 1


                # --------------------------------------------
                # Count PPE violations
                # --------------------------------------------

                if label in current_violations:

                    current_violations[label] += 1


                # --------------------------------------------
                # Bounding box
                # --------------------------------------------

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )


                # Violation = red
                # Normal detection = green

                if label in current_violations:

                    box_color = (0, 0, 255)

                else:

                    box_color = (0, 255, 0)


                cv2.rectangle(
                    image,
                    (x1, y1),
                    (x2, y2),
                    box_color,
                    2,
                )


                # --------------------------------------------
                # Detection label
                # --------------------------------------------

                text = f"{label} {confidence:.2f}"

                cv2.putText(
                    image,
                    text,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    box_color,
                    2,
                )


        # ====================================================
        # DETERMINE SITE STATUS
        # ====================================================

        total_violations = sum(
            current_violations.values()
        )

        if total_violations > 0:

            site_status = "UNSAFE"

        else:

            site_status = "SAFE"


        # ====================================================
        # UPDATE SHARED STATE
        # ====================================================

        with monitoring_state.lock:

            monitoring_state.workers_detected = (
                workers_detected
            )

            monitoring_state.violations = dict(
                current_violations
            )

            monitoring_state.total_detections = (
                total_detections
            )

            monitoring_state.site_status = (
                site_status
            )


        # ====================================================
        # DRAW SITE STATUS ON VIDEO
        # ====================================================

        if site_status == "UNSAFE":

            status_color = (0, 0, 255)

        else:

            status_color = (0, 255, 0)


        # Status background

        cv2.rectangle(
            image,
            (10, 10),
            (360, 75),
            (0, 0, 0),
            -1,
        )


        # Status text

        cv2.putText(
            image,
            f"SITE STATUS: {site_status}",
            (20, 52),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.85,
            status_color,
            2,
        )


        # ====================================================
        # VIOLATION WARNING ON VIDEO
        # ====================================================

        if total_violations > 0:

            cv2.rectangle(
                image,
                (10, 90),
                (450, 145),
                (0, 0, 0),
                -1,
            )

            cv2.putText(
                image,
                f"WARNING: {total_violations} PPE VIOLATION(S)",
                (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )


        # ====================================================
        # RETURN PROCESSED FRAME
        # ====================================================

        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )


# ============================================================
# CAMERA SECTION
# ============================================================

st.subheader("🎥 Live Camera")

st.info(
    "Click START and allow camera access when your browser "
    "asks for permission."
)


# ============================================================
# START WEBRTC STREAM
# ============================================================


webrtc_streamer(
    key="constructai-live-monitoring",

    mode=WebRtcMode.SENDRECV,

    video_processor_factory=SafetyVideoProcessor,

    media_stream_constraints={
        "video": True,
        "audio": False,
    },

    video_html_attrs={
        "style": {
            "width": "800px",
            "height": "600px",
            "object-fit": "contain",
            "margin": "0 auto",
            "display": "block",
        },
        "controls": False,
        "autoPlay": True,
        "muted": True,
    },

    async_processing=True,
)


# ============================================================
# LIVE SAFETY STATUS
# ============================================================

st.markdown("---")

st.subheader("🚨 Live Safety Status")


with monitoring_state.lock:

    workers_detected = (
        monitoring_state.workers_detected
    )

    violations = dict(
        monitoring_state.violations
    )

    total_detections = (
        monitoring_state.total_detections
    )

    site_status = (
        monitoring_state.site_status
    )


# ============================================================
# METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Workers Detected",
        workers_detected,
    )


with col2:

    total_violations = sum(
        violations.values()
    )

    st.metric(
        "PPE Violations",
        total_violations,
    )


with col3:

    st.metric(
        "Detections",
        total_detections,
    )


with col4:

    st.metric(
        "Site Status",
        site_status,
    )


# ============================================================
# PPE VIOLATION BREAKDOWN
# ============================================================

st.subheader("🦺 PPE Violation Breakdown")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "❌ No Hardhat",
        violations.get(
            "NO-Hardhat",
            0
        ),
    )


with col2:

    st.metric(
        "❌ No Mask",
        violations.get(
            "NO-Mask",
            0
        ),
    )


with col3:

    st.metric(
        "❌ No Safety Vest",
        violations.get(
            "NO-Safety Vest",
            0
        ),
    )


# ============================================================
# ALERT
# ============================================================

if site_status == "UNSAFE":

    st.error(
        "🚨 SAFETY VIOLATION DETECTED — "
        "PPE non-compliance has been detected "
        "in the live camera feed. "
        "Take appropriate corrective action."
    )

else:

    st.success(
        "✅ No confirmed PPE violations detected "
        "in the current frame."
    )


# ============================================================
# HOW IT WORKS
# ============================================================

with st.expander(
    "ℹ️ How Real-Time Monitoring Works"
):

    st.write(
        """
        The browser camera sends live video frames
        to the Streamlit application through WebRTC.

        The trained YOLO safety model processes the
        video frames and detects construction-site
        safety conditions.

        The system currently monitors:

        • Construction workers
        • Missing hardhats
        • Missing masks
        • Missing safety vests

        Detection boxes are displayed directly on the
        live camera feed.

        Red boxes indicate PPE violations.

        Green boxes indicate normal detections.

        The site status becomes UNSAFE when a confirmed
        PPE violation is detected.
        """
    )