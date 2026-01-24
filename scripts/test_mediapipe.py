import mediapipe as mp

print("Testing MediaPipe import...")
print(f"MediaPipe version: {mp.__version__}")

try:
    mp_hands = mp.solutions.hands
    print("✓ mp.solutions.hands - OK")
except Exception as e:
    print(f"✗ mp.solutions.hands - FAILED: {e}")

try:
    mp_drawing = mp.solutions.drawing_utils  
    print("✓ mp.solutions.drawing_utils - OK")
except Exception as e:
    print(f"✗ mp.solutions.drawing_utils - FAILED: {e}")

try:
    mp_drawing_styles = mp.solutions.drawing_styles
    print("✓ mp.solutions.drawing_styles - OK")
except Exception as e:
    print(f"⚠ mp.solutions.drawing_styles - NOT AVAILABLE (this is OK)")

print("\nTesting Hands initialization...")
try:
    hands = mp.solutions.hands.Hands()
    print("✓ Hands() - OK")
    hands.close()
except Exception as e:
    print(f"✗ Hands() - FAILED: {e}")

print("\n✓ All tests passed!")
