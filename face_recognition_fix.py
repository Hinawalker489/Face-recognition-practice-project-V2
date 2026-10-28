#!/usr/bin/env python3
"""
Face Recognition Fix - This fixes the issue where all faces show the same person's data
"""

import cv2
import numpy as np
import os

def improved_face_recognition(frame, x, y, w, h, known_faces):
    """
    Improved face recognition that properly compares detected faces with stored data
    """
    try:
        if len(known_faces) == 0:
            return frame, None, None
        
        # Extract the face region from the current frame
        face_roi = frame[y:y+h, x:x+w]
        
        # Find the best matching face from our database
        best_match = None
        best_score = 0
        best_person_id = None
        
        for person_id, person_data in known_faces.items():
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
            
            return frame, best_person_id, best_match
        else:
            # Show "Unknown Face" if no good match found
            cv2.putText(frame, 'Unknown Face', (x, y+h+80), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.putText(frame, 'Not in database', (x, y+h+110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            return frame, None, None
            
    except Exception as e:
        print(f"❌ Face recognition error: {e}")
        # Fallback to showing "Unknown Face"
        cv2.putText(frame, 'Recognition Error', (x, y+h+80), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        return frame, None, None

# Example usage:
if __name__ == "__main__":
    print("Face Recognition Fix - Replace the try_face_recognition method with this logic")
    print("This will properly compare detected faces with stored face data")
    print("Instead of showing the first registered person for all faces")

