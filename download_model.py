"""
Download MediaPipe Hand Landmarker model
"""
import urllib.request
import os

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
MODEL_PATH = "hand_landmarker.task"

print("📥 Downloading MediaPipe Hand Landmarker model...")
print(f"   URL: {MODEL_URL}")
print(f"   Destination: {MODEL_PATH}")
print()

try:
    if os.path.exists(MODEL_PATH):
        print(f"⚠ Model file already exists ({os.path.getsize(MODEL_PATH)} bytes)")
        response = input("  Redownload? (y/n): ")
        if response.lower() != 'y':
            print("✓ Using existing model file")
            exit(0)
        os.remove(MODEL_PATH)
    
    # Download with progress
    def show_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(100, (downloaded / total_size) * 100)
        bar_length = 40
        filled = int(bar_length * downloaded / total_size)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r  Progress: |{bar}| {percent:.1f}% ({downloaded/1024/1024:.1f}/{total_size/1024/1024:.1f} MB)", end='')
    
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH, show_progress)
    print()
    print(f"\n✓ Model downloaded successfully!")
    print(f"  File size: {os.path.getsize(MODEL_PATH) / 1024 / 1024:.2f} MB")
    print(f"  Saved to: {os.path.abspath(MODEL_PATH)}")
    
except Exception as e:
    print(f"\n✗ Download failed: {e}")
    print("\nManual download instructions:")
    print(f"  1. Visit: {MODEL_URL}")
    print(f"  2. Save the file as: {MODEL_PATH}")
    print("  3. Place it in the project directory")
