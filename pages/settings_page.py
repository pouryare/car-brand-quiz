"""
Settings page module for the Car Brand Quiz application.
Handles question management and game settings.
"""
import os
import customtkinter as ctk
from pages.base_page import BasePage
from config import TITLE_FONT_SIZE, CLUES_DIR
from utils.image_handler import ImageHandler


class SettingsPage(BasePage):
    def create_content(self):
        """Create the content for the settings page."""
        # Title
        self.create_label(
            self.frame,
            text="Question Management",
            font_size=TITLE_FONT_SIZE,
            bold=True
        ).pack(pady=(0, 20))

        # Description
        description_text = """Add new questions to the quiz database.
        Provide a question, select a clue image, and specify the correct answer."""
        
        self.create_label(
            self.frame,
            text=description_text,
            wraplength=400
        ).pack(pady=(0, 20))

        # Create form
        form_frame = ctk.CTkFrame(self.frame)
        form_frame.pack(padx=20, pady=10, fill="x")

        # Question input
        self.create_label(
            form_frame,
            text="Question:",
            bold=True
        ).pack(anchor="w", padx=20, pady=(10, 0))

        self.question_entry = self.create_entry(
            form_frame,
            placeholder_text="Enter the question...",
            width=400
        )
        self.question_entry.pack(padx=20, pady=(5, 10))

        # Image selection
        self.create_label(
            form_frame,
            text="Clue Image:",
            bold=True
        ).pack(anchor="w", padx=20, pady=(10, 0))

        # Image browsing frame
        image_frame = ctk.CTkFrame(form_frame)
        image_frame.pack(fill="x", padx=20, pady=(5, 10))

        self.image_path_var = ctk.StringVar()
        self.image_entry = self.create_entry(
            image_frame,
            placeholder_text="Select an image file...",
            width=300,
            textvariable=self.image_path_var,
            state="readonly"
        )
        self.image_entry.pack(side="left", padx=(0, 10))

        self.create_button(
            image_frame,
            text="Browse",
            command=self.browse_image,
            width=100
        ).pack(side="left")

        # Answer input
        self.create_label(
            form_frame,
            text="Correct Answer:",
            bold=True
        ).pack(anchor="w", padx=20, pady=(10, 0))

        self.answer_entry = self.create_entry(
            form_frame,
            placeholder_text="Enter the correct answer...",
            width=400
        )
        self.answer_entry.pack(padx=20, pady=(5, 20))

        # Message label (for success/error messages)
        self.message_label = self.create_label(
            self.frame,
            text="",
            font_size=12
        )
        self.message_label.pack(pady=10)

        # Buttons
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=20)

        self.create_button(
            button_frame,
            text="Add Question",
            command=self.save_question,
            width=120
        ).pack(side="left", padx=10)

        self.create_button(
            button_frame,
            text="Back to Home",
            command=self.go_back,
            width=120
        ).pack(side="left", padx=10)

    def browse_image(self):
        """Open file dialog to select a clue image."""
        file_types = (
            ('Image files', '*.png *.jpg *.jpeg *.gif *.bmp'),
            ('All files', '*.*')
        )
        
        filename = ctk.filedialog.askopenfilename(
            title='Select a clue image',
            filetypes=file_types,
            initialdir=CLUES_DIR
        )

        if filename:
            # Get just the filename, not the full path
            image_filename = os.path.basename(filename)
            
            # Check if the file is already in the clues directory
            if not os.path.exists(os.path.join(CLUES_DIR, image_filename)):
                # Copy the file to the clues directory
                try:
                    import shutil
                    shutil.copy2(filename, os.path.join(CLUES_DIR, image_filename))
                except Exception as e:
                    self.show_message(f"Error copying image: {e}", "red")
                    return
            
            self.image_path_var.set(image_filename)

    def save_question(self):
        """Validate and save the new question."""
        # Get values
        question = self.question_entry.get().strip()
        image_filename = self.image_path_var.get().strip()
        answer = self.answer_entry.get().strip()

        # Validate inputs
        if not question:
            self.show_message("Please enter a question", "red")
            return

        if not image_filename:
            self.show_message("Please select a clue image", "red")
            return

        if not answer:
            self.show_message("Please enter the correct answer", "red")
            return

        # Validate image exists
        if not ImageHandler.validate_image_path(image_filename):
            self.show_message("Selected image file is not accessible", "red")
            return

        # Save to database
        if self.game.db.insert_question(question, image_filename, {answer}):
            self.show_message("Question added successfully!", "green")
            self.clear_form()
        else:
            self.show_message("Error saving question", "red")

    def show_message(self, text, color="black"):
        """Display a message with the specified color."""
        self.message_label.configure(text=text, text_color=color)

    def clear_form(self):
        """Clear all form inputs."""
        self.question_entry.delete(0, 'end')
        self.image_path_var.set("")
        self.answer_entry.delete(0, 'end')

    def go_back(self):
        """Return to the home page."""
        self.hide()
        self.game.show_home()

    def reset(self):
        """Reset the page state."""
        self.clear_form()
        self.show_message("")
