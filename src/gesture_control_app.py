"""
EdgeAI-Gesture-Control Application
===================================
Sprint 2: MediaPipe Hands Integration & Gesture Recognition
(Updated for MediaPipe 0.10.32+ New API)

This module implements the core GestureControlApp class that handles
video capture, hand detection using MediaPipe Tasks API, finger counting algorithm,
and real-time gesture recognition.

Author: EdgeAI Development Team
Version: 2.1.0 (Sprint 2 - MediaPipe 0.10.32+)
"""

import cv2
import time
import os
import numpy as np
from typing import Optional, Tuple, List
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class GestureControlApp:
    """
    Main application class for gesture-based IoT control system.
    
    This class manages video capture from the laptop camera, performs
    hand detection using MediaPipe Tasks API, recognizes gestures (finger counting),
    and displays real-time metrics.
    
    Attributes:
        cap (cv2.VideoCapture): Video capture object for camera access
        window_name (str): Name of the display window
        fps (float): Current frames per second
        prev_time (float): Timestamp of previous frame for FPS calculation
        hand_landmarker: MediaPipe HandLandmarker instance (new API)
        use_mock_mode (bool): Whether running in mock mode (static image)
        finger_count (int): Current count of extended fingers (0-5)
    """
    
    def __init__(self, camera_index: int = 0, window_name: str = "EdgeAI Gesture Control"):
        """
        Initialize the GestureControlApp.
        
        Args:
            camera_index (int): Camera device index (default: 0 for built-in camera)
            window_name (str): Name for the OpenCV display window
            
        Raises:
            RuntimeError: If camera cannot be opened and no test image exists
        """
        self.window_name = window_name
        self.cap: Optional[cv2.VideoCapture] = None
        self.fps: float = 0.0
        self.prev_time: float = time.time()
        self.use_mock_mode: bool = False
        self.finger_count: int = 0
        
        # Initialize MediaPipe HandLandmarker (new API)
        self._initialize_mediapipe()
        
        # Try to initialize camera, fallback to mock mode if fails
        try:
            self._initialize_camera(camera_index)
            print(f"✓ GestureControlApp initialized successfully")
            print(f"✓ Camera: Device {camera_index}")
        except RuntimeError as e:
            print(f"⚠ Camera initialization failed: {e}")
            self._try_mock_mode()
        
        print(f"✓ Window: '{self.window_name}'")
        print(f"✓ MediaPipe HandLandmarker: Initialized (v{mp.__version__})")
        print(f"✓ Press 'q' to quit\n")
    
    def _initialize_mediapipe(self) -> None:
        """
        Initialize MediaPipe HandLandmarker using new Tasks API.
        
        Sets up MediaPipe with optimized parameters for real-time
        hand tracking and gesture recognition.
        
        Raises:
            RuntimeError: If model file is not found
        """
        # Check for model file
        model_path = "hand_landmarker.task"
        if not os.path.exists(model_path):
            raise RuntimeError(
                f"Model file '{model_path}' not found!\n"
                f"Please run: python download_model.py\n"
                f"This will download the required Hand Landmarker model."
            )
        
        # Configure HandLandmarker options
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,  # Video mode for continuous processing
            num_hands=1,                             # Track only one hand
            min_hand_detection_confidence=0.7,       # High confidence threshold
            min_hand_presence_confidence=0.5,        # Balanced tracking
            min_tracking_confidence=0.5              # Balanced tracking
        )
        
        # Create HandLandmarker instance
        self.hand_landmarker = vision.HandLandmarker.create_from_options(options)
        
    def _try_mock_mode(self) -> None:
        """
        Attempt to enable mock mode using test_hand.jpg if available.
        
        Raises:
            RuntimeError: If mock mode cannot be enabled
        """
        test_image_path = os.path.join("assets", "test_hand.jpg")
        if os.path.exists(test_image_path):
            self.use_mock_mode = True
            print(f"✓ Mock mode enabled: Using '{test_image_path}'")
            print(f"  (Press 'q' to quit)")
        else:
            raise RuntimeError(
                f"Camera unavailable and no test image found.\n"
                f"Please either:\n"
                f"  1. Connect a camera\n"
                f"  2. Place a 'test_hand.jpg' in the project directory"
            )
    
    def _initialize_camera(self, camera_index: int) -> None:
        """
        Initialize the camera capture device.
        
        Args:
            camera_index (int): Camera device index
            
        Raises:
            RuntimeError: If camera initialization fails
        """
        try:
            self.cap = cv2.VideoCapture(camera_index)
            
            if not self.cap.isOpened():
                raise RuntimeError(
                    f"Failed to open camera at index {camera_index}. "
                    f"Please check if:\n"
                    f"  1. Camera is connected and not used by another application\n"
                    f"  2. Camera permissions are granted\n"
                    f"  3. Camera index is correct (try 0, 1, or 2)"
                )
            
            # Set camera properties for better performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
        except Exception as e:
            raise RuntimeError(f"Camera initialization error: {str(e)}")
    
    def _calculate_fps(self) -> float:
        """
        Calculate current frames per second.
        
        Returns:
            float: Current FPS value
        """
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        return fps
    
    def _draw_fps(self, frame) -> None:
        """
        Draw FPS counter on the frame.
        
        Args:
            frame: OpenCV image frame to draw on
        """
        # Update FPS with smoothing
        self.fps = self.fps * 0.9 + self._calculate_fps() * 0.1
        
        # Draw semi-transparent background for better readability
        cv2.rectangle(frame, (5, 5), (150, 40), (0, 0, 0), -1)
        cv2.rectangle(frame, (5, 5), (150, 40), (0, 255, 0), 2)
        
        # Draw FPS text
        fps_text = f"FPS: {self.fps:.1f}"
        cv2.putText(
            frame,
            fps_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )
    
    def process_frame(self, frame: np.ndarray, timestamp_ms: int) -> np.ndarray:
        """
        Process frame with MediaPipe HandLandmarker to detect and draw hand landmarks.
        
        This method converts the frame to RGB, performs hand detection using the new
        Tasks API, draws the detected landmarks and connections, and counts fingers.
        
        Args:
            frame: Input BGR frame from camera
            timestamp_ms: Timestamp in milliseconds for video processing
            
        Returns:
            Processed frame with hand landmarks drawn
        """
        # Convert BGR to RGB (MediaPipe requires RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Detect hands using new API
        detection_result = self.hand_landmarker.detect_for_video(mp_image, timestamp_ms)
        
        # Reset finger count
        self.finger_count = 0
        
        # Draw hand landmarks if detected
        if detection_result.hand_landmarks:
            for hand_landmarks in detection_result.hand_landmarks:
                # Draw landmarks with connections
                self._draw_landmarks_on_image(frame, hand_landmarks)
                
                # Count extended fingers
                self.finger_count = self._count_fingers(hand_landmarks)
        
        return frame
    
    def _draw_landmarks_on_image(self, frame: np.ndarray, hand_landmarks) -> None:
        """
        Draw hand landmarks and connections on the frame.
        
        Custom implementation for MediaPipe 0.10.32+ (no drawing_utils available).
        
        Args:
            frame: OpenCV image frame to draw on
            hand_landmarks: Hand landmarks list from detection result
        """
        # Hand connections (same as MediaPipe HAND_CONNECTIONS)
        HAND_CONNECTIONS = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),  # Index finger
            (5, 9), (9, 10), (10, 11), (11, 12),  # Middle finger
            (9, 13), (13, 14), (14, 15), (15, 16),  # Ring finger
            (13, 17), (0, 17), (17, 18), (18, 19), (19, 20)  # Pinky
        ]
        
        h, w, _ = frame.shape
        
        # Draw connections first (so landmarks appear on top)
        for connection in HAND_CONNECTIONS:
            start_idx, end_idx = connection
            if start_idx < len(hand_landmarks) and end_idx < len(hand_landmarks):
                start_point = hand_landmarks[start_idx]
                end_point = hand_landmarks[end_idx]
                
                # Convert normalized coordinates to pixel coordinates
                start_x = int(start_point.x * w)
                start_y = int(start_point.y * h)
                end_x = int(end_point.x * w)
                end_y = int(end_point.y * h)
                
                # Draw line (white color)
                cv2.line(frame, (start_x, start_y), (end_x, end_y), 
                        (255, 255, 255), 2, cv2.LINE_AA)
        
        # Draw landmarks (joints)
        for idx, landmark in enumerate(hand_landmarks):
            # Convert normalized coordinates to pixel coordinates
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            
            # Different colors for different finger types
            if idx in [0]:  # Wrist
                color = (0, 255, 0)  # Green
                radius = 5
            elif idx in [4, 8, 12, 16, 20]:  # Fingertips
                color = (0, 255, 255)  # Yellow
                radius = 4
            else:  # Other joints
                color = (0, 200, 0)  # Light green
                radius = 3
            
            # Draw filled circle
            cv2.circle(frame, (x, y), radius, color, -1)
            # Draw border
            cv2.circle(frame, (x, y), radius, (255, 255, 255), 1)
    
    def _count_fingers(self, hand_landmarks) -> int:
        """
        Count the number of extended fingers using landmark positions.
        
        Algorithm:
        - For thumb: Compare x-coordinate of tip (4) with MCP joint (2)
          * Right hand: Tip should be to the right of MCP
          * Left hand: Tip should be to the left of MCP
        - For other fingers (index, middle, ring, pinky):
          Compare y-coordinate of tip with PIP joint
          * Tip should be above (lower y-value) PIP when extended
        
        Mathematical Logic:
        - MediaPipe landmarks are normalized to [0, 1]
        - Y-axis: 0 is top, 1 is bottom
        - X-axis: 0 is left, 1 is right
        - Extended finger: tip.y < pip.y (tip is higher)
        
        Landmark indices:
        - Thumb: TIP=4, MCP=2
        - Index: TIP=8, PIP=6
        - Middle: TIP=12, PIP=10
        - Ring: TIP=16, PIP=14
        - Pinky: TIP=20, PIP=18
        
        Args:
            hand_landmarks: MediaPipe hand landmarks list
            
        Returns:
            int: Count of extended fingers (0-5)
        """
        # Finger tip and joint indices
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        finger_pips = [2, 6, 10, 14, 18]  # Corresponding joints for comparison
        
        fingers_up = 0
        
        # Check thumb (special case - use x-coordinate)
        # Determine hand orientation by comparing wrist and middle finger MCP
        wrist = hand_landmarks[0]
        middle_mcp = hand_landmarks[9]
        
        # If wrist is to the left of middle MCP, it's a right hand
        is_right_hand = wrist.x < middle_mcp.x
        
        thumb_tip = hand_landmarks[finger_tips[0]]
        thumb_mcp = hand_landmarks[finger_pips[0]]
        
        if is_right_hand:
            # Right hand: thumb extended if tip is to the right of MCP
            if thumb_tip.x > thumb_mcp.x:
                fingers_up += 1
        else:
            # Left hand: thumb extended if tip is to the left of MCP
            if thumb_tip.x < thumb_mcp.x:
                fingers_up += 1
        
        # Check other four fingers (use y-coordinate)
        for i in range(1, 5):  # Index, Middle, Ring, Pinky
            tip = hand_landmarks[finger_tips[i]]
            pip = hand_landmarks[finger_pips[i]]
            
            # Finger is extended if tip is above (lower y value) than PIP
            if tip.y < pip.y:
                fingers_up += 1
        
        return fingers_up
    
    def _draw_gesture_info(self, frame: np.ndarray) -> None:
        """
        Draw gesture recognition information on the frame.
        
        Displays the current finger count with a styled info box.
        
        Args:
            frame: OpenCV image frame to draw on
        """
        # Get frame dimensions
        h, w, _ = frame.shape
        
        # Draw info box in the top-right corner
        box_width = 200
        box_height = 80
        box_x = w - box_width - 10
        box_y = 5
        
        # Semi-transparent background
        cv2.rectangle(
            frame, 
            (box_x, box_y), 
            (box_x + box_width, box_y + box_height),
            (0, 0, 0), 
            -1
        )
        cv2.rectangle(
            frame,
            (box_x, box_y),
            (box_x + box_width, box_y + box_height),
            (255, 165, 0),  # Orange border
            2
        )
        
        # Draw "Gesture" label
        cv2.putText(
            frame,
            "Gesture:",
            (box_x + 10, box_y + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 165, 0),
            1,
            cv2.LINE_AA
        )
        
        # Draw finger count
        finger_text = f"Fingers: {self.finger_count}"
        cv2.putText(
            frame,
            finger_text,
            (box_x + 10, box_y + 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),  # Yellow
            2,
            cv2.LINE_AA
        )

    
    def run(self) -> None:
        """
        Main application loop.
        
        Supports two modes:
        1. Camera mode: Continuously captures and processes frames
        2. Mock mode: Processes a static test image
        
        Press 'q' to exit safely.
        
        Raises:
            RuntimeError: If frame capture fails unexpectedly
        """
        if self.use_mock_mode:
            self._run_mock_mode()
        else:
            self._run_camera_mode()
    
    def _run_camera_mode(self) -> None:
        """
        Run in camera mode with real-time video stream processing.
        """
        print("▶ Starting camera mode...")
        print("  - Hand detection: Active")
        print("  - Finger counting: Enabled\n")
        frame_count = 0
        
        try:
            while True:
                # Capture frame
                ret, frame = self.cap.read()
                
                if not ret:
                    raise RuntimeError(
                        "Failed to capture frame. Camera may have been disconnected."
                    )
                
                # Mirror the frame for more intuitive interaction
                frame = cv2.flip(frame, 1)
                
                # Calculate timestamp in milliseconds
                timestamp_ms = int(time.time() * 1000)
                
                # Process frame with MediaPipe HandLandmarker (new API)
                frame = self.process_frame(frame, timestamp_ms)
                
                # Draw FPS counter
                self._draw_fps(frame)
                
                # Draw gesture information
                self._draw_gesture_info(frame)
                
                # TODO (Sprint 3): Add MQTT publishing based on gestures
                
                # Display frame
                cv2.imshow(self.window_name, frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print(f"\n✓ User requested exit (pressed 'q')")
                    print(f"✓ Total frames processed: {frame_count}")
                    break
                
                frame_count += 1
                
        except KeyboardInterrupt:
            print("\n✓ Interrupted by user (Ctrl+C)")
        except Exception as e:
            print(f"\n✗ Error during execution: {str(e)}")
            raise
        finally:
            self.cleanup()
    
    def _run_mock_mode(self) -> None:
        """
        Run in mock mode using a static test image.
        
        This mode is useful for testing gesture recognition logic
        without a camera.
        """
        print("▶ Starting mock mode...")
        print("  - Using static image: test_hand.jpg")
        print("  - Hand detection: Active")
        print("  - Press 'q' to quit\n")
        
        # Load test image
        test_image = cv2.imread(os.path.join("assets", "test_hand.jpg"))
        
        if test_image is None:
            raise RuntimeError("Failed to load test_hand.jpg")
        
        try:
            frame_count = 0
            while True:
                # Create a copy to process
                frame = test_image.copy()
                
                # Calculate timestamp (simulated)
                timestamp_ms = int(time.time() * 1000)
                
                # Process frame with MediaPipe HandLandmarker
                frame = self.process_frame(frame, timestamp_ms)
                
                # Draw gesture information
                self._draw_gesture_info(frame)
                
                # Add mock mode indicator
                cv2.putText(
                    frame,
                    "MOCK MODE",
                    (10, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA
                )
                
                # Display frame
                cv2.imshow(self.window_name, frame)
                
                # Handle keyboard input
                key = cv2.waitKey(100) & 0xFF
                if key == ord('q'):
                    print("\n✓ User requested exit (pressed 'q')")
                    print(f"✓ Detected fingers: {self.finger_count}")
                    break
                
                frame_count += 1
                
        except KeyboardInterrupt:
            print("\n✓ Interrupted by user (Ctrl+C)")
        except Exception as e:
            print(f"\n✗ Error during execution: {str(e)}")
            raise
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """
        Release all resources and close windows.
        
        This method ensures proper cleanup of camera, MediaPipe,
        and window resources. Should be called when application exits.
        """
        print("\n▶ Cleaning up resources...")
        
        # Release MediaPipe HandLandmarker
        if hasattr(self, 'hand_landmarker') and self.hand_landmarker is not None:
            self.hand_landmarker.close()
            print("  ✓ MediaPipe HandLandmarker released")
        
        # Release camera
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            print("  ✓ Camera released")
        
        # Close all OpenCV windows
        cv2.destroyAllWindows()
        print("  ✓ Windows closed")
        print("\n✓ Application terminated successfully")


if __name__ == "__main__":
    # This allows testing the class directly
    app = GestureControlApp()
    app.run()
