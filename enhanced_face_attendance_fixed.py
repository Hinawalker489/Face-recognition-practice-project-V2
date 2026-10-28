#!/usr/bin/env python3
"""
Enhanced Face Recognition Attendance System - FIXED VERSION
This version addresses common issues that cause the system to get stuck
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import json
import datetime
import threading
import time

class EnhancedFaceAttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Face Recognition Attendance System - FIXED")
        self.root.geometry("1800x1000")
        self.root.configure(bg='#0f0f23')
        
        # Initialize variables
        self.cap = None
        self.is_capturing = False
        self.face_cascade = None
        self.known_faces = {}
        self.attendance_data = {}
        self.current_frame = None
        self.animation_frame = 0
        self.recognition_active = False
        
        # Load face cascade with error handling
        self.load_face_cascade()
        
        # Create GUI
        self.create_gui()
        
        # Load existing data
        self.load_data()
        
        # Start animation
        self.animate()
        
        # Add error handling for window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def load_face_cascade(self):
        """Load OpenCV face cascade classifier with better error handling"""
        try:
            print("Loading face cascade classifier...")
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            if os.path.exists(cascade_path):
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
                if self.face_cascade.empty():
                    print("❌ Failed to load cascade classifier")
                    self.face_cascade = None
                else:
                    print("✅ Face cascade loaded successfully")
            else:
                print(f"❌ Cascade file not found at: {cascade_path}")
                self.face_cascade = None
        except Exception as e:
            print(f"❌ Error loading face cascade: {e}")
            self.face_cascade = None
    
    def create_gui(self):
        """Create the enhanced GUI interface"""
        print("Creating GUI...")
        
        # Main title with animation
        title_frame = tk.Frame(self.root, bg='#0f0f23')
        title_frame.pack(pady=20)
        
        self.title_label = tk.Label(
            title_frame,
            text="Enhanced Face Recognition Attendance System",
            font=("Arial", 28, "bold"),
            fg='#00ffff',
            bg='#0f0f23'
        )
        self.title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            title_frame,
            text="AI-Powered Attendance Management - FIXED VERSION",
            font=("Arial", 14),
            fg='#8888ff',
            bg='#0f0f23'
        )
        subtitle_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#0f0f23')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Left panel - Camera and controls
        left_panel = tk.Frame(main_frame, bg='#1a1a3a', relief='raised', bd=3)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Camera frame with border
        camera_frame = tk.Frame(left_panel, bg='#2a2a4a', relief='sunken', bd=4)
        camera_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Camera title
        camera_title = tk.Label(
            camera_frame,
            text="Live Camera Feed",
            font=("Arial", 16, "bold"),
            fg='#00ffff',
            bg='#2a2a4a'
        )
        camera_title.pack(pady=(10, 5))
        
        self.camera_label = tk.Label(
            camera_frame,
            text="Click 'Start Camera' to begin\n\nPosition your face in the center\n\nEnsure good lighting",
            font=("Arial", 12),
            fg='#ff8888',
            bg='#2a2a4a',
            width=60,
            height=25,
            justify='center'
        )
        self.camera_label.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Control buttons with modern design
        control_frame = tk.Frame(left_panel, bg='#1a1a3a')
        control_frame.pack(pady=20, padx=20, fill='x')
        
        # Button styles
        button_style = {
            'font': ('Arial', 12, 'bold'),
            'bd': 0,
            'relief': 'flat',
            'width': 18,
            'height': 2,
            'cursor': 'hand2',
            'activebackground': '#4444aa'
        }
        
        self.start_btn = tk.Button(
            control_frame,
            text="🚀 Start Camera",
            bg='#00aa44',
            fg='white',
            command=self.start_camera,
            **button_style
        )
        self.start_btn.pack(side='left', padx=(0, 10))
        
        self.stop_btn = tk.Button(
            control_frame,
            text="⏹️ Stop Camera",
            bg='#aa4444',
            fg='white',
            command=self.stop_camera,
            state='disabled',
            **button_style
        )
        self.stop_btn.pack(side='left', padx=(0, 10))
        
        self.capture_btn = tk.Button(
            control_frame,
            text="📸 Capture Face",
            bg='#aa8800',
            fg='white',
            command=self.capture_face,
            state='disabled',
            **button_style
        )
        self.capture_btn.pack(side='left', padx=(0, 10))
        
        # Recognition toggle
        self.recognition_btn = tk.Button(
            control_frame,
            text="🔍 Start Recognition",
            bg='#8844aa',
            fg='white',
            command=self.toggle_recognition,
            state='disabled',
            **button_style
        )
        self.recognition_btn.pack(side='left', padx=(0, 10))
        
        # Center panel - Registration
        center_panel = tk.Frame(main_frame, bg='#1a1a3a', relief='raised', bd=3, width=400)
        center_panel.pack(side='left', fill='y', padx=10)
        center_panel.pack_propagate(False)
        
        # Registration section
        reg_frame = tk.LabelFrame(center_panel, text="👤 Face Registration", 
                                font=("Arial", 16, "bold"), 
                                fg='#00ffff', bg='#1a1a3a', bd=2)
        reg_frame.pack(pady=20, padx=20, fill='x')
        
        # Name entry
        name_frame = tk.Frame(reg_frame, bg='#1a1a3a')
        name_frame.pack(pady=15, padx=15, fill='x')
        
        tk.Label(name_frame, text="👤 Name:", font=("Arial", 12, "bold"), 
                fg='#00ff88', bg='#1a1a3a').pack(side='left')
        
        self.name_entry = tk.Entry(name_frame, font=("Arial", 12), width=25,
                                 bg='#2a2a4a', fg='white', insertbackground='#00ffff')
        self.name_entry.pack(side='right', padx=(15, 0))
        
        # ID entry
        id_frame = tk.Frame(reg_frame, bg='#1a1a3a')
        id_frame.pack(pady=15, padx=15, fill='x')
        
        tk.Label(id_frame, text="🆔 ID:", font=("Arial", 12, "bold"), 
                fg='#00ff88', bg='#1a1a3a').pack(side='left')
        
        self.id_entry = tk.Entry(id_frame, font=("Arial", 12), width=25,
                               bg='#2a2a4a', fg='white', insertbackground='#00ffff')
        self.id_entry.pack(side='right', padx=(15, 0))
        
        # Department entry
        dept_frame = tk.Frame(reg_frame, bg='#1a1a3a')
        dept_frame.pack(pady=15, padx=15, fill='x')
        
        tk.Label(dept_frame, text="🏢 Department:", font=("Arial", 12, "bold"), 
                fg='#00ff88', bg='#1a1a3a').pack(side='left')
        
        self.dept_entry = tk.Entry(dept_frame, font=("Arial", 12), width=25,
                                 bg='#2a2a4a', fg='white', insertbackground='#00ffff')
        self.dept_entry.pack(side='right', padx=(15, 0))
        
        # Register button
        self.register_btn = tk.Button(
            reg_frame,
            text="✅ Register New Face",
            bg='#00aa44',
            fg='white',
            command=self.register_face,
            font=("Arial", 12, "bold"),
            bd=0,
            relief='flat',
            cursor='hand2',
            width=20,
            height=2
        )
        self.register_btn.pack(pady=15)
        
        # Registered Faces section
        faces_frame = tk.LabelFrame(center_panel, text="👥 Registered Faces", 
                                  font=("Arial", 16, "bold"), 
                                  fg='#00ffff', bg='#1a1a3a', bd=2)
        faces_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Registered faces listbox
        faces_listbox_frame = tk.Frame(faces_frame, bg='#2a2a4a')
        faces_listbox_frame.pack(pady=10, padx=15, fill='both', expand=True)
        
        self.faces_listbox = tk.Listbox(
            faces_listbox_frame,
            font=("Consolas", 10),
            bg='#1a1a3a',
            fg='#00ff88',
            selectmode='single',
            height=15,
            width=50,
            selectbackground='#4444aa',
            selectforeground='white'
        )
        self.faces_listbox.pack(side='left', fill='both', expand=True)
        
        # Scrollbar for faces
        faces_scrollbar = tk.Scrollbar(faces_listbox_frame, orient='vertical')
        faces_scrollbar.pack(side='right', fill='y')
        
        self.faces_listbox.config(yscrollcommand=faces_scrollbar.set)
        faces_scrollbar.config(command=self.faces_listbox.yview)
        
        # Right panel - Attendance
        right_panel = tk.Frame(main_frame, bg='#1a1a3a', relief='raised', bd=3, width=700)
        right_panel.pack(side='right', fill='y', padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Attendance section
        att_frame = tk.LabelFrame(right_panel, text="📊 Attendance Records", 
                                font=("Arial", 16, "bold"), 
                                fg='#00ffff', bg='#1a1a3a', bd=2)
        att_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Attendance controls
        att_control_frame = tk.Frame(att_frame, bg='#1a1a3a')
        att_control_frame.pack(pady=10, padx=15, fill='x')
        
        self.export_btn = tk.Button(
            att_control_frame,
            text="📤 Export Data",
            bg='#8844aa',
            fg='white',
            command=self.export_attendance,
            font=("Arial", 10, "bold"),
            bd=0,
            relief='flat',
            cursor='hand2'
        )
        self.export_btn.pack(side='right')
        
        # Attendance listbox with modern styling
        listbox_frame = tk.Frame(att_frame, bg='#2a2a4a')
        listbox_frame.pack(pady=10, padx=15, fill='both', expand=True)
        
        self.attendance_listbox = tk.Listbox(
            listbox_frame,
            font=("Consolas", 10),
            bg='#1a1a3a',
            fg='#00ff88',
            selectmode='single',
            height=20,
            width=80,
            selectbackground='#4444aa',
            selectforeground='white'
        )
        self.attendance_listbox.pack(side='left', fill='both', expand=True)
        
        # Scrollbar for attendance
        att_scrollbar = tk.Scrollbar(listbox_frame, orient='vertical')
        att_scrollbar.pack(side='right', fill='y')
        
        self.attendance_listbox.config(yscrollcommand=att_scrollbar.set)
        att_scrollbar.config(command=self.attendance_listbox.yview)
        
        # Status bar with animation
        self.status_var = tk.StringVar()
        self.status_var.set("🚀 System Ready - Start camera to begin")
        
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief='sunken',
            anchor='w',
            font=("Arial", 11, "bold"),
            bg='#2a2a4a',
            fg='#00ffff',
            bd=2
        )
        status_bar.pack(side='bottom', fill='x')
        
        print("✅ GUI created successfully")
        
    def animate(self):
        """Animate the title and other elements"""
        try:
            self.animation_frame += 1
            
            # Animate title color
            colors = ['#00ffff', '#00ff88', '#ff8800', '#ff0088', '#8800ff']
            color_index = (self.animation_frame // 30) % len(colors)
            self.title_label.config(fg=colors[color_index])
            
            # Schedule next animation
            self.root.after(50, self.animate)
        except Exception as e:
            print(f"Animation error: {e}")
    
    def start_camera(self):
        """Start the webcam with better error handling"""
        try:
            print("Starting camera...")
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open webcam")
                print("❌ Camera failed to open")
                return
            
            self.is_capturing = True
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.capture_btn.config(state='normal')
            self.recognition_btn.config(state='normal')
            self.status_var.set("📹 Camera started - Position your face in the center")
            
            print("✅ Camera started successfully")
            
            # Start camera thread
            self.camera_thread = threading.Thread(target=self.update_camera, daemon=True)
            self.camera_thread.start()
            
        except Exception as e:
            error_msg = f"Failed to start camera: {str(e)}"
            messagebox.showerror("Error", error_msg)
            print(f"❌ {error_msg}")
    
    def stop_camera(self):
        """Stop the webcam"""
        try:
            print("Stopping camera...")
            self.is_capturing = False
            self.recognition_active = False
            if self.cap:
                self.cap.release()
            
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.capture_btn.config(state='disabled')
            self.recognition_btn.config(state='disabled', text="🔍 Start Recognition")
            self.status_var.set("⏹️ Camera stopped")
            
            # Clear camera display
            self.camera_label.config(
                text="Click 'Start Camera' to begin\n\nPosition your face in the center\n\nEnsure good lighting",
                image=''
            )
            print("✅ Camera stopped successfully")
        except Exception as e:
            print(f"❌ Error stopping camera: {e}")
    
    def toggle_recognition(self):
        """Toggle face recognition mode"""
        try:
            if not self.recognition_active:
                self.recognition_active = True
                self.recognition_btn.config(text="⏸️ Stop Recognition", bg='#aa4444')
                self.status_var.set("🔍 Recognition active - Looking for known faces")
                print("✅ Recognition started")
            else:
                self.recognition_active = False
                self.recognition_btn.config(text="🔍 Start Recognition", bg='#8844aa')
                self.status_var.set("📹 Camera active - Recognition stopped")
                print("⏸️ Recognition stopped")
        except Exception as e:
            print(f"❌ Error toggling recognition: {e}")
    
    def update_camera(self):
        """Update camera feed in a separate thread"""
        print("Camera thread started")
        while self.is_capturing:
            try:
                ret, frame = self.cap.read()
                if ret:
                    # Flip frame horizontally for mirror effect
                    frame = cv2.flip(frame, 1)
                    
                    # Detect faces and process
                    frame_with_faces = self.process_frame(frame)
                    
                    # Convert to PIL format
                    frame_rgb = cv2.cvtColor(frame_with_faces, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(frame_rgb)
                    
                    # Resize for display
                    display_size = (640, 480)
                    pil_image = pil_image.resize(display_size, Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(pil_image)
                    
                    # Update GUI in main thread
                    self.root.after(0, self.update_camera_display, photo)
                    
                    # Store current frame
                    self.current_frame = frame
                    
                time.sleep(0.03)  # ~30 FPS
            except Exception as e:
                print(f"❌ Camera update error: {e}")
                time.sleep(0.1)
        
        print("Camera thread ended")
    
    def process_frame(self, frame):
        """Process frame for face detection and recognition"""
        try:
            if self.face_cascade is None:
                return frame
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            # Draw bounding boxes and process faces
            for (x, y, w, h) in faces:
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Add face detection label
                cv2.putText(frame, 'Face Detected', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                # If recognition is active, try to identify the face
                if self.recognition_active:
                    self.try_face_recognition(frame, x, y, w, h)
                else:
                    # Show guidance text only when recognition is not active
                    cv2.putText(frame, 'Position face here', (x, y+h+25), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    cv2.putText(frame, 'Start Recognition to identify', (x, y+h+50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            return frame
        except Exception as e:
            print(f"❌ Frame processing error: {e}")
            return frame
    
    def try_face_recognition(self, frame, x, y, w, h):
        """Attempt to recognize the detected face"""
        try:
            if len(self.known_faces) == 0:
                return
            
            # Extract the face region from the current frame
            face_roi = frame[y:y+h, x:x+w]
            
            # Find the best matching face from our database
            best_match = None
            best_score = 0
            best_person_id = None
            
            for person_id, person_data in self.known_faces.items():
                if 'filename' in person_data and os.path.exists(person_data['filename']):
                    # Load the stored face image
                    stored_face = cv2.imread(person_data['filename'])
                    if stored_face is not None:
                        # Resize stored face to match detected face size
                        stored_face_resized = cv2.resize(stored_face, (w, h))
                        
                        # Convert both faces to grayscale for comparison
                        detected_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
                        stored_gray = cv2.cvtColor(stored_face_resized, cv2.COLOR_BGR2GRAY)
                        
                        # Calculate similarity using template matching
                        result = cv2.matchTemplate(detected_gray, stored_gray, cv2.TM_CCOEFF_NORMED)
                        score = result[0][0]
                        
                        # Update best match if this score is higher
                        if score > best_score:
                            best_score = score
                            best_match = person_data
                            best_person_id = person_id
            
            # If we found a good match (threshold can be adjusted)
            if best_match and best_score > 0.3:  # Adjust this threshold as needed
                # Show "Face Recognized" status
                cv2.putText(frame, 'Face Recognized!', (x, y+h+80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                # Show person's name under the face box
                cv2.putText(frame, f"Name: {best_match['name']}", (x, y+h+110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Show person's ID
                cv2.putText(frame, f"ID: {best_person_id}", (x, y+h+140), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Show department if available
                if 'department' in best_match:
                    cv2.putText(frame, f"Dept: {best_match['department']}", (x, y+h+170), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Show confidence score
                cv2.putText(frame, f"Match: {best_score:.2f}", (x, y+h+200), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Automatically mark attendance for the recognized person
                self.auto_mark_attendance_for_person(best_person_id, best_match)
            else:
                # Show "Unknown Face" if no good match found
                cv2.putText(frame, 'Unknown Face', (x, y+h+80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.putText(frame, 'Not in database', (x, y+h+110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                
        except Exception as e:
            print(f"❌ Face recognition error: {e}")
            # Fallback to showing "Unknown Face"
            cv2.putText(frame, 'Recognition Error', (x, y+h+80), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    def auto_mark_attendance_for_person(self, person_id, person_data):
        """Automatically mark attendance for a specific recognized person"""
        try:
            if not self.recognition_active:
                return
                
            current_time = datetime.datetime.now()
            date_str = current_time.strftime("%Y-%m-%d")
            time_str = current_time.strftime("%H:%M:%S")
            
            # Mark attendance for the specific recognized person
            if date_str not in self.attendance_data:
                self.attendance_data[date_str] = {}
            
            # Only mark if not already marked today
            if person_id not in self.attendance_data[date_str]:
                self.attendance_data[date_str][person_id] = {
                    'name': person_data['name'],
                    'time': time_str,
                    'status': 'Present'
                }
                
                # Update attendance display
                self.update_attendance_display()
                self.save_data()
                
                # Update status with specific person info
                self.status_var.set(f"✅ {person_data['name']} ({person_id}) marked present at {time_str}")
                
                # Schedule status reset after 5 seconds
                self.root.after(5000, lambda: self.status_var.set("🔍 Recognition active - Looking for known faces"))
        except Exception as e:
            print(f"❌ Attendance marking error: {e}")
    
    def update_camera_display(self, photo):
        """Update camera display in main thread"""
        try:
            self.camera_label.config(image=photo)
            self.camera_label.image = photo  # Keep a reference
        except Exception as e:
            print(f"❌ Camera display update error: {e}")
    
    def capture_face(self):
        """Capture current frame for registration"""
        try:
            if self.current_frame is None:
                messagebox.showwarning("Warning", "No frame available. Please start camera first.")
                return
            
            if not self.name_entry.get().strip() or not self.id_entry.get().strip():
                messagebox.showwarning("Warning", "Please enter both name and ID")
                return
            
            # Create faces directory if it doesn't exist
            if not os.path.exists('faces'):
                os.makedirs('faces')
            
            # Save face image
            face_filename = f"faces/{self.id_entry.get()}_{self.name_entry.get()}.jpg"
            cv2.imwrite(face_filename, self.current_frame)
            
            # Store face data
            person_id = self.id_entry.get()
            person_name = self.name_entry.get()
            
            self.known_faces[person_id] = {
                'name': person_name,
                'department': self.dept_entry.get() or 'General',
                'filename': face_filename,
                'registered_date': datetime.datetime.now().isoformat()
            }
            
            # Save data
            self.save_data()
            
            # Update displays
            self.update_faces_display()
            self.update_attendance_display()
            
            messagebox.showinfo("Success", f"✅ Face registered for {person_name}")
            
            # Clear entries
            self.name_entry.delete(0, tk.END)
            self.id_entry.delete(0, tk.END)
            self.dept_entry.delete(0, tk.END)
            
            self.status_var.set(f"✅ Face registered for {person_name}")
            print(f"✅ Face registered for {person_name}")
        except Exception as e:
            error_msg = f"Error capturing face: {str(e)}"
            messagebox.showerror("Error", error_msg)
            print(f"❌ {error_msg}")
    
    def register_face(self):
        """Register a new face"""
        try:
            if not self.name_entry.get().strip() or not self.id_entry.get().strip():
                messagebox.showwarning("Warning", "Please enter both name and ID")
                return
            
            if self.id_entry.get() in self.known_faces:
                messagebox.showwarning("Warning", "ID already exists")
                return
            
            # Enable capture button temporarily
            self.capture_btn.config(state='normal')
            self.status_var.set("📸 Position your face and click 'Capture Face'")
            print("✅ Registration mode enabled")
        except Exception as e:
            print(f"❌ Registration error: {e}")
    
    def update_faces_display(self):
        """Update the registered faces display"""
        try:
            self.faces_listbox.delete(0, tk.END)
            
            if not self.known_faces:
                self.faces_listbox.insert(tk.END, "No faces registered yet")
                return
            
            for person_id, data in self.known_faces.items():
                self.faces_listbox.insert(tk.END, f"🆔 {person_id}")
                self.faces_listbox.insert(tk.END, f"  👤 {data['name']}")
                self.faces_listbox.insert(tk.END, f"  🏢 {data['department']}")
                self.faces_listbox.insert(tk.END, f"  📅 {data['registered_date'][:10]}")
                self.faces_listbox.insert(tk.END, "")
        except Exception as e:
            print(f"❌ Faces display update error: {e}")
    
    def update_attendance_display(self):
        """Update the attendance display"""
        try:
            self.attendance_listbox.delete(0, tk.END)
            
            for date in sorted(self.attendance_data.keys(), reverse=True):
                self.attendance_listbox.insert(tk.END, f"=== {date} ===")
                for person_id, data in self.attendance_data[date].items():
                    self.attendance_listbox.insert(tk.END, 
                        f"  {data['name']} ({person_id}) - {data['time']}")
                self.attendance_listbox.insert(tk.END, "")
        except Exception as e:
            print(f"❌ Attendance display update error: {e}")
    
    def export_attendance(self):
        """Export attendance data to CSV"""
        try:
            if not self.attendance_data:
                messagebox.showwarning("Warning", "No attendance data to export")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', newline='') as csvfile:
                    csvfile.write("Date,ID,Name,Department,Time,Status\n")
                    for date in self.attendance_data:
                        for person_id, data in self.attendance_data[date].items():
                            dept = self.known_faces.get(person_id, {}).get('department', 'Unknown')
                            csvfile.write(f"{date},{person_id},{data['name']},{dept},{data['time']},{data['status']}\n")
                
                messagebox.showinfo("Success", f"Attendance data exported to {filename}")
                print(f"✅ Data exported to {filename}")
        except Exception as e:
            error_msg = f"Failed to export data: {str(e)}"
            messagebox.showerror("Error", error_msg)
            print(f"❌ {error_msg}")
    
    def load_data(self):
        """Load saved face and attendance data"""
        try:
            print("Loading saved data...")
            if os.path.exists('faces_data.json'):
                with open('faces_data.json', 'r') as f:
                    data = json.load(f)
                    self.known_faces = data.get('faces', {})
                    self.attendance_data = data.get('attendance', {})
                    self.update_faces_display()
                    self.update_attendance_display()
                print(f"✅ Loaded {len(self.known_faces)} faces and {len(self.attendance_data)} attendance records")
            else:
                print("ℹ️ No existing data found - starting fresh")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
    
    def save_data(self):
        """Save face and attendance data"""
        try:
            data = {
                'faces': self.known_faces,
                'attendance': self.attendance_data
            }
            with open('faces_data.json', 'w') as f:
                json.dump(data, f, indent=2)
            print("✅ Data saved successfully")
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        try:
            print("Closing application...")
            if self.is_capturing:
                self.stop_camera()
            self.save_data()
            print("✅ Application closed successfully")
            self.root.destroy()
        except Exception as e:
            print(f"❌ Error during shutdown: {e}")
            self.root.destroy()

def main():
    """Main function with error handling"""
    try:
        print("🚀 Starting Enhanced Face Recognition Attendance System...")
        print("=" * 60)
        
        # Create root window
        root = tk.Tk()
        
        # Create application
        app = EnhancedFaceAttendanceSystem(root)
        
        # Center the window
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        print("✅ System initialized successfully!")
        print("🎯 Ready to use - GUI should be visible now")
        print("=" * 60)
        
        # Start main loop
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("Please check the error message above and try again.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
