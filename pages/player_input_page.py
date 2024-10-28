"""
Player input page module for the Car Brand Quiz application.
"""
import customtkinter as ctk
from pages.base_page import BasePage


class PlayerInputPage(BasePage):
    def create_content(self):
        """Create the player input page content."""
        # Title
        self.create_label(
            self.frame,
            text="Enter your name",
            font_size=16,
            bold=True
        ).pack(pady=20)

        # Name entry
        self.name_entry = self.create_entry(
            self.frame,
            placeholder_text="Your name here...",
            width=200
        )
        self.name_entry.pack(pady=10)
        
        # Error message label (hidden initially)
        self.error_label = self.create_label(
            self.frame,
            text="",
            text_color="red"
        )
        self.error_label.pack_forget()

        # Start button
        self.create_button(
            self.frame,
            text="Start Game",
            command=self.validate_and_start,
            width=200
        ).pack(pady=10)

        # Set focus to name entry and bind Enter key
        self.name_entry.focus()
        self.name_entry.bind("<Return>", lambda e: self.validate_and_start())

    def validate_and_start(self):
        """Validate player name and start game if valid."""
        name = self.name_entry.get().strip()

        if not name:
            self.show_error("Please enter your name!")
            return

        if len(name) > 20:
            self.show_error("Name must be 20 characters or less!")
            return

        if not name.replace(" ", "").isalnum():
            self.show_error("Name can only contain letters, numbers, and spaces!")
            return

        # Hide error if validation passed
        self.error_label.pack_forget()
        
        # Start game with validated name
        self.game.start_game(name)

    def show_error(self, message):
        """Display error message."""
        self.error_label.configure(text=message)
        self.error_label.pack(pady=5)
        self.name_entry.focus()

    def reset(self):
        """Reset the page state."""
        super().reset()
        if hasattr(self, 'name_entry'):
            self.name_entry.delete(0, 'end')
        if hasattr(self, 'error_label'):
            self.error_label.pack_forget()
