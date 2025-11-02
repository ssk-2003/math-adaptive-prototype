"""
Performance Tracker Module
Tracks user performance metrics including correctness, time taken, and streak.
"""

import time
from typing import List, Dict
from datetime import datetime


class PerformanceTracker:
    """Tracks and analyzes user performance across puzzles"""
    
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.session_start = datetime.now()
        self.attempts: List[Dict] = []
        self.current_streak = 0
        self.best_streak = 0
        
    def start_puzzle(self) -> float:
        """Mark the start time for a puzzle"""
        return time.time()
    
    def record_attempt(self, puzzle: Dict, user_answer: int, correct: bool, 
                      time_taken: float, difficulty_level: int):
        """
        Record a puzzle attempt with all relevant metrics.
        
        Args:
            puzzle: The puzzle dictionary
            user_answer: User's submitted answer
            correct: Whether the answer was correct
            time_taken: Time taken to solve (in seconds)
            difficulty_level: Current difficulty level (1-4)
        """
        attempt = {
            'puzzle': puzzle,
            'user_answer': user_answer,
            'correct_answer': puzzle['answer'],
            'correct': correct,
            'time_taken': time_taken,
            'difficulty': difficulty_level,
            'timestamp': datetime.now()
        }
        
        self.attempts.append(attempt)
        
        # Update streak
        if correct:
            self.current_streak += 1
            self.best_streak = max(self.best_streak, self.current_streak)
        else:
            self.current_streak = 0
    
    def get_recent_performance(self, n: int = 5) -> Dict:
        """
        Analyze performance over the last n attempts.
        
        Args:
            n: Number of recent attempts to analyze
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.attempts:
            return {
                'accuracy': 0.0,
                'avg_time': 0.0,
                'correct_count': 0,
                'total_count': 0
            }
        
        recent = self.attempts[-n:]
        correct_count = sum(1 for a in recent if a['correct'])
        total_count = len(recent)
        avg_time = sum(a['time_taken'] for a in recent) / total_count
        
        return {
            'accuracy': correct_count / total_count,
            'avg_time': avg_time,
            'correct_count': correct_count,
            'total_count': total_count
        }
    
    def get_difficulty_performance(self) -> Dict[int, Dict]:
        """Analyze performance broken down by difficulty level"""
        difficulty_stats = {}
        
        for attempt in self.attempts:
            diff = attempt['difficulty']
            if diff not in difficulty_stats:
                difficulty_stats[diff] = {'correct': 0, 'total': 0, 'times': []}
            
            difficulty_stats[diff]['total'] += 1
            if attempt['correct']:
                difficulty_stats[diff]['correct'] += 1
            difficulty_stats[diff]['times'].append(attempt['time_taken'])
        
        # Calculate averages
        for diff, stats in difficulty_stats.items():
            stats['accuracy'] = stats['correct'] / stats['total']
            stats['avg_time'] = sum(stats['times']) / len(stats['times'])
        
        return difficulty_stats
    
    def get_session_summary(self) -> Dict:
        """Generate comprehensive session summary"""
        if not self.attempts:
            return {
                'user_name': self.user_name,
                'total_puzzles': 0,
                'accuracy': 0.0,
                'avg_time': 0.0,
                'best_streak': 0,
                'session_duration': 0
            }
        
        total_puzzles = len(self.attempts)
        correct_count = sum(1 for a in self.attempts if a['correct'])
        accuracy = correct_count / total_puzzles
        avg_time = sum(a['time_taken'] for a in self.attempts) / total_puzzles
        session_duration = (datetime.now() - self.session_start).total_seconds()
        
        return {
            'user_name': self.user_name,
            'total_puzzles': total_puzzles,
            'correct': correct_count,
            'incorrect': total_puzzles - correct_count,
            'accuracy': accuracy,
            'avg_time': avg_time,
            'best_streak': self.best_streak,
            'current_streak': self.current_streak,
            'session_duration': session_duration,
            'difficulty_breakdown': self.get_difficulty_performance(),
            'session_start': self.session_start,
            'session_end': datetime.now()
        }
    
    def print_summary(self):
        """Print formatted session summary"""
        summary = self.get_session_summary()
        
        print("\n" + "="*60)
        print(f"📊 SESSION SUMMARY FOR {summary['user_name'].upper()}")
        print("="*60)
        
        if summary['total_puzzles'] == 0:
            print("No puzzles completed in this session.")
            return
        
        print(f"\n📈 Overall Performance:")
        print(f"   Total Puzzles: {summary['total_puzzles']}")
        print(f"   Correct: {summary['correct']} ✓")
        print(f"   Incorrect: {summary['incorrect']} ✗")
        print(f"   Accuracy: {summary['accuracy']*100:.1f}%")
        print(f"   Average Time: {summary['avg_time']:.2f} seconds")
        
        print(f"\n🔥 Streaks:")
        print(f"   Best Streak: {summary['best_streak']}")
        print(f"   Current Streak: {summary['current_streak']}")
        
        print(f"\n⏱️  Session Duration: {summary['session_duration']:.0f} seconds")
        
        print(f"\n📊 Performance by Difficulty:")
        diff_names = {1: 'Easy', 2: 'Medium', 3: 'Hard', 4: 'Expert'}
        for diff, stats in sorted(summary['difficulty_breakdown'].items()):
            print(f"   {diff_names.get(diff, f'Level {diff}')}: "
                  f"{stats['accuracy']*100:.1f}% accuracy "
                  f"({stats['correct']}/{stats['total']}), "
                  f"avg {stats['avg_time']:.2f}s")
        
        print("\n" + "="*60 + "\n")
