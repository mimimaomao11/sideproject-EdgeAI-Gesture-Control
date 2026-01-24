"""
EdgeAI-Gesture-Control - Main Entry Point
==========================================

This is the main entry point for the EdgeAI Gesture Control application.
It creates and runs the GestureControlApp instance.

Usage:
    python main.py

Controls:
    - Press 'q' to quit the application

Author: EdgeAI Development Team
Version: 1.0.0 (Sprint 1)
"""

import sys
from src.gesture_control_app import GestureControlApp


def main():
    """
    Main function to initialize and run the application.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    print("=" * 60)
    print("  EdgeAI-Gesture-Control System")
    print("  Sprint 1: Basic Video Streaming")
    print("=" * 60)
    print()
    
    try:
        # Create application instance
        app = GestureControlApp(
            camera_index=0,
            window_name="EdgeAI Gesture Control - Sprint 1"
        )
        
        # Run main loop
        app.run()
        
        return 0
        
    except RuntimeError as e:
        print(f"\n✗ Runtime Error: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
