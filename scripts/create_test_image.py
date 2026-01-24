"""
Create a test hand image for mock mode testing.

This script generates a simple visual representation of a hand
or helps you download a test image from the internet.
"""

import cv2
import numpy as np

def create_test_hand_placeholder():
    """
    Create a placeholder image with instructions for the user.
    This is a temporary solution until a real hand image is provided.
    """
    # Create a white background
    img = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    # Add instructions
    instructions = [
        "TEST HAND IMAGE NEEDED",
        "",
        "To use Mock Mode:",
        "1. Take a photo of your hand (5 fingers up)",
        "2. Save it as 'test_hand.jpg'",
        "3. Place it in the project directory",
        "",
        "Or use this command to download a sample:",
        "curl -o test_hand.jpg https://example.com/hand.jpg",
        "",
        "(Press 'q' to close this window)"
    ]
    
    y_offset = 100
    for i, line in enumerate(instructions):
        # Determine font size and color
        if i == 0:
            font_scale = 1.0
            color = (0, 0, 255)  # Red
            thickness = 2
        elif line.startswith("Or"):
            font_scale = 0.5
            color = (0, 128, 255)  # Orange
            thickness = 1
        elif line.startswith("curl"):
            font_scale = 0.4
            color = (128, 128, 128)  # Gray
            thickness = 1
        else:
            font_scale = 0.6
            color = (50, 50, 50)  # Dark gray
            thickness = 1
        
        # Calculate text size for centering
        (text_width, text_height), _ = cv2.getTextSize(
            line,
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            thickness
        )
        
        x = (img.shape[1] - text_width) // 2
        
        cv2.putText(
            img,
            line,
            (x, y_offset + i * 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            color,
            thickness,
            cv2.LINE_AA
        )
    
    return img


if __name__ == "__main__":
    print("📸 Test Hand Image Creator")
    print("=" * 50)
    print()
    print("Creating placeholder image...")
    
    img = create_test_hand_placeholder()
    
    # Save the image
    cv2.imwrite("test_hand_placeholder.jpg", img)
    print("✓ Created: test_hand_placeholder.jpg")
    print()
    print("⚠️  This is just a placeholder!")
    print()
    print("For best results, please:")
    print("  1. Take a photo of your hand with all 5 fingers extended")
    print("  2. Ensure good lighting and clear background")
    print("  3. Save it as 'test_hand.jpg' in this directory")
    print()
    print("Quick photo tips:")
    print("  • Use your phone camera")
    print("  • Hold hand flat, fingers spread")
    print("  • White or plain background works best")
    print("  • Make sure hand fills ~60% of frame")
    print()
    
    # Display the placeholder
    print("Displaying placeholder... (press 'q' to close)")
    cv2.imshow("Test Hand Placeholder", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n✓ Done!")
