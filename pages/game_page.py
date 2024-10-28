"""
Game page module for the Car Brand Quiz application.
"""
import random
import os
from PIL import Image, ImageTk
import customtkinter as ctk
from pages.base_page import BasePage
from config import CLUE_IMAGE_SIZE


class GamePage(BasePage):
    def __init__(self, master, game_instance):
        self.current_question = None
        self.clue_shown = False
        self.questions = {}
        super().__init__(master, game_instance)

    def create_content(self):
        """Create the game page content."""
        # Main container with fixed height
        main_container = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True)

        # Score display - centered at top
        ctk.CTkLabel(
            main_container,
            text=f"Score: {self.game.score}",
            font=("Arial", 16),
            anchor="center"
        ).pack(pady=(0, 10))

        # Load questions if needed
        if not self.questions:
            self.questions = {
                q[1]: (q[2], q[3]) for q in self.game.db.select_question()
            }

        if self.questions:
            # Get random question
            question = random.choice(list(self.questions.keys()))
            
            # Question display - centered
            question_label = ctk.CTkLabel(
                main_container,
                text=question,
                wraplength=400,
                justify="center"
            )
            question_label.pack(pady=10)

            # Create frame for clue image with fixed size
            self.clue_frame = ctk.CTkFrame(
                main_container, 
                fg_color="transparent",
                height=300  # Fixed height for clue area
            )
            self.clue_frame.pack(fill="x", pady=10)
            self.clue_frame.pack_propagate(False)  # Prevent frame from shrinking
            
            # Create image label in advance (hidden initially)
            self.clue_label = ctk.CTkLabel(self.clue_frame, text="")
            self.clue_label.pack(expand=True)

            # Answer entry - centered
            self.answer_entry = ctk.CTkEntry(
                main_container,
                width=400,
                height=30,
                placeholder_text="Type your answer here..."
            )
            self.answer_entry.pack(pady=10)
            
            # Button container at bottom
            button_frame = ctk.CTkFrame(main_container, fg_color="transparent")
            button_frame.pack(side="bottom", pady=20)

            # Buttons with fixed width
            self.clue_button = ctk.CTkButton(
                button_frame,
                text="Clue",
                command=lambda: self.show_clue(question),
                width=100,
                height=30
            )
            self.clue_button.pack(side="left", padx=10)

            submit_button = ctk.CTkButton(
                button_frame,
                text="Submit",
                command=lambda: self.check_answer(question),
                width=100,
                height=30
            )
            submit_button.pack(side="left", padx=10)

            # Set focus to answer entry
            self.answer_entry.focus()
            
            # Bind Enter key to submit
            self.answer_entry.bind("<Return>", lambda e: self.check_answer(question))

    def show_clue(self, question):
        """Display clue image."""
        try:
            # Update score first
            self.game.score -= 5
            self.update_score_display()

            # Load and display image
            image_path = os.path.join("assets", "images", "clues", self.questions[question][0])
            original_image = Image.open(image_path)
            
            # Calculate aspect ratio
            aspect_ratio = original_image.width / original_image.height
            target_height = 300
            target_width = int(target_height * aspect_ratio)
            
            # Resize maintaining aspect ratio
            resized_image = original_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Create CTkImage instead of PhotoImage
            ctk_image = ctk.CTkImage(
                light_image=resized_image,
                dark_image=resized_image,
                size=(target_width, target_height)
            )
            
            # Update existing label
            self.clue_label.configure(image=ctk_image)
            self.clue_label.image = ctk_image  # Keep reference
            
            # Disable clue button
            self.clue_button.configure(state="disabled")

        except Exception as e:
            print(f"Error showing clue: {e}")

    def check_answer(self, question):
        """Process the answer and move to next question."""
        answer = self.answer_entry.get().strip().lower()
        correct_answer = str(self.questions[question][1]).strip().lower()

        if answer == correct_answer:
            self.game.score += 10

        self.questions.pop(question)
        
        if self.questions:
            self.reset()  # Show next question
        else:
            self.show_game_over()

    def show_game_over(self):
        """Display game over screen."""
        self.clear_frame()

        # Game Over title
        ctk.CTkLabel(
            self.frame,
            text="Game Over!",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # Score message
        if self.game.score > 0:
            message = f"Congratulations {self.game.player_name}!"
        else:
            message = f"Keep practicing {self.game.player_name}! Better luck next time!"

        ctk.CTkLabel(
            self.frame,
            text=message,
            font=("Arial", 16)
        ).pack(pady=5)

        ctk.CTkLabel(
            self.frame,
            text=f"Final Score: {self.game.score} points",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        # Save score
        self.game.db.create_score(self.game.player_name, self.game.score)

        # Buttons
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Play Again",
            command=self.game.show_home,
            width=120,
            height=30
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="View High Scores",
            command=self.game.show_high_scores,
            width=120,
            height=30
        ).pack(side="left", padx=10)

    def update_score_display(self):
        """Update the score display."""
        for widget in self.frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and "Score:" in widget._text:
                widget.configure(text=f"Score: {self.game.score}")
                break

    def clear_frame(self):
        """Clear all widgets from the frame."""
        for widget in self.frame.winfo_children():
            widget.destroy()
