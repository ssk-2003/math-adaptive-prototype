"""
Adaptive Engine Module
Implements adaptive difficulty adjustment based on user performance.
Uses a hybrid rule-based approach with performance metrics.
"""

from typing import Dict
from .puzzle_generator import Difficulty


class AdaptiveEngine:
    """
    Adaptive engine that adjusts difficulty based on user performance.
    
    Uses a combination of:
    - Recent accuracy (last N attempts)
    - Response time relative to difficulty
    - Consecutive correct/incorrect patterns
    - Performance confidence score
    """
    
    def __init__(self, initial_difficulty: Difficulty = Difficulty.MEDIUM):
        self.current_difficulty = initial_difficulty
        self.difficulty_level = initial_difficulty.value
        self.min_difficulty = 1
        self.max_difficulty = 4
        
        # Adaptive parameters
        self.window_size = 3  # Number of recent attempts to consider
        self.accuracy_threshold_up = 0.80  # 80% accuracy to level up
        self.accuracy_threshold_down = 0.40  # Below 40% to level down
        self.time_weight = 0.3  # Weight for time performance in decision
        
        # Expected time targets for each difficulty (in seconds)
        self.expected_times = {
            1: 10.0,  # Easy
            2: 15.0,  # Medium
            3: 20.0,  # Hard
            4: 30.0   # Expert
        }
        
        self.transition_history = []
    
    def calculate_performance_score(self, recent_performance: Dict, 
                                    current_difficulty: int) -> float:
        """
        Calculate a performance score based on accuracy and time.
        
        Args:
            recent_performance: Dictionary with accuracy and avg_time
            current_difficulty: Current difficulty level
        
        Returns:
            Performance score between 0 and 1
        """
        if recent_performance['total_count'] == 0:
            return 0.5  # Neutral score
        
        accuracy = recent_performance['accuracy']
        avg_time = recent_performance['avg_time']
        expected_time = self.expected_times[current_difficulty]
        
        # Time performance score (faster is better, but too fast might mean too easy)
        if avg_time < expected_time * 0.5:
            time_score = 1.0  # Very fast - might be too easy
        elif avg_time < expected_time:
            time_score = 0.8  # Good time
        elif avg_time < expected_time * 1.5:
            time_score = 0.6  # Acceptable time
        else:
            time_score = 0.3  # Slow - might be too hard
        
        # Combine accuracy and time with weights
        performance_score = (accuracy * (1 - self.time_weight) + 
                           time_score * self.time_weight)
        
        return performance_score
    
    def should_increase_difficulty(self, recent_performance: Dict, 
                                  current_difficulty: int) -> bool:
        """
        Determine if difficulty should be increased.
        
        Criteria:
        - High accuracy (>80%)
        - Fast response time relative to difficulty
        - Minimum attempts in current level
        """
        if recent_performance['total_count'] < self.window_size:
            return False
        
        accuracy = recent_performance['accuracy']
        avg_time = recent_performance['avg_time']
        expected_time = self.expected_times[current_difficulty]
        
        # High accuracy and reasonable time
        if accuracy >= self.accuracy_threshold_up and avg_time < expected_time * 1.2:
            return True
        
        # Very high accuracy, even if time is a bit slow
        if accuracy >= 0.90:
            return True
        
        return False
    
    def should_decrease_difficulty(self, recent_performance: Dict, 
                                  current_difficulty: int) -> bool:
        """
        Determine if difficulty should be decreased.
        
        Criteria:
        - Low accuracy (<40%)
        - Slow response time
        - Pattern of consecutive errors
        """
        if recent_performance['total_count'] < 2:
            return False
        
        accuracy = recent_performance['accuracy']
        avg_time = recent_performance['avg_time']
        expected_time = self.expected_times[current_difficulty]
        
        # Low accuracy
        if accuracy < self.accuracy_threshold_down:
            return True
        
        # Moderate accuracy but very slow
        if accuracy < 0.60 and avg_time > expected_time * 2.0:
            return True
        
        return False
    
    def adjust_difficulty(self, performance_tracker) -> Dict:
        """
        Adjust difficulty based on recent performance.
        
        Args:
            performance_tracker: PerformanceTracker instance
        
        Returns:
            Dictionary with decision details
        """
        recent_perf = performance_tracker.get_recent_performance(self.window_size)
        current_diff = self.difficulty_level
        previous_diff = current_diff
        
        # Calculate performance score
        perf_score = self.calculate_performance_score(recent_perf, current_diff)
        
        # Make decision
        decision = "MAINTAIN"
        reason = "Performance is appropriate for current level"
        
        if self.should_increase_difficulty(recent_perf, current_diff):
            if current_diff < self.max_difficulty:
                self.difficulty_level += 1
                decision = "INCREASE"
                reason = (f"High performance (accuracy: {recent_perf['accuracy']*100:.1f}%, "
                         f"avg time: {recent_perf['avg_time']:.1f}s)")
        
        elif self.should_decrease_difficulty(recent_perf, current_diff):
            if current_diff > self.min_difficulty:
                self.difficulty_level -= 1
                decision = "DECREASE"
                reason = (f"Struggling (accuracy: {recent_perf['accuracy']*100:.1f}%, "
                         f"avg time: {recent_perf['avg_time']:.1f}s)")
        
        # Update current difficulty enum
        difficulty_map = {1: Difficulty.EASY, 2: Difficulty.MEDIUM, 
                         3: Difficulty.HARD, 4: Difficulty.EXPERT}
        self.current_difficulty = difficulty_map[self.difficulty_level]
        
        # Record transition
        transition = {
            'from_level': previous_diff,
            'to_level': self.difficulty_level,
            'decision': decision,
            'reason': reason,
            'performance_score': perf_score,
            'recent_accuracy': recent_perf['accuracy'],
            'recent_avg_time': recent_perf['avg_time']
        }
        self.transition_history.append(transition)
        
        return transition
    
    def get_difficulty_name(self) -> str:
        """Get human-readable name for current difficulty"""
        names = {1: 'Easy', 2: 'Medium', 3: 'Hard', 4: 'Expert'}
        return names.get(self.difficulty_level, 'Unknown')
    
    def print_transition(self, transition: Dict):
        """Print difficulty transition information"""
        if transition['decision'] == "INCREASE":
            emoji = "⬆️ "
            print(f"\n{emoji} DIFFICULTY INCREASED!")
            print(f"   {transition['from_level']} → {transition['to_level']}")
            print(f"   Reason: {transition['reason']}")
        elif transition['decision'] == "DECREASE":
            emoji = "⬇️ "
            print(f"\n{emoji} Difficulty Decreased")
            print(f"   {transition['from_level']} → {transition['to_level']}")
            print(f"   Reason: {transition['reason']}")
        
        if transition['decision'] != "MAINTAIN":
            print(f"   New level: {self.get_difficulty_name()}\n")
    
    def get_recommendation(self, performance_tracker) -> str:
        """Get recommendation for next session"""
        summary = performance_tracker.get_session_summary()
        
        if summary['total_puzzles'] < 5:
            return "Complete more puzzles to get personalized recommendations."
        
        accuracy = summary['accuracy']
        
        if accuracy >= 0.85:
            return (f"Excellent work! You're mastering {self.get_difficulty_name()} level. "
                   f"Keep challenging yourself!")
        elif accuracy >= 0.70:
            return (f"Great progress! Continue practicing at {self.get_difficulty_name()} level "
                   f"to build confidence.")
        elif accuracy >= 0.50:
            return (f"You're learning! Focus on accuracy before speed. "
                   f"Current level: {self.get_difficulty_name()}")
        else:
            return (f"Take your time and review the basics. "
                   f"You're currently at {self.get_difficulty_name()} level.")
