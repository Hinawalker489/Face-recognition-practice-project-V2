#!/usr/bin/env python3
"""
Test version of the Face Recognition Attendance System
This simplified version helps identify what's causing the system to get stuck
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def test_basic_tkinter():
    """Test if basic Tkinter is working"""
    try:
        root = tk.Tk()
        root.title("Tkinter Test")
        root.geometry("400x300")
        
        label = tk.Label(root, text="Tkinter is working!", font=("Arial", 16))
        label.pack(pady=50)
        
        button = tk.Button(root, text="Click Me", command=lambda: messagebox.showinfo("Test", "Button works!"))
        button.pack(pady=20)
        
        print("✅ Basic Tkinter test successful")
        return root
    except Exception as e:
        print(f"❌ Tkinter test failed: {e}")
        return None

def test_imports():
    """Test if all required packages can be imported"""
    try:
        print("Testing imports...")
        
        import cv2
        print("✅ OpenCV imported successfully")
        
        import numpy as np
        print("✅ NumPy imported successfully")
        
        from PIL import Image, ImageTk
        print("✅ PIL/Pillow imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_camera_access():
    """Test if camera can be accessed"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera access successful")
            cap.release()
            return True
        else:
            print("❌ Camera access failed")
            return False
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Face Recognition System Test...")
    print("=" * 50)
    
    # Test 1: Check Python version
    print(f"Python version: {sys.version}")
    
    # Test 2: Check current directory
    print(f"Current directory: {os.getcwd()}")
    
    # Test 3: Test imports
    if not test_imports():
        print("❌ Import test failed - cannot continue")
        return
    
    # Test 4: Test camera access
    if not test_camera_access():
        print("⚠️ Camera test failed - system may not work properly")
    
    # Test 5: Test basic Tkinter
    root = test_basic_tkinter()
    if root:
        print("✅ All tests passed! Starting Tkinter window...")
        print("If you see a window with 'Tkinter is working!', the system should work.")
        print("Close the test window to continue...")
        root.mainloop()
    else:
        print("❌ Tkinter test failed - this is likely the problem")

if __name__ == "__main__":
    main()



