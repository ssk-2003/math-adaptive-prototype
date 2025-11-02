"""
Math Adventures - AI-Powered Adaptive Learning Prototype
Main application module that orchestrates the adaptive learning experience.
"""

import sys
import time
from typing import Dict, Optional, Tuple
from puzzle_generator import PuzzleGenerator, Difficulty
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine


class MathAdventures:
    """Main application class for adaptive math learning"""
    
    def __init__(self):
        self.puzzle_gen = PuzzleGenerator()
        self.tracker = None
        self.adaptive_engine = None
        self.user_name = ""
        
    def welcome_screen(self):
        """Display welcome message and get user information"""
        print("\n" + "="*60)
        print("🎮  MATH ADVENTURES - AI-Powered Adaptive Learning")
        print("="*60)
        print("\nWelcome! This app will help you practice math skills")
        print("while automatically adjusting to your learning pace.\n")
        
        # Get user name
        self.user_name = input("Enter your name: ").strip()
        if not self.user_name:
            self.user_name = "Student"
        
        print(f"\nHello, {self.user_name}! Let's start your math adventure! 🚀")
    
    def choose_initial_difficulty(self) -> Difficulty:
        """Let user choose starting difficulty"""
        print("\n" + "-"*60)
        print("Choose your starting difficulty level:")
        print("  1. Easy    (Ages 5-6: Small numbers)")
        print("  2. Medium  (Ages 7-8: Larger numbers)")
        print("  3. Hard    (Ages 9-10: Challenging problems)")
        print("  4. Expert  (Advanced: Multi-digit operations)")
        print("-"*60)
        
        while True:
            choice = input("Enter 1, 2, 3, or 4 (or press Enter for Medium): ").strip()
            
            if not choice:
                choice = "2"
            
            if choice in ['1', '2', '3', '4']:
                difficulty_map = {
                    '1': Difficulty.EASY,
                    '2': Difficulty.MEDIUM,
                    '3': Difficulty.HARD,
                    '4': Difficulty.EXPERT
                }
                return difficulty_map[choice]
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    def get_session_length(self) -> int:
        """Ask user how many puzzles they want to solve"""
        print("\nHow many puzzles would you like to solve?")
        
        while True:
            try:
                count = input("Enter a number (5-50, or press Enter for 10): ").strip()
                if not count:
                    return 10
                
                num = int(count)
                if 5 <= num <= 50:
                    return num
                else:
                    print("Please enter a number between 5 and 50.")
            except ValueError:
                print("Please enter a valid number.")
    
    def present_puzzle(self, puzzle_num: int, total_puzzles: int, puzzle: Dict):
        """Display a puzzle to the user"""
        print("\n" + "="*60)
        print(f"Puzzle {puzzle_num}/{total_puzzles} | "
              f"Level: {puzzle['difficulty']} | "
              f"Streak: {self.tracker.current_streak} 🔥")
        print("="*60)
        print(f"\n   {puzzle['question']} = ?")
        print()
    
    def get_user_answer(self) -> Tuple[Optional[int], float]:
        """
        Get answer from user and measure time.
        Returns (answer, time_taken) or (None, time) if user quits.
        """
        start_time = time.time()
        
        answer_str = input("Your answer (or 'q' to quit): ").strip()
        
        time_taken = time.time() - start_time
        
        if answer_str.lower() == 'q':
            return None, time_taken
        
        try:
            answer = int(answer_str)
            return answer, time_taken
        except ValueError:
            print("Invalid input. Please enter a number.")
            return self.get_user_answer()
    
    def check_answer(self, user_answer: int, correct_answer: int) -> bool:
        """Check if answer is correct and provide feedback"""
        if user_answer == correct_answer:
            responses = ["Correct! 🎉", "Great job! ✨", "Excellent! 🌟", 
                        "Perfect! 💯", "You got it! ✓"]
            import random
            print(f"\n   ✓ {random.choice(responses)}")
            return True
        else:
            print(f"\n   ✗ Not quite. The correct answer is {correct_answer}")
            return False
    
    def run_learning_session(self):
        """Main learning session loop"""
        puzzle_count = self.get_session_length()
        
        print(f"\n🎯 Starting session with {puzzle_count} puzzles!")
        print("   The difficulty will adapt based on your performance.\n")
        input("Press Enter to begin...")
        
        for i in range(1, puzzle_count + 1):
            # Generate puzzle at current difficulty
            puzzle = self.puzzle_gen.generate_puzzle(
                self.adaptive_engine.current_difficulty
            )
            
            # Present puzzle
            self.present_puzzle(i, puzzle_count, puzzle)
            
            # Get user answer
            user_answer, time_taken = self.get_user_answer()
            
            # Check if user wants to quit
            if user_answer is None:
                print("\n👋 Thanks for practicing! Let's see your progress...\n")
                break
            
            # Check answer
            is_correct = self.check_answer(user_answer, puzzle['answer'])
            
            # Record attempt
            self.tracker.record_attempt(
                puzzle=puzzle,
                user_answer=user_answer,
                correct=is_correct,
                time_taken=time_taken,
                difficulty_level=self.adaptive_engine.difficulty_level
            )
            
            # Show time feedback
            if time_taken < 5:
                print(f"   ⚡ Lightning fast! ({time_taken:.1f}s)")
            elif time_taken < 15:
                print(f"   👍 Good pace ({time_taken:.1f}s)")
            
            # Adjust difficulty every 3 puzzles
            if i % 3 == 0 and i < puzzle_count:
                transition = self.adaptive_engine.adjust_difficulty(self.tracker)
                self.adaptive_engine.print_transition(transition)
                
                if transition['decision'] != "MAINTAIN":
                    input("Press Enter to continue...")
    
    def show_final_summary(self):
        """Display comprehensive end-of-session summary"""
        self.tracker.print_summary()
        
        # Show recommendation
        recommendation = self.adaptive_engine.get_recommendation(self.tracker)
        print("💡 Recommendation:")
        print(f"   {recommendation}\n")
        
        # Show next session suggestion
        summary = self.tracker.get_session_summary()
        if summary['total_puzzles'] > 0:
            next_level = self.adaptive_engine.get_difficulty_name()
            print(f"📌 Next Session:")
            print(f"   Start at {next_level} level for optimal challenge.\n")
    
    def run(self):
        """Main application flow"""
        try:
            # Welcome and setup
            self.welcome_screen()
            initial_difficulty = self.choose_initial_difficulty()
            
            # Initialize components
            self.tracker = PerformanceTracker(self.user_name)
            self.adaptive_engine = AdaptiveEngine(initial_difficulty)
            
            # Run learning session
            self.run_learning_session()
            
            # Show summary
            self.show_final_summary()
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Showing your progress...\n")
            if self.tracker and self.tracker.attempts:
                self.show_final_summary()
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please report this issue if it persists.")
        
        print("Thanks for using Math Adventures! Keep learning! 📚✨\n")


def main():
    """Entry point for the application"""
    app = MathAdventures()
    app.run()


if __name__ == "__main__":
    main()
