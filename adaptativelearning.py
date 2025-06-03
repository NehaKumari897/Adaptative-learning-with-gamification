import tkinter as tk
from tkinter import messagebox
import random
import threading
import time

# AI-related Multiple Choice Questions (MCQs)
mcqs = {
    "easy": [
        ("What does 'AI' stand for?", ["Artificial Intelligence", "Automatic Interface", "Advanced Input", "None of the above"], "Artificial Intelligence"),
        ("Which of these is an example of AI?", ["A calculator", "A chatbot", "A bicycle", "A book"], "A chatbot"),
        ("What is a chatbot?", ["A human", "A robot", "A program to simulate conversation", "None of the above"], "A program to simulate conversation")
    ],
    "medium": [
        ("What is the most popular machine learning algorithm?", ["Linear Regression", "Random Forest", "K-means", "Naive Bayes"], "Linear Regression"),
        ("What is a neural network?", ["A network of neurons", "A set of algorithms modeled after the human brain", "A type of decision tree", "None of the above"], "A set of algorithms modeled after the human brain"),
        ("Which of the following is not a supervised learning algorithm?", ["KNN", "Linear Regression", "K-means", "Support Vector Machine"], "K-means")
    ],
    "hard": [
        ("What does NLP stand for in AI?", ["Neural Learning Protocol", "Natural Language Processing", "Nonlinear Programming", "Network Language Processing"], "Natural Language Processing"),
        ("Which algorithm is commonly used for image recognition?", ["Convolutional Neural Network", "Recurrent Neural Network", "Support Vector Machine", "Decision Tree"], "Convolutional Neural Network"),
        ("What is overfitting in machine learning?", ["The model fits the data too well", "The model is too simple", "The model ignores training data", "None of the above"], "The model fits the data too well")
    ],
}

# AI-related words for the puzzle game
word_lists = {
    "easy": ["AI", "bot", "data", "code", "app", "chat","dots","rust","read","role"],
    "medium": ["machine learning", "neural network", "algorithm", "model", "training"],
    "hard": ["reinforcement", "convolutional", "deep learning", "supervised", "unsupervised"],
}

class AdaptiveLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adaptive Learning Game")
        self.score = 0
        self.difficulty = "easy"  # Initial difficulty
        self.current_question = None
        self.correct_answer = None
        self.options = None
        self.question_index = 0  # To keep track of the current question
        self.correct_answers = 0  # Track number of correct answers
        self.attempted_questions = []  # To store questions with answers for review
        self.attempted_puzzles = []  # To store puzzle words and answers for review
        
        # Timer-related attributes
        self.timer_running = False
        self.remaining_time = 60
    

        # Set window size and background color
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        # Create main menu frame
        self.menu_frame = tk.Frame(root, bg="#f0f0f0")
        self.menu_frame.pack(fill="both", expand=True)

        # Title Label
        self.title_label = tk.Label(self.menu_frame, text="Adaptive Learning Game", font=("Helvetica", 30, "bold"), fg="#2c3e50", bg="#f0f0f0")
        self.title_label.pack(pady=40)

        # Play Buttons
        self.quiz_button = tk.Button(self.menu_frame, text="Play Quiz", command=self.start_quiz, font=("Arial", 16), bg="#3498db", fg="white", relief="raised", width=15, height=2)
        self.quiz_button.pack(pady=10)

        self.puzzle_button = tk.Button(self.menu_frame, text="Play Puzzle", command=self.start_puzzle, font=("Arial", 16), bg="#3498db", fg="white", relief="raised", width=15, height=2)
        self.puzzle_button.pack(pady=10)

        # Difficulty Buttons
        self.difficulty_easy_button = tk.Button(self.menu_frame, text="Easy", command=self.set_difficulty_easy, font=("Arial", 16), bg="#2efc71", fg="white", relief="raised", width=15, height=2)
        self.difficulty_easy_button.pack(pady=5)

        self.difficulty_medium_button = tk.Button(self.menu_frame, text="Medium", command=self.set_difficulty_medium, font=("Arial", 16), bg="#f39c12", fg="white", relief="raised", width=15, height=2)
        self.difficulty_medium_button.pack(pady=5)

        self.difficulty_hard_button = tk.Button(self.menu_frame, text="Hard", command=self.set_difficulty_hard, font=("Arial", 16), bg="#e74c3c", fg="white", relief="raised", width=15, height=2)
        self.difficulty_hard_button.pack(pady=5)

        # Score Label
        self.score_label = tk.Label(self.menu_frame, text=f"Score: {self.score}", font=("Arial", 16), fg="#2c3e50", bg="#f0f0f0")
        self.score_label.pack(pady=20)

        # Feedback Label
        self.feedback_label = tk.Label(self.menu_frame, text="", font=("Arial", 14), fg="green", bg="#f0f0f0")
        self.feedback_label.pack()

        # Feedback Button
        self.feedback_button = tk.Button(self.menu_frame, text="Give Feedback", command=self.open_feedback_window, font=("Arial", 16), bg="#16a085", fg="white", relief="raised", width=15, height=2)
        self.feedback_button.pack(pady=10)

        # Game Frames (Quiz, Puzzle)
        self.quiz_frame = tk.Frame(root, bg="#f0f0f0")
        self.puzzle_frame = tk.Frame(root, bg="#f0f0f0")

        # Quiz UI Elements
        self.quiz_question_label = tk.Label(self.quiz_frame, text="Question will appear here", font=("Helvetica", 20), fg="#34495e", bg="#f0f0f0")
        self.quiz_question_label.pack(pady=30)

        # Timer Label for Quiz
        self.quiz_timer_label = tk.Label(self.quiz_frame, text="Time Left: 30", font=("Arial", 16), fg="#e74c3c", bg="#f0f0f0")
        self.quiz_timer_label.pack(pady=10)

        # Quiz Option Buttons
        self.quiz_option_buttons = []
        for i in range(4):
            button = tk.Button(self.quiz_frame, text="", font=("Arial", 16), command=lambda i=i: self.check_quiz_answer(i), relief="raised", width=30, height=3)
            button.pack(pady=15)
            self.quiz_option_buttons.append(button)

        # Quiz Back and Quit Buttons
        self.quiz_back_button = tk.Button(self.quiz_frame, text="Back to Menu", command=self.show_menu, font=("Arial", 14), bg="#e74c3c", fg="white", relief="raised", width=20, height=2)
        self.quiz_back_button.pack(pady=20)

        self.quiz_quit_button = tk.Button(self.quiz_frame, text="End Quiz", command=self.confirm_quit_quiz, font=("Arial", 14), bg="#e74c3c", fg="white", relief="raised", width=20, height=2)
        self.quiz_quit_button.pack(pady=10)

        # Puzzle UI Elements
        self.puzzle_label = tk.Label(self.puzzle_frame, text="Unscramble: ", font=("Helvetica", 20), fg="#34495e", bg="#f0f0f0")
        self.puzzle_label.pack(pady=30)

        # Timer Label for Puzzle
        self.puzzle_timer_label = tk.Label(self.puzzle_frame, text="Time Left: 30", font=("Arial", 16), fg="#e74c3c", bg="#f0f0f0")
        self.puzzle_timer_label.pack(pady=10)

        # Puzzle Answer Entry
        self.puzzle_answer_entry = tk.Entry(self.puzzle_frame, font=("Arial", 16))
        self.puzzle_answer_entry.pack(pady=20)

        # Puzzle Check and Back Buttons
        self.puzzle_check_button = tk.Button(self.puzzle_frame, text="Check Answer", command=self.check_puzzle_answer, font=("Arial", 16), bg="#3498db", fg="white", relief="raised", width=15, height=2)
        self.puzzle_check_button.pack(pady=20)

        self.puzzle_back_button = tk.Button(self.puzzle_frame, text="Back to Menu", command=self.show_menu, font=("Arial", 14), bg="#e74c3c", fg="white", relief="raised", width=20, height=2)
        self.puzzle_back_button.pack(pady=20)

        self.puzzle_quit_button = tk.Button(self.puzzle_frame, text="End Puzzle", command=self.confirm_quit_puzzle, font=("Arial", 14), bg="#e74c3c", fg="white", relief="raised", width=20, height=2)
        self.puzzle_quit_button.pack(pady=10)

        # Reset Game Button
        self.reset_button = tk.Button(self.menu_frame, text="Reset Game", command=self.reset_game, font=("Arial", 16), bg="#2ecc71", fg="white", relief="raised", width=15, height=2)
        self.reset_button.pack(pady=10)

        # Hint-related attributes
        self.puzzle_hint_button = tk.Button(self.puzzle_frame, text="Get Hint", command=self.show_puzzle_hint, font=("Arial", 16), bg="#2ecc71", fg="white", relief="raised", width=15, height=2)
        self.puzzle_hint_button.pack(pady=10)
        
        self.puzzle_hint_label = tk.Label(self.puzzle_frame, text="", font=("Arial", 14), fg="#2980b9", bg="#f0f0f0")
        self.puzzle_hint_label.pack(pady=10)
        
        self.hint_used = False

    def start_timer(self, mode):
        """Start the countdown timer for quiz or puzzle."""
        self.timer_running = True
        self.remaining_time = 60
        
        def countdown():
            timer_mode = mode  # Create a local copy of the mode
            while self.timer_running and self.remaining_time > 0:
                time.sleep(1)
                self.remaining_time -= 1
                
                # Update timer label based on mode
                if timer_mode == 'quiz':
                    self.root.after(0, lambda: self.quiz_timer_label.config(text=f"Time Left: {self.remaining_time}"))
                elif timer_mode == 'puzzle':
                    self.root.after(0, lambda: self.puzzle_timer_label.config(text=f"Time Left: {self.remaining_time}"))
                
                # If time runs out, end the game
                if self.remaining_time <= 0:
                    self.root.after(0, self.time_up)
                    break
        
        # Start countdown in a separate thread
        threading.Thread(target=countdown, daemon=True).start()

    def time_up(self):
        """Handle what happens when time runs out."""
        self.timer_running = False
        
        # Determine which game mode was active
        if self.quiz_frame.winfo_viewable():
            self.show_final_score()
        elif self.puzzle_frame.winfo_viewable():
            self.show_final_puzzle_score()

    def open_feedback_window(self):
        """Create a new window for feedback submission."""
        self.feedback_window = tk.Toplevel(self.root)
        self.feedback_window.title("Submit Feedback")
        self.feedback_window.geometry("400x300")

        # Label for feedback input
        self.feedback_label = tk.Label(self.feedback_window, text="Please provide your feedback:", font=("Arial", 14))
        self.feedback_label.pack(pady=10)

        # Textbox for feedback
        self.feedback_textbox = tk.Text(self.feedback_window, height=6, width=40, font=("Arial", 12))
        self.feedback_textbox.pack(pady=10)

        # Submit button
        self.submit_button = tk.Button(self.feedback_window, text="Submit", command=self.submit_feedback, font=("Arial", 14), bg="#3498db", fg="white", relief="raised")
        self.submit_button.pack(pady=20)

    def submit_feedback(self):
        """Save the feedback to a file."""
        feedback = self.feedback_textbox.get("1.0", "end-1c")
        try:
            with open("feedback.txt", "a") as file:
                file.write(feedback + "\n\n")
            self.feedback_textbox.delete("1.0", "end")
            messagebox.showinfo("Feedback Submitted", "Thank you for your feedback!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save feedback: {e}")

    def reset_game(self):
        """Reset the game state to initial values."""
        self.score = 0
        self.difficulty = "easy"
        self.correct_answers = 0
        self.question_index = 0
        self.attempted_questions = []
        self.attempted_puzzles = []
        self.timer_running = False
        self.remaining_time = 60
        self.score_label.config(text=f"Score: {self.score}")
        self.feedback_label.config(text="")
        self.quiz_timer_label.config(text="Time Left: 60")
        self.puzzle_timer_label.config(text="Time Left: 60")
        self.show_menu()

    def confirm_quit(self, quit_callback):
        """Confirm quitting the game"""
        self.timer_running = False
        answer = messagebox.askyesno("Quit Game", "Are you sure you want to quit?")
        if answer:
            quit_callback()

    def confirm_quit_quiz(self):
        """Confirm quitting the quiz"""
        self.confirm_quit(self.show_final_score)

    def confirm_quit_puzzle(self):
        """Confirm quitting the puzzle"""
        self.confirm_quit(self.show_final_puzzle_score)

    def set_difficulty_easy(self):
        """Set difficulty to easy"""
        self.difficulty = "easy"
        self.feedback_label.config(text="Difficulty set to Easy.", fg="green")

    def set_difficulty_medium(self):
        """Set difficulty to medium"""
        self.difficulty = "medium"
        self.feedback_label.config(text="Difficulty set to Medium.", fg="orange")

    def set_difficulty_hard(self):
        """Set difficulty to hard"""
        self.difficulty = "hard"
        self.feedback_label.config(text="Difficulty set to Hard.", fg="red")

    def show_menu(self):
        """Return to main menu and stop timer"""
        self.timer_running = False
        self.quiz_frame.pack_forget()
        self.puzzle_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)

    def start_quiz(self):
        """Start quiz with timer"""
        self.menu_frame.pack_forget()
        self.quiz_frame.pack(fill="both", expand=True)
        self.quiz_timer_label.config(text="Time Left: 60")  # Reset timer label
        self.show_next_question()
        self.start_timer('quiz')

    def start_puzzle(self):
        """Start puzzle with timer"""
        self.menu_frame.pack_forget()
        self.puzzle_frame.pack(fill="both", expand=True)
        self.puzzle_timer_label.config(text="Time Left: 60")  # Reset timer label
        self.show_next_puzzle()
        self.start_timer('puzzle')

    def show_next_question(self):
        """Show next quiz question"""
        # Dynamically update difficulty if the user didn't manually set it
        if self.difficulty not in mcqs:
            self.difficulty = "easy"

        questions = mcqs[self.difficulty]
        self.current_question, self.options, self.correct_answer = random.choice(questions)

        self.quiz_question_label.config(text=self.current_question)
        for i, option in enumerate(self.options):
            self.quiz_option_buttons[i].config(text=option)

    def check_quiz_answer(self, index):
        """Check the selected quiz answer"""
        selected_answer = self.options[index]
        correct_answer = self.correct_answer

        if selected_answer == correct_answer:
            self.score += 1
            self.correct_answers += 1
            self.attempted_questions.append((self.current_question, selected_answer, correct_answer))
            self.feedback_label.config(text="Correct!", fg="green")
            self.adjust_difficulty(correct=True)
        else:
            self.attempted_questions.append((self.current_question, selected_answer, correct_answer))
            self.feedback_label.config(text="Incorrect!", fg="red")
            self.adjust_difficulty(correct=False)

        self.score_label.config(text=f"Score: {self.score}")
        self.show_next_question()

    def show_final_score(self):
        """Show final quiz score and review"""
        self.timer_running = False
        self.quiz_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)
        review_text = f"Your final score is: {self.score}\nCorrect Answers: {self.correct_answers}\n\nReview:\n"
        
        # Loop through attempted questions for review
        for question, answer, correct_answer in self.attempted_questions:
            review_text += f"Q: {question}\nYour Answer: {answer}\nCorrect Answer: {correct_answer}\n\n"
        
        messagebox.showinfo("Quiz Finished", review_text)
        self.feedback_label.config(text="Quiz finished. Your score has been updated.", fg="blue")

    def show_next_puzzle(self):
        """Show next puzzle word to unscramble"""
        words = word_lists[self.difficulty]
        self.scrambled_word = random.choice(words)
        self.correct_word = self.scrambled_word  # The correct word is the original one

        # Scramble the word here
        scrambled_list = list(self.scrambled_word)
        random.shuffle(scrambled_list)
        self.scrambled_word = ''.join(scrambled_list)

        self.puzzle_label.config(text=f"Unscramble: {self.scrambled_word}")
        self.puzzle_answer_entry.delete(0, tk.END)
        
        # Reset hint for new puzzle
        self.hint_used = False
        self.puzzle_hint_label.config(text="")

    def check_puzzle_answer(self):
        """Check the puzzle answer"""
        user_answer = self.puzzle_answer_entry.get().strip().lower()
        if user_answer == self.correct_word.lower():
            self.score += 1
            self.attempted_puzzles.append((self.scrambled_word, self.correct_word, user_answer))
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            self.attempted_puzzles.append((self.scrambled_word, self.correct_word, user_answer))
            self.feedback_label.config(text="Incorrect!", fg="red")

        self.score_label.config(text=f"Score: {self.score}")
        self.show_next_puzzle()

    def show_final_puzzle_score(self):
        """Show final puzzle score and review"""
        self.timer_running = False
        self.puzzle_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)
        review_text = f"Your final score is: {self.score}\n\nReview:\n"
        
        # Loop through attempted puzzles for review
        for scrambled, correct_word, user_answer in self.attempted_puzzles:
            review_text += f"Scrambled: {scrambled}\nYour Answer: {user_answer}\nCorrect Answer: {correct_word}\n\n"
        
        messagebox.showinfo("Puzzle Finished", review_text)
        self.feedback_label.config(text="Puzzle finished. Your score has been updated.", fg="blue")

    def adjust_difficulty(self, correct):
        """Adjust the difficulty level based on the user's performance."""
        difficulties = ["easy", "medium", "hard"]

        # Get the current difficulty index
        current_index = difficulties.index(self.difficulty)

        # Increase difficulty for a correct answer, decrease for an incorrect one
        if correct and current_index < len(difficulties) - 1:
            self.difficulty = difficulties[current_index + 1]
        elif not correct and current_index > 0:
            self.difficulty = difficulties[current_index - 1]

    def show_puzzle_hint(self):
        """Provide a hint for the current puzzle"""
        if not self.hint_used:
            # Reveal first and last letters, mask middle with asterisks
            if len(self.correct_word) > 2:
                hint = self.correct_word[0] + '*' * (len(self.correct_word) - 2) + self.correct_word[-1]
            else:
                hint = self.correct_word
            
            self.puzzle_hint_label.config(text=f"Hint: {hint}")
            self.hint_used = True
            
            # Deduct points for using a hint
            self.score = max(0, self.score - 1)
            self.score_label.config(text=f"Score: {self.score}")
        else:
            messagebox.showinfo("Hint", "You've already used a hint for this puzzle!")

# Create the main window
root = tk.Tk()

# Create an instance of the AdaptiveLearningApp class
app = AdaptiveLearningApp(root)

# Run the application
root.mainloop()
        