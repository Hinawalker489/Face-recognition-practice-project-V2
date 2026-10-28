#!/usr/bin/env python3
"""
Script to apply the face recognition fix to the existing file
"""

def apply_face_recognition_fix():
    """Apply the face recognition fix to the existing file"""
    
    # Read the existing file
    try:
        with open('enhanced_face_attendance_fixed.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Successfully read the existing file")
        
        # Find the old try_face_recognition method
        old_method_start = content.find('    def try_face_recognition(self, frame, x, y, w, h):')
        if old_method_start == -1:
            print("❌ Could not find the try_face_recognition method")
            return False
        
        # Find the end of the old method (next method or end of class)
        old_method_end = content.find('    def auto_mark_attendance_for_person', old_method_start)
        if old_method_end == -1:
            old_method_end = content.find('    def ', old_method_start + 1)
        
        if old_method_end == -1:
            print("❌ Could not find the end of the try_face_recognition method")
            return False
        
        # Create the new method content
        new_method = '''    def try_face_recognition(self, frame, x, y, w, h):
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
'''
        
        # Replace the old method with the new one
        new_content = content[:old_method_start] + new_method + content[old_method_end:]
        
        # Write the updated content back to the file
        with open('enhanced_face_attendance_fixed.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Successfully applied the face recognition fix!")
        print("🎯 Now each face will be properly recognized with its own data")
        print("📝 The system will compare detected faces with stored face images")
        print("🔍 Unknown faces will show 'Unknown Face' instead of wrong data")
        
        return True
        
    except Exception as e:
        print(f"❌ Error applying fix: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Applying Face Recognition Fix...")
    print("=" * 50)
    
    if apply_face_recognition_fix():
        print("\n✅ Fix applied successfully!")
        print("🚀 You can now run the system and it will properly recognize faces")
    else:
        print("\n❌ Failed to apply the fix")
        print("💡 You may need to manually replace the try_face_recognition method")

