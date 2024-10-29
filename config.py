"""
Configuration settings for the Car Brand Quiz application.
"""
import os

# Base paths using relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
DATA_DIR = os.path.join(ASSETS_DIR, 'data')

# Image directories
LOGO_DIR = os.path.join(IMAGES_DIR, 'logo')
CLUES_DIR = os.path.join(IMAGES_DIR, 'clues')

# Logo settings
LOGO_PATH = os.path.join(LOGO_DIR, 'python_logo.gif')
LOGO_SIZE = (60, 60)  # Width, Height for logo

# Database settings
DB_NAME = 'branddb.db'
DB_PATH = os.path.join(DATA_DIR, DB_NAME)

# Window settings
DEFAULT_WINDOW_SIZE = '640x600'
DEFAULT_WINDOW_POSITION = '+250+150'

# UI Theme settings
BACKGROUND_COLOR = "#2b2b2b"  # Dark background
BUTTON_COLOR = "#1f538d"      # Blue buttons
TEXT_COLOR = "#ffffff"        # White text
FRAME_COLOR = "#1e1e1e"      # Darker frame background
ERROR_COLOR = "#ff4444"      # Red for errors
SUCCESS_COLOR = "#44ff44"    # Green for success

# UI Component settings
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 120
BUTTON_CORNER_RADIUS = 0
FRAME_CORNER_RADIUS = 0

# Font settings
FONT_FAMILY = "Arial"
TITLE_FONT_SIZE = 20
NORMAL_FONT_SIZE = 12

# Image settings
CLUE_IMAGE_SIZE = (500, 300)  # Width, Height for clue images
LOGO_IMAGE_SIZE = (60, 60)    # Width, Height for logo

# Game settings
POINTS_FOR_CORRECT = 10
POINTS_FOR_CLUE = -5

def ensure_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        ASSETS_DIR,
        IMAGES_DIR,
        DATA_DIR,
        LOGO_DIR,
        CLUES_DIR
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def get_logo_path(filename):
    """Get the full path for a logo file."""
    return os.path.join(LOGO_DIR, filename)

def get_clue_path(filename):
    """Get the full path for a clue image file."""
    return os.path.join(CLUES_DIR, filename)

# Padding and spacing
PADDING = {
    'small': 5,
    'medium': 10,
    'large': 20,
    'xlarge': 30
}

# Content widths
CONTENT_WIDTH = {
    'small': 200,
    'medium': 300,
    'large': 400,
    'full': 620  # For full-width content like images
}

# Z-index levels for widget stacking
Z_INDEX = {
    'base': 0,
    'content': 1,
    'overlay': 2,
    'modal': 3
}
