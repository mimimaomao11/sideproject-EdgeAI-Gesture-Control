"""
Test MediaPipe 0.10.32 HandLandmarker API
"""
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

print("Testing HandLandmarker initialization...")

try:
    # Method 1: Using default model (should download automatically)
    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=''),
        running_mode=vision.RunningMode.VIDEO
    )
    print("✓ HandLandmarkerOptions created")
    
    landmarker = vision.HandLandmarker.create_from_options(options)
    print("✓ HandLandmarker created successfully!")
    landmarker.close()
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    
    print("\n--- Trying alternative approach ---")
    try:
        # Try without model path (use default)
        options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(),
            running_mode=vision.RunningMode.VIDEO
        )
        print("✓ Alternative options created")
    except Exception as e2:
        print(f"✗ Alternative also failed: {e2}")
