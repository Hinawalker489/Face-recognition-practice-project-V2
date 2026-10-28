"""
Configuration file for Enhanced Face Recognition Attendance System
Modify these settings to customize the system behavior
"""

# =============================================================================
# DISPLAY SETTINGS
# =============================================================================

# Window dimensions
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000

# Panel widths
LEFT_PANEL_WIDTH = "flexible"  # Camera panel - expands to fill available space
CENTER_PANEL_WIDTH = 400       # Registration panel - fixed width
RIGHT_PANEL_WIDTH = 700        # Attendance panel - fixed width

# Camera display size
CAMERA_DISPLAY_WIDTH = 640
CAMERA_DISPLAY_HEIGHT = 480

# =============================================================================
# COLORS AND THEMES
# =============================================================================

# Main color scheme
COLORS = {
    'background': '#0f0f23',           # Main background
    'panel': '#1a1a3a',               # Panel backgrounds
    'subpanel': '#2a2a4a',            # Sub-panel backgrounds
    'title': '#00ffff',                # Title color
    'subtitle': '#8888ff',             # Subtitle color
    'accent_green': '#00ff88',         # Green accents
    'accent_yellow': '#ff8800',        # Yellow accents
    'accent_red': '#ff8888',           # Red accents
    'accent_purple': '#8844aa',        # Purple accents
    'text_white': '#ffffff',           # White text
    'button_active': '#4444aa',        # Button active state
}

# Button colors
BUTTON_COLORS = {
    'start': '#00aa44',                # Start button (green)
    'stop': '#aa4444',                 # Stop button (red)
    'capture': '#aa8800',              # Capture button (yellow)
    'recognition': '#8844aa',          # Recognition button (purple)
    'export': '#8844aa',               # Export button (purple)
}

# =============================================================================
# FACE DETECTION SETTINGS
# =============================================================================

# OpenCV face detection parameters
FACE_DETECTION = {
    'scale_factor': 1.1,               # Scale factor for face detection
    'min_neighbors': 5,                # Minimum neighbors for detection
    'min_size': (30, 30),              # Minimum face size
    'max_size': None,                  # Maximum face size (None = no limit)
}

# Camera settings
CAMERA = {
    'fps': 30,                         # Target frames per second
    'flip_horizontal': True,           # Mirror effect for natural experience
    'camera_index': 0,                 # Default camera (0 = built-in)
}

# =============================================================================
# RECOGNITION SETTINGS
# =============================================================================

# Face recognition parameters
RECOGNITION = {
    'confidence_threshold': 0.6,        # Minimum confidence for recognition
    'max_recognition_distance': 0.6,   # Maximum distance for face matching
    'recognition_delay': 2.0,          # Delay before showing recognition result
}

# =============================================================================
# DATA STORAGE SETTINGS
# =============================================================================

# File paths
PATHS = {
    'faces_directory': 'faces',         # Directory for storing face images
    'data_file': 'faces_data.json',    # JSON file for face and attendance data
    'export_directory': 'exports',      # Directory for exported data
}

# Data retention
DATA_RETENTION = {
    'max_face_images': 1000,           # Maximum number of face images to store
    'attendance_history_days': 365,    # Days to keep attendance history
    'auto_cleanup': True,              # Automatically clean old data
}

# =============================================================================
# UI CUSTOMIZATION
# =============================================================================

# Font settings
FONTS = {
    'title': ('Arial', 28, 'bold'),
    'subtitle': ('Arial', 14),
    'heading': ('Arial', 16, 'bold'),
    'body': ('Arial', 12),
    'small': ('Arial', 10),
    'monospace': ('Consolas', 10),
}

# Animation settings
ANIMATION = {
    'title_color_cycle': True,         # Enable title color animation
    'animation_speed': 50,             # Animation update interval (ms)
    'color_cycle_speed': 30,           # Color change speed (frames)
}

# =============================================================================
# EXPORT SETTINGS
# =============================================================================

# CSV export options
CSV_EXPORT = {
    'include_headers': True,           # Include column headers
    'date_format': '%Y-%m-%d',        # Date format for export
    'time_format': '%H:%M:%S',        # Time format for export
    'separator': ',',                  # CSV field separator
}

# =============================================================================
# ADVANCED SETTINGS
# =============================================================================

# Performance settings
PERFORMANCE = {
    'enable_multithreading': True,     # Enable camera threading
    'camera_buffer_size': 3,          # Camera frame buffer size
    'memory_optimization': True,       # Enable memory optimization
}

# Debug settings
DEBUG = {
    'show_fps': False,                 # Show FPS counter
    'log_level': 'INFO',               # Logging level (DEBUG, INFO, WARNING, ERROR)
    'save_debug_frames': False,        # Save debug camera frames
}

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Check color values
    for color_name, color_value in COLORS.items():
        if not color_value.startswith('#') or len(color_value) != 7:
            errors.append(f"Invalid color format for {color_name}: {color_value}")
    
    # Check dimensions
    if WINDOW_WIDTH < 1200 or WINDOW_HEIGHT < 800:
        errors.append("Window dimensions too small")
    
    # Check camera settings
    if CAMERA['fps'] < 1 or CAMERA['fps'] > 60:
        errors.append("Invalid FPS value")
    
    # Check face detection parameters
    if FACE_DETECTION['scale_factor'] <= 1.0:
        errors.append("Scale factor must be greater than 1.0")
    
    if errors:
        print("Configuration errors found:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True

# =============================================================================
# CONFIGURATION PRESETS
# =============================================================================

# High performance preset
HIGH_PERFORMANCE = {
    'camera_fps': 60,
    'camera_buffer_size': 5,
    'memory_optimization': True,
    'enable_multithreading': True,
}

# Low resource preset
LOW_RESOURCE = {
    'camera_fps': 15,
    'camera_buffer_size': 1,
    'memory_optimization': True,
    'enable_multithreading': False,
}

# Production preset
PRODUCTION = {
    'debug_show_fps': False,
    'debug_log_level': 'WARNING',
    'debug_save_debug_frames': False,
    'data_auto_cleanup': True,
}

# Development preset
DEVELOPMENT = {
    'debug_show_fps': True,
    'debug_log_level': 'DEBUG',
    'debug_save_debug_frames': True,
    'data_auto_cleanup': False,
}

# =============================================================================
# LOAD CONFIGURATION
# =============================================================================

def load_preset(preset_name):
    """Load a configuration preset"""
    presets = {
        'high_performance': HIGH_PERFORMANCE,
        'low_resource': LOW_RESOURCE,
        'production': PRODUCTION,
        'development': DEVELOPMENT,
    }
    
    if preset_name in presets:
        print(f"Loading {preset_name} preset...")
        return presets[preset_name]
    else:
        print(f"Unknown preset: {preset_name}")
        return {}

# Validate configuration on import
if __name__ == "__main__":
    if validate_config():
        print("✅ Configuration is valid!")
    else:
        print("❌ Configuration has errors!")
else:
    # Auto-validate when imported
    validate_config()




