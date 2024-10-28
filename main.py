"""
Main application module for Car Brand Quiz.
"""
import customtkinter as ctk
from game_logic import GameLogic
from pages.home_page import HomePage
from pages.player_input_page import PlayerInputPage
from pages.game_page import GamePage
from pages.score_page import ScorePage
from pages.info_page import InfoPage
from pages.settings_page import SettingsPage
from database_operations import DatabaseOperations
from config import DEFAULT_WINDOW_SIZE, DEFAULT_WINDOW_POSITION


class CarBrandQuiz:
    def __init__(self):
        """Initialize the application."""
        self.setup_window()
        self.setup_game()
        self.create_pages()
        self.show_home()

    def setup_window(self):
        """Set up the main window."""
        self.root = ctk.CTk()
        self.root.title("Car Brand Quiz")
        self.root.geometry(f"{DEFAULT_WINDOW_SIZE}{DEFAULT_WINDOW_POSITION}")
        ctk.set_appearance_mode("dark")
        self.root.resizable(False, False)

    def setup_game(self):
        """Initialize game components."""
        self.db = DatabaseOperations()
        self.game_logic = GameLogic()
        self.score = 0
        self.player_name = None
        self.current_page = None

    def create_pages(self):
        """Create all application pages."""
        self.pages = {
            'home': HomePage(self.root, self),
            'player_input': PlayerInputPage(self.root, self),
            'game': GamePage(self.root, self),
            'score': ScorePage(self.root, self),
            'info': InfoPage(self.root, self),
            'settings': SettingsPage(self.root, self)
        }
        
        # Hide all pages initially
        for page in self.pages.values():
            page.hide()

    def show_page(self, page_name):
        """Show specified page and hide current one."""
        if self.current_page:
            self.current_page.hide()
            
        page = self.pages[page_name]
        page.reset()
        page.show()
        self.current_page = page

    # Navigation methods
    def show_home(self):
        """Show home page."""
        self.score = 0
        self.show_page('home')

    def show_player_input(self):
        """Show player input page."""
        self.show_page('player_input')

    def show_game(self):
        """Show game page."""
        self.show_page('game')

    def show_high_scores(self):
        """Show high scores page."""
        self.show_page('score')

    def show_info(self):
        """Show info page."""
        self.show_page('info')

    def show_settings(self):
        """Show settings page."""
        self.show_page('settings')

    def start_game(self, player_name):
        """Start game with given player name."""
        self.player_name = player_name
        self.score = 0
        self.show_game()

    def update_score(self, points):
        """Update game score."""
        self.score += points
        self.pages['game'].update_score_display()

    def save_score(self):
        """Save player score to database."""
        if self.player_name and self.score > 0:
            self.db.create_score(self.player_name, self.score)

    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Main function to start the application."""
    app = CarBrandQuiz()
    app.run()


if __name__ == "__main__":
    main()
