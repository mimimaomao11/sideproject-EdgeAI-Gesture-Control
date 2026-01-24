"""
Test MediaPipe Hand Detection with downloaded model
"""
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

print("=== MediaPipe Hand Detection Test ===\n")

# Check model file
import os
if not os.path.exists("hand_landmarker.task"):
    print("✗ Model file not found!")
    print("Please run: python download_model.py")
    exit(1)

print("✓ Model file found")

# Create HandLandmarker
print("Creating HandLandmarker...")
try:
    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path="hand_landmarker.task"),
        running_mode=vision.RunningMode.IMAGE,  # Use IMAGE mode for testing
        num_hands=1,
        min_hand_detection_confidence=0.7
    )
    landmarker = vision.HandLandmarker.create_from_options(options)
    print("✓ HandLandmarker created successfully!")
except Exception as e:
    print(f"✗ Failed to create HandLandmarker: {e}")
    exit(1)

# Test with test image
print("\nTesting with test_hand.jpg...")
if not os.path.exists("test_hand.jpg"):
    print("✗ test_hand.jpg not found!")
    exit(1)

frame = cv2.imread("test_hand.jpg")
if frame is None:
    print("✗ Failed to load image")
    exit(1)

print(f"✓ Image loaded: {frame.shape}")

# Convert to RGB
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

# Detect
print("\nPerforming hand detection...")
try:
    result = landmarker.detect(mp_image)
    
    if result.hand_landmarks:
        print(f"✓ Detected {len(result.hand_landmarks)} hand(s)!")
        print(f"  Number of landmarks: {len(result.hand_landmarks[0])}")
        
        # Test finger counting logic
        hand = result.hand_landmarks[0]
        
        # Simple finger count (index finger tip vs pip)
        index_tip = hand[8]
        index_pip = hand[6]
        
        print(f"\n  Index finger tip Y: {index_tip.y:.3f}")
        print(f"  Index finger PIP Y: {index_pip.y:.3f}")
        
        if index_tip.y < index_pip.y:
            print("  → Index finger is EXTENDED")
        else:
            print("  → Index finger is FOLDED")
            
    else:
        print("✗ No hands detected")
        
except Exception as e:
    print(f"✗ Detection failed: {e}")
    import traceback
    traceback.print_exc()
finally:
    landmarker.close()
    print("\n✓ Test completed!")
