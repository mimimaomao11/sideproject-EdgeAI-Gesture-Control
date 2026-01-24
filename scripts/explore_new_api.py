"""
探索 MediaPipe 0.10.32 新 API 結構
"""
import mediapipe as mp

print("=== MediaPipe 0.10.32 API Structure ===\n")
print(f"Version: {mp.__version__}")

print("\n1. Top-level modules:")
print([a for a in dir(mp) if not a.startswith('_')])

print("\n2. Tasks module:")
if hasattr(mp, 'tasks'):
    tasks_attrs = [a for a in dir(mp.tasks) if not a.startswith('_')]
    print(f"   Attributes: {tasks_attrs}")
    
    if hasattr(mp.tasks, 'python'):
        print("\n3. tasks.python module:")
        python_attrs = [a for a in dir(mp.tasks.python) if not a.startswith('_')]
        print(f"   Attributes: {python_attrs}")
        
        if hasattr(mp.tasks.python, 'vision'):
            print("\n4. tasks.python.vision module:")
            vision_attrs = [a for a in dir(mp.tasks.python.vision) if not a.startswith('_')]
            print(f"   Attributes: {vision_attrs[:20]}")  # First 20
            
            # Check for HandLandmarker
            if 'HandLandmarker' in vision_attrs:
                print("\n✓ Found HandLandmarker!")
                print("   This is the new API for hand detection")
                
                # Check options
                if 'HandLandmarkerOptions' in vision_attrs:
                    print("✓ Found HandLandmarkerOptions!")

print("\n=== API Migration Required ===")
print("Old API: mp.solutions.hands")
print("New API: mp.tasks.python.vision.HandLandmarker")
