"""
Score page module for the Car Brand Quiz application.
Displays high scores and rankings.
"""
import customtkinter as ctk
from pages.base_page import BasePage
from config import TITLE_FONT_SIZE


class ScorePage(BasePage):
    def create_content(self):
        """Create the content for the score page."""
        # Title
        self.create_label(
            self.frame,
            text="Top Scores",
            font_size=TITLE_FONT_SIZE,
            bold=True
        ).pack(pady=(0, 30))

        # Create scoreboard frame
        scoreboard = ctk.CTkFrame(self.frame)
        scoreboard.pack(padx=20, pady=10, fill="both", expand=True)

        # Headers
        header_frame = ctk.CTkFrame(scoreboard, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)

        # Fixed widths for columns
        self.column_widths = {
            "rank": 100,
            "name": 200,
            "score": 100
        }

        # Create headers
        for text, width in [
            ("Rank", self.column_widths["rank"]),
            ("Player", self.column_widths["name"]),
            ("Score", self.column_widths["score"])
        ]:
            self.create_label(
                header_frame,
                text=text,
                font_size=16,
                bold=True,
                width=width
            ).pack(side="left")

        # Get scores from database
        scores = self.game.db.select_score()
        
        if scores:
            # Create scrollable frame for scores
            scores_frame = self.create_scrollable_frame(
                scoreboard,
                height=200,
                width=400
            )
            scores_frame.pack(fill="x", padx=20, pady=5)

            # Sort scores by value in descending order
            sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

            # Display scores
            for rank, (name, score) in enumerate(sorted_scores, 1):
                self.create_score_row(scores_frame, rank, name, score)
        else:
            # Show message if no scores
            self.create_label(
                scoreboard,
                text="No scores yet! Be the first to play!",
                font_size=14,
                text_color=("gray70", "gray30")  # Different colors for light/dark mode
            ).pack(pady=20)

        # Add button container
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=20)

        # Add action buttons
        self.create_button(
            button_frame,
            text="Play Game",
            command=self.start_game,
            width=120
        ).pack(side="left", padx=10)

        self.create_button(
            button_frame,
            text="Back to Home",
            command=self.go_back,
            width=120
        ).pack(side="left", padx=10)

    def create_score_row(self, parent, rank, name, score):
        """
        Create a row in the scoreboard.
        
        Args:
            parent: Parent widget
            rank (int): Player's rank
            name (str): Player's name
            score (int): Player's score
        """
        # Create row frame
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", pady=2)

        # Get rank display text
        if rank <= 3:
            rank_texts = {1: "1st", 2: "2nd", 3: "3rd"}
            rank_text = rank_texts[rank]
        else:
            rank_text = f"{rank}th"

        # Add rank
        self.create_label(
            row_frame,
            text=rank_text,
            width=self.column_widths["rank"],
            font_size=14
        ).pack(side="left")

        # Add name (truncate if too long)
        display_name = name if len(name) <= 20 else name[:17] + "..."
        self.create_label(
            row_frame,
            text=display_name,
            width=self.column_widths["name"],
            font_size=14
        ).pack(side="left")

        # Add score (right-aligned)
        score_label = self.create_label(
            row_frame,
            text=str(score),
            width=self.column_widths["score"],
            font_size=14
        )
        score_label.pack(side="left")

        # Highlight current player's score
        if hasattr(self.game, 'player_name') and self.game.player_name == name:
            row_frame.configure(
                fg_color=("gray85", "gray25")  # Different colors for light/dark mode
            )

    def start_game(self):
        """Start a new game."""
        self.hide()
        self.game.show_player_input()

    def go_back(self):
        """Return to the home page."""
        self.hide()
        self.game.show_home()

    def refresh(self):
        """Refresh the score display."""
        self.create_frame()
        self.create_content()
