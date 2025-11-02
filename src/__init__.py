"""
Math Adventures - AI-Powered Adaptive Learning Prototype
A minimal adaptive math learning system for children ages 5-10.
"""

__version__ = "1.0.0"
__author__ = "Adaptive Learning Team"

from .puzzle_generator import PuzzleGenerator, Difficulty, Operation
from .tracker import PerformanceTracker
from .adaptive_engine import AdaptiveEngine

__all__ = [
    'PuzzleGenerator',
    'Difficulty',
    'Operation',
    'PerformanceTracker',
    'AdaptiveEngine'
]
