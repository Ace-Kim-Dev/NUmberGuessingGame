import os
import tkinter as tk
import random
import pygame
from tkinter import messagebox

class NumberGuessingGame:
    def __init__(self):
        # Initialize game variables
        self.best_score = None
        self.number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 10  # Default for medium difficulty

        # Initialize Pygame mixer
        pygame.mixer.init()
        self.correct_sound = self.load_sound("ding-126626.mp3")
        self.wrong_sound = self.load_sound("buzzer-or-wrong-answer-20582.mp3")

        # Create the Tkinter window
        self.root = tk.Tk()
        self.root.title("Number Guessing Game")
        self.create_widgets()
        self.root.mainloop()

    def load_sound(self, file_name):
        try:
            sound_file_path = os.path.join(os.path.dirname(__file__), file_name)
            return pygame.mixer.Sound(sound_file_path)
        except pygame.error:
            print(f"Sound file {file_name} not found. Sound disabled.")
            return None

    def create_widgets(self):
        # Header Label
        tk.Label(self.root, text="I'm thinking of a number between 1 and 100.").pack()

        # Entry Field
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.entry.bind("<Return>", self.check_guess)

        # Buttons
        self.submit_button = tk.Button(self.root, text="Submit Guess", command=self.check_guess)
        self.submit_button.pack()

        self.reset_button = tk.Button(self.root, text="Reset Game", command=self.reset_game)
        self.reset_button.pack()

        # Difficulty Dropdown
        self.difficulty_var = tk.StringVar(value="Medium")
        tk.Label(self.root, text="Select Difficulty:").pack()
        difficulty_menu = tk.OptionMenu(self.root, self.difficulty_var, "Easy", "Medium", "Hard", command=self.set_difficulty)
        difficulty_menu.pack()

        # Result Label
        self.result_label = tk.Label(self.root, text="Guess a number between 1 and 100.")
        self.result_label.pack()

        # Best Score Label
        self.best_label = tk.Label(self.root, text="Best Score: None")
        self.best_label.pack()

    def check_guess(self, event=None):
        try:
            guess = int(self.entry.get())
            if not 1 <= guess <= 100:
                self.result_label.config(text="Enter a number between 1 and 100.")
                return

            self.attempts += 1

            if self.attempts > self.max_attempts:
                self.end_game(False)
                return

            if guess < self.number:
                self.result_label.config(text=f"Too low! Attempts left: {self.max_attempts - self.attempts}")
                if self.wrong_sound:
                    self.wrong_sound.play()
            elif guess > self.number:
                self.result_label.config(text=f"Too high! Attempts left: {self.max_attempts - self.attempts}")
                if self.wrong_sound:
                    self.wrong_sound.play()
            else:
                self.result_label.config(text=f"Correct! You guessed it in {self.attempts} attempts.")
                if self.correct_sound:
                    self.correct_sound.play()
                self.update_best_score()
                self.submit_button.config(state="disabled")

        except ValueError:
            self.result_label.config(text="Invalid input. Enter a number.")

    def update_best_score(self):
        if self.best_score is None or self.attempts < self.best_score:
            self.best_score = self.attempts
            self.best_label.config(text=f"Best Score: {self.best_score} attempts")

    def reset_game(self):
        self.number = random.randint(1, 100)
        self.attempts = 0
        self.result_label.config(text="Guess a number between 1 and 100.")
        self.entry.delete(0, tk.END)
        self.submit_button.config(state="normal")

    def set_difficulty(self, difficulty):
        if difficulty == "Easy":
            self.max_attempts = 50
        elif difficulty == "Hard":
            self.max_attempts = 5
        else:
            self.max_attempts = 10
        self.reset_game()
        self.result_label.config(text=f"Difficulty set to {difficulty}. You have {self.max_attempts} attempts.")

    def end_game(self, won):
        if won:
            messagebox.showinfo("Game Over", f"Congratulations! You guessed the number in {self.attempts} attempts.")
        else:
            messagebox.showinfo("Game Over", f"Out of attempts! The number was {self.number}.")
        self.submit_button.config(state="disabled")

# Run the game
if __name__ == "__main__":
    NumberGuessingGame()
