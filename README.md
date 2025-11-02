# 🎮 Math Adventures - AI-Powered Adaptive Learning Prototype

An intelligent math learning system that dynamically adjusts puzzle difficulty based on real-time performance analysis. Designed for children ages 5-10.

**🔗 Repository:** https://github.com/ssk-2003/math-adaptive-prototype

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![GitHub](https://img.shields.io/badge/GitHub-ssk--2003%2Fmath--adaptive--prototype-blue?logo=github)](https://github.com/ssk-2003/math-adaptive-prototype)

## 🎯 Overview

Math Adventures uses adaptive learning algorithms to personalize math practice. The system:
- ✅ Generates dynamic math puzzles (addition, subtraction, multiplication, division)
- 📊 Tracks performance metrics (accuracy, response time, streaks)
- 🎚️ Automatically adjusts difficulty based on user performance
- 📈 Provides detailed session analytics and recommendations

## 🏗️ Architecture

```
math-adaptive-prototype/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── app.py                   # Streamlit web interface 
├── run_cli.py               # CLI launcher script
├── src/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # CLI application logic
│   ├── puzzle_generator.py  # Dynamic puzzle generation engine
│   ├── tracker.py           # Performance tracking and analytics
│   └── adaptive_engine.py   # Adaptive difficulty adjustment logic
```

### Component Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
┌──────▼──────────────────────────────────────┐
│           Main Application                  │
│  - Session management                       │
│  - User interface                           │
└──┬─────────┬─────────────┬─────────────────┘
   │         │             │
   ▼         ▼             ▼
┌────────┐ ┌──────────┐ ┌────────────────┐
│Puzzle  │ │Performance│ │ Adaptive       │
│Generator│ │ Tracker   │ │ Engine         │
└────────┘ └──────────┘ └────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ssk-2003/math-adaptive-prototype.git
cd math-adaptive-prototype
```

2. **Install dependencies (for web UI):**
```bash
pip install -r requirements.txt
```
*Note: CLI version requires no dependencies!*

### Running the Application

#### Option 1: Web Interface (Streamlit) - Recommended 
```bash
streamlit run app.py
```
- Beautiful, interactive web interface
- Real-time progress tracking
- Visual feedback and animations
- Runs in your browser

#### Option 2: Command Line Interface (CLI)
```bash
python run_cli.py
```
- No dependencies required
- Terminal-based interface
- Works anywhere with Python

### Usage Example

```bash
$ python run_cli.py

============================================================
🎮  MATH ADVENTURES - AI-Powered Adaptive Learning
============================================================

Enter your name: Alex

Choose your starting difficulty level:
  1. Easy    (Ages 5-6: Small numbers)
  2. Medium  (Ages 7-8: Larger numbers)
  3. Hard    (Ages 9-10: Challenging problems)
  4. Expert  (Advanced: Multi-digit operations)

Enter 1, 2, 3, or 4: 2

How many puzzles would you like to solve? 10

============================================================
Puzzle 1/10 | Level: MEDIUM | Streak: 0 🔥
============================================================

   23 + 34 = ?

Your answer: 57

   ✓ Excellent! 🌟
   👍 Good pace (4.2s)

[System automatically adjusts difficulty based on performance...]
```

## 🧠 Adaptive Learning Logic

### How It Works

The adaptive engine uses a **hybrid rule-based approach** with performance metrics:

#### 1. **Performance Metrics Tracked**
- **Accuracy**: Percentage of correct answers
- **Response Time**: Time taken per puzzle
- **Streak**: Consecutive correct answers
- **Difficulty Performance**: Success rate at each level

#### 2. **Difficulty Adjustment Rules**

**Increase Difficulty When:**
- Accuracy ≥ 80% over last 3 attempts
- Response time < expected time for current level
- OR accuracy ≥ 90% (regardless of time)

**Decrease Difficulty When:**
- Accuracy < 40% over last 2+ attempts
- OR (accuracy < 60% AND response time > 2× expected)

**Maintain Difficulty:**
- Performance is within acceptable range (40-80% accuracy)

#### 3. **Performance Score Calculation**

```
Performance Score = (Accuracy × 0.7) + (Time Score × 0.3)

Where Time Score:
- 1.0: Very fast (< 0.5 × expected_time)
- 0.8: Good time (< expected_time)
- 0.6: Acceptable (< 1.5 × expected_time)
- 0.3: Slow (≥ 1.5 × expected_time)
```

### Difficulty Levels

| Level | Age Range | Number Range | Operations |
|-------|-----------|--------------|------------|
| **Easy** | 5-6 | 1-10 | Addition/Subtraction (1-10), Multiplication (1-5) |
| **Medium** | 7-8 | 10-50 | Addition/Subtraction (10-50), Multiplication (2-12) |
| **Hard** | 9-10 | 50-200 | Addition/Subtraction (50-200), Multiplication (10-25) |
| **Expert** | Advanced | 100-1000 | All operations with larger numbers |

## 📊 Features

### 1. Puzzle Generation
- Four difficulty levels with progressively challenging number ranges
- Four operations: +, −, ×, ÷
- Ensures valid division problems (whole number results)
- Random operation selection or specific operation mode

### 2. Performance Tracking
- Real-time correctness tracking
- Response time measurement
- Streak counting (current and best)
- Per-difficulty performance breakdown
- Session duration and total puzzles solved

### 3. Adaptive Difficulty
- Window-based performance evaluation (last 3 attempts)
- Time-weighted scoring
- Smooth transitions between difficulty levels
- Prevents premature level changes
- Provides clear feedback on transitions

### 4. User Experience
- Clean command-line interface
- Real-time feedback with emojis
- Streak tracking for motivation
- Comprehensive session summary
- Personalized recommendations

## 📈 Session Summary Example

```
============================================================
📊 SESSION SUMMARY FOR ALEX
============================================================

📈 Overall Performance:
   Total Puzzles: 15
   Correct: 12 ✓
   Incorrect: 3 ✗
   Accuracy: 80.0%
   Average Time: 6.43 seconds

🔥 Streaks:
   Best Streak: 5
   Current Streak: 2

⏱️  Session Duration: 127 seconds

📊 Performance by Difficulty:
   Medium: 85.7% accuracy (6/7), avg 5.32s
   Hard: 75.0% accuracy (6/8), avg 7.54s

💡 Recommendation:
   Great progress! Continue practicing at Hard level to build confidence.

📌 Next Session:
   Start at Hard level for optimal challenge.
```

## 🔧 Technical Details

### Design Decisions

#### **Why Rule-Based Instead of ML?**
1. **Transparency**: Parents and educators can understand exactly how decisions are made
2. **No Training Data Required**: Works immediately without collecting data
3. **Predictable Behavior**: No black-box decisions
4. **Lightweight**: Zero dependencies, runs anywhere
5. **Sufficient for Domain**: Math difficulty progression is well-understood

#### **Key Algorithmic Choices**

- **Window Size (3 attempts)**: Balances responsiveness with stability
- **80/40 Threshold Split**: Creates a "comfort zone" (40-80%) where difficulty stays constant
- **Time Weighting (30%)**: Considers speed but prioritizes accuracy
- **Streak Tracking**: Provides motivation without affecting difficulty decisions

### Data Structure

```python
# Attempt Record
{
    'puzzle': {...},           # Full puzzle details
    'user_answer': int,        # User's submitted answer
    'correct_answer': int,     # Correct answer
    'correct': bool,           # Whether answer was correct
    'time_taken': float,       # Time in seconds
    'difficulty': int,         # Difficulty level (1-4)
    'timestamp': datetime      # When attempt was made
}

# Difficulty Transition
{
    'from_level': int,         # Previous difficulty
    'to_level': int,           # New difficulty
    'decision': str,           # INCREASE/DECREASE/MAINTAIN
    'reason': str,             # Human-readable explanation
    'performance_score': float,# Calculated performance (0-1)
    'recent_accuracy': float,  # Last N attempts accuracy
    'recent_avg_time': float   # Last N attempts avg time
}
```

## 🧪 Testing the System

### Manual Testing Scenarios

**1. Test Easy → Hard Progression**
```bash
# Get all answers correct quickly
# Expected: Difficulty increases every 3 puzzles
```

**2. Test Hard → Easy Regression**
```bash
# Get answers wrong or take too long
# Expected: Difficulty decreases
```

**3. Test Stability in Comfort Zone**
```bash
# Maintain 60-70% accuracy
# Expected: Difficulty stays constant
```

## 🔮 Future Enhancements

### Short-term
- [ ] Add color output using `colorama`
- [ ] Export session data to JSON/CSV
- [ ] Add practice mode for specific operations
- [ ] Implement hint system

### Medium-term
- [ ] Web interface using Streamlit
- [ ] User profiles with progress history
- [ ] Visualize performance trends with matplotlib
- [ ] Multi-player mode

### Long-term
- [ ] ML model trained on real user data
- [ ] Spaced repetition algorithm
- [ ] Topic expansion (fractions, decimals, word problems)
- [ ] Gamification elements (badges, levels, achievements)

## 🤔 Discussion Questions

### Data Collection
**Q: How would you collect real data to train or improve your model?**

A: 
1. **Anonymous Telemetry**: Record attempt data (puzzle, answer, time, difficulty transitions)
2. **A/B Testing**: Compare rule-based vs. ML-based adaptations
3. **Teacher Feedback**: Collect educator assessments of difficulty appropriateness
4. **Learning Outcomes**: Track long-term retention through periodic assessments

### Handling Noise
**Q: How would you handle noisy or inconsistent performance?**

A:
1. **Larger Window Size**: Increase from 3 to 5-7 attempts for more stable assessment
2. **Weighted History**: Give more weight to recent attempts, less to older ones
3. **Confidence Intervals**: Only adjust when confident about performance trend
4. **Session Continuity**: Consider performance across sessions, not just current
5. **Outlier Detection**: Ignore attempts that are statistical outliers (too fast/slow)

### Rule-Based vs ML
**Q: What are the trade-offs between rule-based and ML-driven adaptation?**

A:

| Aspect | Rule-Based | ML-Driven |
|--------|-----------|-----------|
| **Transparency** | ✅ Fully explainable | ❌ Black box |
| **Setup** | ✅ Works immediately | ❌ Needs training data |
| **Performance** | ⚠️ Good for known patterns | ✅ Can discover patterns |
| **Adaptability** | ❌ Requires manual tuning | ✅ Self-optimizing |
| **Dependencies** | ✅ None | ❌ ML libraries |
| **Trust** | ✅ Educators trust logic | ⚠️ Requires validation |

### Scaling to Other Topics
**Q: How would you scale this to different topics (beyond math)?**

A:
1. **Abstraction**: Separate domain logic from adaptive logic
2. **Plugin Architecture**: Each subject implements a `PuzzleGenerator` interface
3. **Domain-Specific Metrics**: Different subjects may need different performance indicators
4. **Unified Tracking**: Keep tracker generic, add domain-specific analysis
5. **Cross-Topic Learning**: Track meta-learning skills (problem-solving speed, pattern recognition)

**Example Extensions:**
- **Spelling**: Track accuracy, word difficulty (syllables, common words)
- **Reading Comprehension**: Track passage complexity, question types
- **Science**: Track concept mastery, experiment complexity
- **Geography**: Track location difficulty, region familiarity

## 📄 License

MIT License - feel free to use for educational purposes.

## 🙏 Acknowledgments

Created as part of the Adaptive Learning Assignment - demonstrating AI-powered personalized education.

## 📧 Contact

For questions or feedback about this prototype, please open an issue on [GitHub](https://github.com/ssk-2003/math-adaptive-prototype/issues).

## 🔗 Links

- **Repository:** https://github.com/ssk-2003/math-adaptive-prototype
- **Live Demo:** Run locally with `python -m streamlit run app.py`
- **Author:** [@ssk-2003](https://github.com/ssk-2003)

---

**Built with ❤️ for better learning experiences**
