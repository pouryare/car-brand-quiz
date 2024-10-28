"""
Base page module providing common functionality for all pages in the Car Brand Quiz application.
"""
import customtkinter as ctk
from config import FONT_FAMILY, NORMAL_FONT_SIZE


class BasePage:
    """Base class for all pages in the application."""
    
    def __init__(self, master, game_instance):
        """
        Initialize the base page.
        
        Args:
            master: The parent widget (usually the main frame)
            game_instance: Instance of the main game class for accessing shared resources
        """
        self.master = master
        self.game = game_instance
        self.frame = None
        self.setup()

    def setup(self):
        """Set up the page frame and content."""
        self.create_frame()
        self.create_content()

    def create_frame(self):
        """Create the main frame for the page."""
        # Destroy existing frame if it exists
        if self.frame is not None:
            self.frame.destroy()

        # Create new frame
        self.frame = ctk.CTkFrame(self.master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

    def create_content(self):
        """
        Create the content for the page.
        To be overridden by child classes.
        """
        raise NotImplementedError("Subclasses must implement create_content()")

    def show(self):
        """Display the page."""
        if self.frame:
            self.frame.pack(pady=20, padx=20, fill="both", expand=True)

    def hide(self):
        """Hide the page."""
        if self.frame:
            self.frame.pack_forget()

    def destroy(self):
        """Destroy the page frame."""
        if self.frame:
            self.frame.destroy()
            self.frame = None

    def reset(self):
        """
        Reset the page to its initial state.
        Can be overridden by child classes for specific reset behavior.
        Default implementation recreates the frame and content.
        """
        self.create_frame()
        self.create_content()

    def create_label(self, parent, text, font_size=None, bold=False, **kwargs):
        """
        Create a standardized label.
        
        Args:
            parent: Parent widget
            text (str): Label text
            font_size (int, optional): Font size
            bold (bool): Whether to make text bold
            **kwargs: Additional arguments for CTkLabel
        
        Returns:
            CTkLabel: The created label
        """
        font_size = font_size or NORMAL_FONT_SIZE
        weight = "bold" if bold else "normal"
        label = ctk.CTkLabel(
            parent,
            text=text,
            font=(FONT_FAMILY, font_size, weight),
            **kwargs
        )
        return label

    def create_button(self, parent, text, command, **kwargs):
        """
        Create a standardized button.
        
        Args:
            parent: Parent widget
            text (str): Button text
            command: Button command
            **kwargs: Additional arguments for CTkButton
        
        Returns:
            CTkButton: The created button
        """
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=(FONT_FAMILY, NORMAL_FONT_SIZE),
            **kwargs
        )
        return button

    def create_entry(self, parent, placeholder_text="", **kwargs):
        """
        Create a standardized entry field.
        
        Args:
            parent: Parent widget
            placeholder_text (str): Placeholder text for the entry
            **kwargs: Additional arguments for CTkEntry
        
        Returns:
            CTkEntry: The created entry field
        """
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder_text,
            font=(FONT_FAMILY, NORMAL_FONT_SIZE),
            **kwargs
        )
        return entry

    def create_scrollable_frame(self, parent, **kwargs):
        """
        Create a standardized scrollable frame.
        
        Args:
            parent: Parent widget
            **kwargs: Additional arguments for CTkScrollableFrame
        
        Returns:
            CTkScrollableFrame: The created scrollable frame
        """
        frame = ctk.CTkScrollableFrame(
            parent,
            **kwargs
        )
        return frame

    def show_message(self, text, text_color=None, font_size=None):
        """
        Display a message on the page.
        
        Args:
            text (str): Message text
            text_color (str, optional): Color of the text
            font_size (int, optional): Font size for the message
        """
        self.create_label(
            self.frame,
            text=text,
            text_color=text_color,
            font_size=font_size
        ).pack(pady=10)
