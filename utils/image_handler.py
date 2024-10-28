"""
Utility functions for handling images in the Car Brand Quiz application.
"""
import os
import shutil
from PIL import Image
from config import CLUES_DIR, CLUE_IMAGE_SIZE


class ImageHandler:
    @staticmethod
    def validate_image_file(file_path):
        """
        Validate if a file is a valid image file.
        """
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except Exception:
            return False

    @staticmethod
    def copy_to_clues(source_path):
        """
        Copy an image file to the clues directory.
        """
        try:
            if not ImageHandler.validate_image_file(source_path):
                return None

            filename = os.path.basename(source_path)
            base, ext = os.path.splitext(filename)
            counter = 1
            
            while os.path.exists(os.path.join(CLUES_DIR, filename)):
                filename = f"{base}_{counter}{ext}"
                counter += 1

            destination = os.path.join(CLUES_DIR, filename)
            shutil.copy2(source_path, destination)

            # Resize image if needed
            with Image.open(destination) as img:
                img = img.convert('RGB')
                img.thumbnail(CLUE_IMAGE_SIZE)
                img.save(destination, quality=95, optimize=True)

            return filename

        except Exception as e:
            print(f"Error copying image: {e}")
            return None

    @staticmethod
    def get_supported_formats():
        """Get list of supported image formats."""
        return ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    @staticmethod
    def is_valid_extension(filename):
        """Check if filename has a supported image extension."""
        ext = os.path.splitext(filename)[1].lower()
        return ext in ImageHandler.get_supported_formats()

    @staticmethod
    def validate_image_in_clues(filename):
        """Check if an image exists in the clues directory."""
        if not filename:
            return False
            
        file_path = os.path.join(CLUES_DIR, filename)
        return os.path.exists(file_path) and ImageHandler.validate_image_file(file_path)
