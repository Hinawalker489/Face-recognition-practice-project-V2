#!/usr/bin/env python3
"""
Face Recognition Attendance System Launcher
Choose between basic and enhanced versions
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

class SystemLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System - Launcher")
        self.root.geometry("500x400")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        self.create_gui()
        
    def center_window(self):
        """Center the launcher window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_gui(self):
        """Create the launcher interface"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(pady=30)
        
        title_label = tk.Label(
            title_frame,
            text="Face Recognition Attendance System",
            font=("Arial", 20, "bold"),
            fg='#00d4ff',
            bg='#1a1a2e'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Choose your version",
            font=("Arial", 12),
            fg='#8888ff',
            bg='#1a1a2e'
        )
        subtitle_label.pack()
        
        # Version selection frame
        selection_frame = tk.Frame(self.root, bg='#1a1a2e')
        selection_frame.pack(pady=40, padx=50, fill='both', expand=True)
        
        # Enhanced version button
        enhanced_btn = tk.Button(
            selection_frame,
            text="🚀 Enhanced Version",
            font=("Arial", 16, "bold"),
            bg='#00aa44',
            fg='white',
            command=self.run_enhanced,
            bd=0,
            relief='flat',
            cursor='hand2',
            width=25,
            height=3
        )
        enhanced_btn.pack(pady=20)
        
        enhanced_desc = tk.Label(
            selection_frame,
            text="• Animated interface with modern design\n• Advanced features and better UI\n• Recommended for best experience",
            font=("Arial", 10),
            fg='#00ff88',
            bg='#1a1a2e',
            justify='left'
        )
        enhanced_desc.pack()
        
        # Basic version button
        basic_btn = tk.Button(
            selection_frame,
            text="📱 Basic Version",
            font=("Arial", 16, "bold"),
            bg='#8844aa',
            fg='white',
            command=self.run_basic,
            bd=0,
            relief='flat',
            cursor='hand2',
            width=25,
            height=3
        )
        basic_btn.pack(pady=20)
        
        basic_desc = tk.Label(
            selection_frame,
            text="• Simple and lightweight\n• Basic functionality\n• Good for testing and development",
            font=("Arial", 10),
            fg='#ff8888',
            bg='#1a1a2e',
            justify='left'
        )
        basic_desc.pack()
        
        # Exit button
        exit_btn = tk.Button(
            self.root,
            text="❌ Exit",
            font=("Arial", 12),
            bg='#aa4444',
            fg='white',
            command=self.root.destroy,
            bd=0,
            relief='flat',
            cursor='hand2',
            width=15,
            height=2
        )
        exit_btn.pack(pady=20)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to launch - Choose your version")
        
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief='sunken',
            anchor='w',
            font=("Arial", 10),
            bg='#2a2a4a',
            fg='#00ffff',
            bd=2
        )
        status_bar.pack(side='bottom', fill='x')
    
    def run_enhanced(self):
        """Run the enhanced version"""
        self.status_var.set("🚀 Launching Enhanced Version...")
        self.root.update()
        
        try:
            if os.path.exists('enhanced_face_attendance.py'):
                subprocess.Popen([sys.executable, 'enhanced_face_attendance.py'])
                self.root.destroy()
            else:
                messagebox.showerror("Error", "Enhanced version file not found!\nPlease ensure 'enhanced_face_attendance.py' is in the same directory.")
                self.status_var.set("❌ Enhanced version file not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch enhanced version: {str(e)}")
            self.status_var.set("❌ Launch failed")
    
    def run_basic(self):
        """Run the basic version"""
        self.status_var.set("📱 Launching Basic Version...")
        self.root.update()
        
        try:
            if os.path.exists('face_attendance_system.py'):
                subprocess.Popen([sys.executable, 'face_attendance_system.py'])
                self.root.destroy()
            else:
                messagebox.showerror("Error", "Basic version file not found!\nPlease ensure 'face_attendance_system.py' is in the same directory.")
                self.status_var.set("❌ Basic version file not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch basic version: {str(e)}")
            self.status_var.set("❌ Launch failed")

def main():
    root = tk.Tk()
    app = SystemLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()




