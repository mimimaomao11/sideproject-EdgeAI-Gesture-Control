"""
Simple script to download or create a test hand image.
Run this to prepare for Mock Mode testing.
"""

import cv2
import numpy as np
import urllib.request

def download_sample_hand():
    """Try to download a sample hand image from the internet."""
    urls = [
        # Public domain hand gesture images
        "https://images.unsplash.com/photo-1584302179602-e4c78d9d3e7e?w=640",
    ]
    
    for url in urls:
        try:
            print(f"Attempting to download from: {url[:50]}...")
            urllib.request.urlretrieve(url, "test_hand.jpg")
            print("✓ Successfully downloaded test_hand.jpg")
            return True
        except Exception as e:
            print(f"✗ Download failed: {e}")
            continue
    
    return False


def create_placeholder():
    """Create a simple placeholder with a drawn hand."""
    # Create canvas
    img = np.ones((480, 640, 3), dtype=np.uint8) * 240
    
    # Draw a simple hand shape
    # Palm (rectangle)
    cv2.rectangle(img, (220, 180), (420, 380), (200, 180, 150), -1)
    
    # Fingers (rectangles)
    finger_positions = [
        (240, 80, 280, 180),   # Index
        (300, 60, 340, 180),   # Middle  
        (360, 80, 400, 180),   # Ring
        (410, 120, 440, 180),  # Pinky
        (180, 240, 220, 320),  # Thumb
    ]
    
    for x1, y1, x2, y2 in finger_positions:
        cv2.rectangle(img, (x1, y1), (x2, y2), (200, 180, 150), -1)
        cv2.rectangle(img, (x1, y1), (x2, y2), (100, 90, 70), 2)
    
    # Add text
    cv2.putText(img, "PLACEHOLDER - Replace with real hand photo",
                (50, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 128), 2)
    
    cv2.imwrite("test_hand.jpg", img)
    print("✓ Created placeholder: test_hand.jpg")
    return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  Test Hand Image Setup")
    print("="*60 + "\n")
    
    # Try to download first
    print("Step 1: Attempting to download a sample hand image...")
    if not download_sample_hand():
        print("\nStep 2: Creating a placeholder image...")
        create_placeholder()
    
    print("\n" + "="*60)
    print("✓ Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Run: python main.py")
    print("  2. The program will use test_hand.jpg for testing")
    print("\nFor better results:")
    print("  - Replace test_hand.jpg with your own hand photo")
    print("  - Show all 5 fingers clearly extended")
    print("  - Use good lighting and plain background")
    print()
