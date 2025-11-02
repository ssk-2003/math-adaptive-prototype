"""
Puzzle Generator Module
Generates math puzzles dynamically based on difficulty level.
Supports addition, subtraction, multiplication, and division.
"""

import random
from enum import Enum
from typing import Dict, Tuple


class Difficulty(Enum):
    """Enum for difficulty levels"""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4


class Operation(Enum):
    """Enum for math operations"""
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "×"
    DIVISION = "÷"


class PuzzleGenerator:
    """Generates math puzzles based on difficulty and operation type"""
    
    def __init__(self):
        # Define number ranges for each difficulty level
        self.difficulty_config = {
            Difficulty.EASY: {
                Operation.ADDITION: (1, 10, 1, 10),
                Operation.SUBTRACTION: (1, 10, 1, 10),
                Operation.MULTIPLICATION: (1, 5, 1, 5),
                Operation.DIVISION: (1, 5, 1, 5)
            },
            Difficulty.MEDIUM: {
                Operation.ADDITION: (10, 50, 10, 50),
                Operation.SUBTRACTION: (10, 50, 10, 50),
                Operation.MULTIPLICATION: (2, 12, 2, 12),
                Operation.DIVISION: (2, 12, 2, 12)
            },
            Difficulty.HARD: {
                Operation.ADDITION: (50, 200, 50, 200),
                Operation.SUBTRACTION: (50, 200, 10, 100),
                Operation.MULTIPLICATION: (10, 25, 2, 15),
                Operation.DIVISION: (10, 20, 2, 10)
            },
            Difficulty.EXPERT: {
                Operation.ADDITION: (100, 1000, 100, 1000),
                Operation.SUBTRACTION: (100, 1000, 50, 500),
                Operation.MULTIPLICATION: (15, 50, 10, 25),
                Operation.DIVISION: (20, 100, 5, 20)
            }
        }
    
    def generate_puzzle(self, difficulty: Difficulty, operation: Operation = None) -> Dict:
        """
        Generate a math puzzle based on difficulty and operation.
        
        Args:
            difficulty: Difficulty level
            operation: Specific operation (if None, chooses randomly)
        
        Returns:
            Dictionary with question, answer, operation, and numbers
        """
        if operation is None:
            operation = random.choice(list(Operation))
        
        config = self.difficulty_config[difficulty][operation]
        num1_min, num1_max, num2_min, num2_max = config
        
        if operation == Operation.ADDITION:
            num1 = random.randint(num1_min, num1_max)
            num2 = random.randint(num2_min, num2_max)
            answer = num1 + num2
            question = f"{num1} + {num2}"
            
        elif operation == Operation.SUBTRACTION:
            num1 = random.randint(num1_min, num1_max)
            num2 = random.randint(num2_min, min(num1, num2_max))
            answer = num1 - num2
            question = f"{num1} - {num2}"
            
        elif operation == Operation.MULTIPLICATION:
            num1 = random.randint(num1_min, num1_max)
            num2 = random.randint(num2_min, num2_max)
            answer = num1 * num2
            question = f"{num1} × {num2}"
            
        elif operation == Operation.DIVISION:
            num2 = random.randint(max(1, num2_min), num2_max)
            answer = random.randint(1, num1_max // num2)
            num1 = num2 * answer
            question = f"{num1} ÷ {num2}"
        
        return {
            'question': question,
            'answer': answer,
            'operation': operation.value,
            'difficulty': difficulty.name,
            'num1': num1 if 'num1' in locals() else None,
            'num2': num2 if 'num2' in locals() else None
        }
    
    def get_difficulty_from_string(self, difficulty_str: str) -> Difficulty:
        """Convert string to Difficulty enum"""
        difficulty_map = {
            'easy': Difficulty.EASY,
            'medium': Difficulty.MEDIUM,
            'hard': Difficulty.HARD,
            'expert': Difficulty.EXPERT,
            '1': Difficulty.EASY,
            '2': Difficulty.MEDIUM,
            '3': Difficulty.HARD,
            '4': Difficulty.EXPERT
        }
        return difficulty_map.get(difficulty_str.lower(), Difficulty.MEDIUM)
