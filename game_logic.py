"""
Game logic module handling core game mechanics and state management.
"""
from typing import Dict, Tuple, Optional


class GameLogic:
    """Handles core game mechanics and scoring logic."""

    def __init__(self):
        """Initialize game state."""
        self.reset_game()

    def reset_game(self):
        """Reset all game state variables."""
        self.score = 0
        self.questions_answered = 0
        self.clues_used = 0
        self.current_streak = 0
        self.best_streak = 0

    def calculate_score(self, is_correct: bool, used_clue: bool) -> int:
        """
        Calculate score for an answer.
        
        Args:
            is_correct (bool): Whether the answer was correct
            used_clue (bool): Whether a clue was used
            
        Returns:
            int: Points earned/lost for this question
        """
        points = 0
        
        if is_correct:
            points = 10
            self.current_streak += 1
            self.best_streak = max(self.best_streak, self.current_streak)
        else:
            self.current_streak = 0
        
        if used_clue:
            points -= 5
        
        self.score += points
        self.questions_answered += 1
        if used_clue:
            self.clues_used += 1
            
        return points

    def check_answer(self, user_answer: str, correct_answer: str) -> bool:
        """
        Check if the user's answer is correct.
        
        Args:
            user_answer (str): The user's answer
            correct_answer (str): The correct answer
            
        Returns:
            bool: True if answer is correct, False otherwise
        """
        return user_answer.strip().lower() == correct_answer.strip().lower()

    def get_statistics(self) -> Dict[str, int]:
        """
        Get current game statistics.
        
        Returns:
            Dict[str, int]: Dictionary containing game statistics
        """
        return {
            'score': self.score,
            'questions_answered': self.questions_answered,
            'clues_used': self.clues_used,
            'current_streak': self.current_streak,
            'best_streak': self.best_streak
        }

    def calculate_accuracy(self) -> Optional[float]:
        """
        Calculate the player's accuracy percentage.
        
        Returns:
            Optional[float]: Accuracy percentage or None if no questions answered
        """
        if self.questions_answered == 0:
            return None
        return (self.score / (self.questions_answered * 10)) * 100

    def should_show_achievement(self) -> Optional[str]:
        """
        Check if any achievements have been unlocked.
        
        Returns:
            Optional[str]: Achievement message if unlocked, None otherwise
        """
        achievements = []
        
        if self.current_streak >= 5:
            achievements.append("Hot Streak: 5 correct answers in a row!")
        if self.score >= 100:
            achievements.append("Century: Reached 100 points!")
        if self.questions_answered >= 10 and self.clues_used == 0:
            achievements.append("No Help Needed: Answered 10 questions without clues!")
            
        return achievements[0] if achievements else None
