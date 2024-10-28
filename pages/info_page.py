"""
Info page module for the Car Brand Quiz application.
Provides game instructions and rules.
"""
import customtkinter as ctk
from pages.base_page import BasePage
from config import TITLE_FONT_SIZE


class InfoPage(BasePage):
    def create_content(self):
        """Create the content for the info page."""
        # Title
        self.create_label(
            self.frame,
            text="How to Play the Car Brand Quiz",
            font_size=TITLE_FONT_SIZE,
            bold=True
        ).pack(pady=(0, 20))

        # Create scrollable frame for rules
        scrollable_frame = self.create_scrollable_frame(
            self.frame,
            height=300,
            width=500
        )
        scrollable_frame.pack(pady=10, padx=20, fill="x", expand=True)

        # Rules sections with headers and content
        self.add_rule_section(
            scrollable_frame,
            "Game Overview",
            [
                "Test your knowledge of car brands and logos",
                "Answer questions about various automotive manufacturers",
                "Use clues wisely to maximize your score",
                "Compete for the top spot on the leaderboard"
            ]
        )

        self.add_rule_section(
            scrollable_frame,
            "Scoring System",
            [
                "Correct answer: +10 points",
                "Using a clue: -5 points",
                "Wrong answer: 0 points",
                "Your highest score will be saved"
            ]
        )

        self.add_rule_section(
            scrollable_frame,
            "How to Answer",
            [
                "Read the question carefully",
                "Type your answer in the input field",
                "Press Enter or click Submit to check your answer",
                "Answers are not case-sensitive"
            ]
        )

        self.add_rule_section(
            scrollable_frame,
            "Using Clues",
            [
                "Each question has one image clue available",
                "Click 'Get Clue' to reveal the image",
                "Clues can only be used once per question",
                "Consider if -5 points is worth seeing the clue"
            ]
        )

        self.add_rule_section(
            scrollable_frame,
            "Tips for Success",
            [
                "Study common car logos and brands",
                "Pay attention to distinctive design features",
                "Learn about major automotive manufacturers",
                "Remember both luxury and everyday car brands"
            ]
        )

        self.add_rule_section(
            scrollable_frame,
            "High Scores",
            [
                "Your best score is saved to the leaderboard",
                "Only your highest score will be kept",
                "View the High Scores page to see top players",
                "Try to reach the number one position!"
            ]
        )

        # Back button container
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=20)

        self.create_button(
            button_frame,
            text="Back to Home",
            command=self.go_back,
            width=200
        ).pack()

    def add_rule_section(self, parent, title, rules):
        """
        Add a section of rules with a title and bullet points.
        
        Args:
            parent: Parent widget
            title (str): Section title
            rules (list): List of rule strings
        """
        # Section title
        self.create_label(
            parent,
            text=title,
            font_size=14,
            bold=True
        ).pack(pady=(15, 5), anchor="w", padx=10)

        # Rules container
        rules_frame = ctk.CTkFrame(parent, fg_color="transparent")
        rules_frame.pack(fill="x", padx=20)

        # Add each rule as a bullet point
        for rule in rules:
            self.create_label(
                rules_frame,
                text=f"• {rule}",
                justify="left",
                anchor="w"
            ).pack(pady=2, anchor="w")

    def go_back(self):
        """Return to the home page."""
        self.hide()
        self.game.show_home()
