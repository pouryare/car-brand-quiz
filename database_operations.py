"""
Database operations for the Car Brand Quiz application.
"""
import sqlite3
from config import DB_PATH


class DatabaseOperations:
    def __init__(self):
        """Initialize database connection and create tables if needed."""
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create necessary database tables if they don't exist."""
        try:
            # Create questions table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS question (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    question TEXT NOT NULL,
                    image_filename TEXT UNIQUE NOT NULL,
                    answer TEXT NOT NULL,
                    path TEXT
                )
            ''')

            # Create score table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS score_table (
                    name TEXT UNIQUE,
                    score INTEGER NOT NULL
                )
            ''')

            self.conn.commit()
        except Exception as e:
            print(f"Error creating tables: {e}")
            self.conn.rollback()

    def insert_question(self, question, image_filename, answer):
        """
        Insert a new question into the database.
        
        Args:
            question (str): The question text
            image_filename (str): Name of the clue image file
            answer (set): Set containing the correct answer(s)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cursor.execute(
                'INSERT INTO question (question, image_filename, answer) VALUES (?, ?, ?)',
                (question, image_filename, str(answer))
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting question: {e}")
            self.conn.rollback()
            return False

    def select_question(self):
        """
        Retrieve all questions from the database.
        
        Returns:
            list: List of tuples containing question data
        """
        try:
            self.cursor.execute('SELECT * FROM question')
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error selecting questions: {e}")
            return []

    def select_score(self):
        """
        Retrieve all scores from the database.
        
        Returns:
            list: List of tuples containing score data
        """
        try:
            self.cursor.execute('SELECT * FROM score_table ORDER BY score DESC')
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error selecting scores: {e}")
            return []

    def create_score(self, player, score):
        """
        Create or update a player's score.
        
        Args:
            player (str): Player's name
            score (int): Player's score
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Try to insert new score
            try:
                self.cursor.execute(
                    'INSERT INTO score_table (name, score) VALUES (?, ?)',
                    (player, score)
                )
            except sqlite3.IntegrityError:
                # Player exists, update only if new score is higher
                self.cursor.execute(
                    'SELECT score FROM score_table WHERE name = ?',
                    (player,)
                )
                current_score = self.cursor.fetchone()
                
                if current_score and current_score[0] < score:
                    self.cursor.execute(
                        'UPDATE score_table SET score = ? WHERE name = ?',
                        (score, player)
                    )

            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error creating/updating score: {e}")
            self.conn.rollback()
            return False

    def get_top_scores(self, limit=10):
        """
        Get top scores from the database.
        
        Args:
            limit (int): Number of top scores to retrieve
            
        Returns:
            list: List of tuples containing top scores
        """
        try:
            self.cursor.execute(
                'SELECT name, score FROM score_table ORDER BY score DESC LIMIT ?',
                (limit,)
            )
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving top scores: {e}")
            return []

    def add_sample_questions(self):
        """Add sample questions to the database if it's empty."""
        if not self.select_question():
            sample_questions = [
                (
                    "An England company founded in 1910's that made luxurious cars and later owned by BMW in 2003",
                    "Rolls Royce.jpg",
                    "{'Rolls Royce'}"
                ),
                (
                    "Which German car manufacturer is known for the 911 model?",
                    "Porsche.jpg",
                    "{'Porsche'}"
                ),
                (
                    "This Italian car manufacturer is known for its prancing horse logo",
                    "Ferrari.jpg",
                    "{'Ferrari'}"
                )
            ]
            
            for q, img, ans in sample_questions:
                self.insert_question(q, img, eval(ans))

    def __del__(self):
        """Cleanup database connection."""
        try:
            self.conn.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")


# Initialize database with sample questions if needed
if __name__ == "__main__":
    db = DatabaseOperations()
    db.add_sample_questions()
