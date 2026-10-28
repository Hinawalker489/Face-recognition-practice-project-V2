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

class FaceAttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1400x800")
        self.root.configure(bg='#1a1a2e')
        
        # Initialize variables
        self.cap = None
        self.is_capturing = False
        self.face_cascade = None
        self.known_faces = {}
        self.attendance_data = {}
        self.current_frame = None
        
        # Load face cascade
        self.load_face_cascade()
        
        # Create GUI
        self.create_gui()
        
        # Load existing data
        self.load_data()
        
    def load_face_cascade(self):
        """Load OpenCV face cascade classifier"""
        try:
            # Try to load from OpenCV data directory
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            if os.path.exists(cascade_path):
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
            else:
                # Fallback to basic face detection
                self.face_cascade = None
        except Exception as e:
            print(f"Error loading face cascade: {e}")
            self.face_cascade = None
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="Face Recognition Attendance System",
            font=("Arial", 24, "bold"),
            fg='#00d4ff',
            bg='#1a1a2e'
        )
        title_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Left panel - Camera and controls
        left_panel = tk.Frame(main_frame, bg='#16213e', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Camera frame
        camera_frame = tk.Frame(left_panel, bg='#0f3460', relief='sunken', bd=3)
        camera_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        self.camera_label = tk.Label(
            camera_frame,
            text="Camera Feed\nClick 'Start Camera' to begin",
            font=("Arial", 14),
            fg='#e94560',
            bg='#0f3460',
            width=50,
            height=20
        )
        self.camera_label.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Control buttons
        control_frame = tk.Frame(left_panel, bg='#16213e')
        control_frame.pack(pady=20, padx=20, fill='x')
        
        # Button styles
        button_style = {
            'font': ('Arial', 12, 'bold'),
            'bd': 0,
            'relief': 'flat',
            'width': 15,
            'height': 2,
            'cursor': 'hand2'
        }
        
        self.start_btn = tk.Button(
            control_frame,
            text="Start Camera",
            bg='#00d4ff',
            fg='white',
            command=self.start_camera,
            **button_style
        )
        self.start_btn.pack(side='left', padx=(0, 10))
        
        self.stop_btn = tk.Button(
            control_frame,
            text="Stop Camera",
            bg='#e94560',
            fg='white',
            command=self.stop_camera,
            state='disabled',
            **button_style
        )
        self.stop_btn.pack(side='left', padx=(0, 10))
        
        self.capture_btn = tk.Button(
            control_frame,
            text="Capture Face",
            bg='#00ff88',
            fg='white',
            command=self.capture_face,
            state='disabled',
            **button_style
        )
        self.capture_btn.pack(side='left', padx=(0, 10))
        
        # Center panel - Registration
        center_panel = tk.Frame(main_frame, bg='#16213e', relief='raised', bd=2)
        center_panel.pack(side='left', fill='both', expand=True, padx=10)
        
        # Registration section
        reg_frame = tk.LabelFrame(center_panel, text="Face Registration", 
                                font=("Arial", 14, "bold"), 
                                fg='#00d4ff', bg='#16213e', bd=2)
        reg_frame.pack(pady=20, padx=20, fill='x')
        
        # Name entry
        name_frame = tk.Frame(reg_frame, bg='#16213e')
        name_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(name_frame, text="Name:", font=("Arial", 12), 
                fg='white', bg='#16213e').pack(side='left')
        
        self.name_entry = tk.Entry(name_frame, font=("Arial", 12), width=20)
        self.name_entry.pack(side='right', padx=(10, 0))
        
        # ID entry
        id_frame = tk.Frame(reg_frame, bg='#16213e')
        id_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(id_frame, text="ID:", font=("Arial", 12), 
                fg='white', bg='#16213e').pack(side='left')
        
        self.id_entry = tk.Entry(id_frame, font=("Arial", 12), width=20)
        self.id_entry.pack(side='right', padx=(10, 0))
        
        # Register button
        self.register_btn = tk.Button(
            reg_frame,
            text="Register Face",
            bg='#00ff88',
            fg='white',
            command=self.register_face,
            font=("Arial", 12, "bold"),
            bd=0,
            relief='flat',
            cursor='hand2'
        )
        self.register_btn.pack(pady=10)
        
        # Registered Faces section
        faces_frame = tk.LabelFrame(center_panel, text="Registered Faces", 
                                  font=("Arial", 14, "bold"), 
                                  fg='#00d4ff', bg='#16213e', bd=2)
        faces_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Registered faces listbox
        self.faces_listbox = tk.Listbox(
            faces_frame,
            font=("Arial", 10),
            bg='#0f3460',
            fg='white',
            selectmode='single',
            height=15
        )
        self.faces_listbox.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Right panel - Attendance
        right_panel = tk.Frame(main_frame, bg='#16213e', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Attendance section
        att_frame = tk.LabelFrame(right_panel, text="Attendance Records", 
                                font=("Arial", 14, "bold"), 
                                fg='#00d4ff', bg='#16213e', bd=2)
        att_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Attendance listbox
        self.attendance_listbox = tk.Listbox(
            att_frame,
            font=("Arial", 10),
            bg='#0f3460',
            fg='white',
            selectmode='single',
            height=15
        )
        self.attendance_listbox.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Scrollbar for attendance
        att_scrollbar = tk.Scrollbar(att_frame, orient='vertical')
        att_scrollbar.pack(side='right', fill='y')
        
        self.attendance_listbox.config(yscrollcommand=att_scrollbar.set)
        att_scrollbar.config(command=self.attendance_listbox.yview)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to start")
        
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief='sunken',
            anchor='w',
            font=("Arial", 10),
            bg='#0f3460',
            fg='white'
        )
        status_bar.pack(side='bottom', fill='x')
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def start_camera(self):
        """Start the webcam"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open webcam")
                return
            
            self.is_capturing = True
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.capture_btn.config(state='normal')
            self.status_var.set("Camera started - Adjust your face position")
            
            # Start camera thread
            self.camera_thread = threading.Thread(target=self.update_camera)
            self.camera_thread.daemon = True
            self.camera_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
    
    def stop_camera(self):
        """Stop the webcam"""
        self.is_capturing = False
        if self.cap:
            self.cap.release()
        
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.capture_btn.config(state='disabled')
        self.status_var.set("Camera stopped")
        
        # Clear camera display
        self.camera_label.config(
            text="Camera Feed\nClick 'Start Camera' to begin",
            image=''
        )
    
    def update_camera(self):
        """Update camera feed in a separate thread"""
        while self.is_capturing:
            ret, frame = self.cap.read()
            if ret:
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Detect faces
                frame_with_faces = self.detect_faces(frame)
                
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
    
    def update_camera_display(self, photo):
        """Update camera display in main thread"""
        self.camera_label.config(image=photo)
        self.camera_label.image = photo  # Keep a reference
    
    def detect_faces(self, frame):
        """Detect faces in the frame and draw bounding boxes"""
        if self.face_cascade is None:
            return frame
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Draw bounding boxes around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, 'Face Detected', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # Show "DETECTED!" if we have registered faces
            if len(self.known_faces) > 0:
                cv2.putText(frame, 'DETECTED!', (x, y+h+25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.putText(frame, 'Face Matches Database', (x, y+h+50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame
    
    def capture_face(self):
        """Capture current frame for registration"""
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
            'filename': face_filename,
            'registered_date': datetime.datetime.now().isoformat()
        }
        
        # Save data
        self.save_data()
        
        # Update displays
        self.update_faces_display()
        self.update_attendance_display()
        
        messagebox.showinfo("Success", f"Face registered for {person_name}")
        
        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        
        self.status_var.set(f"Face registered for {person_name}")
    
    def register_face(self):
        """Register a new face"""
        if not self.name_entry.get().strip() or not self.id_entry.get().strip():
            messagebox.showwarning("Warning", "Please enter both name and ID")
            return
        
        if self.id_entry.get() in self.known_faces:
            messagebox.showwarning("Warning", "ID already exists")
            return
        
        # Enable capture button temporarily
        self.capture_btn.config(state='normal')
        self.status_var.set("Position your face and click 'Capture Face'")
    
    def update_faces_display(self):
        """Update the registered faces display"""
        self.faces_listbox.delete(0, tk.END)
        
        if not self.known_faces:
            self.faces_listbox.insert(tk.END, "No faces registered yet")
            return
        
        for person_id, data in self.known_faces.items():
            self.faces_listbox.insert(tk.END, f"ID: {person_id}")
            self.faces_listbox.insert(tk.END, f"  Name: {data['name']}")
            self.faces_listbox.insert(tk.END, f"  Date: {data['registered_date'][:10]}")
            self.faces_listbox.insert(tk.END, "")
    
    def mark_attendance(self, person_id):
        """Mark attendance for a person"""
        if person_id in self.known_faces:
            current_time = datetime.datetime.now()
            date_str = current_time.strftime("%Y-%m-%d")
            time_str = current_time.strftime("%H:%M:%S")
            
            if date_str not in self.attendance_data:
                self.attendance_data[date_str] = {}
            
            if person_id not in self.attendance_data[date_str]:
                self.attendance_data[date_str][person_id] = {
                    'name': self.known_faces[person_id]['name'],
                    'time': time_str,
                    'status': 'Present'
                }
                
                # Update attendance display
                self.update_attendance_display()
                self.save_data()
                
                self.status_var.set(f"Attendance marked for {self.known_faces[person_id]['name']}")
                return True
        
        return False
    
    def update_attendance_display(self):
        """Update the attendance display"""
        self.attendance_listbox.delete(0, tk.END)
        
        for date in sorted(self.attendance_data.keys(), reverse=True):
            self.attendance_listbox.insert(tk.END, f"=== {date} ===")
            for person_id, data in self.attendance_data[date].items():
                self.attendance_listbox.insert(tk.END, 
                    f"  {data['name']} ({person_id}) - {data['time']}")
            self.attendance_listbox.insert(tk.END, "")
    
    def load_data(self):
        """Load saved face and attendance data"""
        try:
            if os.path.exists('faces_data.json'):
                with open('faces_data.json', 'r') as f:
                    data = json.load(f)
                    self.known_faces = data.get('faces', {})
                    self.attendance_data = data.get('attendance', {})
                    self.update_faces_display()
                    self.update_attendance_display()
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def save_data(self):
        """Save face and attendance data"""
        try:
            data = {
                'faces': self.known_faces,
                'attendance': self.attendance_data
            }
            with open('faces_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_capturing:
            self.stop_camera()
        self.save_data()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = FaceAttendanceSystem(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
