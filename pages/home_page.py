"""
Home page module for the Car Brand Quiz application.
"""
import customtkinter as ctk
from pages.base_page import BasePage
from config import TITLE_FONT_SIZE, NORMAL_FONT_SIZE


class HomePage(BasePage):
    def create_content(self):
        """Create the content for the home page."""
        # Welcome title
        self.create_label(
            self.frame,
            text="Welcome to Car Brand Quiz!",
            font_size=TITLE_FONT_SIZE,
            bold=True
        ).pack(pady=(0, 20))

        # Welcome message
        welcome_text = """
        Welcome to the Car Brand Quiz Challenge!
        Test your knowledge of automotive brands and logos.
        Each correct answer earns you 10 points.
        Need help? Use a clue for -5 points.
        See if you can become the ultimate car brand expert!
        """
        
        self.create_label(
            self.frame,
            text=welcome_text,
            wraplength=400
        ).pack(pady=20)

        # Create container for buttons
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=30)

        # Start quiz button
        self.create_button(
            button_frame,
            text="Start Quiz",
            command=self.start_quiz,
            width=200
        ).pack(pady=10)

        # Practice button (if we add practice mode later)
        self.create_button(
            button_frame,
            text="How to Play",
            command=self.show_info,
            width=200
        ).pack(pady=10)

        # High scores button
        self.create_button(
            button_frame,
            text="High Scores",
            command=self.show_high_scores,
            width=200
        ).pack(pady=10)

    def start_quiz(self):
        """Start the quiz by showing the player name input page."""
        self.hide()
        self.game.show_player_input()

    def show_info(self):
        """Show the info page."""
        self.hide()
        self.game.show_info()

    def show_high_scores(self):
        """Show the high scores page."""
        self.hide()
        self.game.show_high_scores()

    def refresh(self):
        """Refresh the home page (if needed)."""
        # This could be used to update any dynamic content
        # Currently just recreates the content
        self.create_frame()
        self.create_content()
