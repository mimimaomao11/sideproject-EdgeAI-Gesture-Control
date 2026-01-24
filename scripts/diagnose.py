import sys
print("Python version:", sys.version)
print("Python path:")
for p in sys.path[:5]:
    print(f"  {p}")

print("\n--- Testing MediaPipe import ---")
import mediapipe
print(f"✓ MediaPipe imported from: {mediapipe.__file__}")
print(f"✓ MediaPipe version: {mediapipe.__version__}")

print("\n--- Checking MediaPipe contents ---")
mp_attrs = [attr for attr in dir(mediapipe) if not attr.startswith('_')]
print(f"MediaPipe has {len(mp_attrs)} public attributes")
print(f"First 20: {mp_attrs[:20]}")

print("\n--- Checking for 'solutions' ---")
if hasattr(mediapipe, 'solutions'):
    print("✓ 'solutions' found!")
    print(f"  Type: {type(mediapipe.solutions)}")
else:
    print("✗ 'solutions' NOT FOUND!")
    print("  This意味著 MediaPipe 安裝損壞")
    print("\n  建議解決方案:")
    print("  1. pip uninstall mediapipe")
    print("  2. pip cache purge")
    print("  3. pip install mediapipe==0.10.9")
