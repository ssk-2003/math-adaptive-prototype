"""
Math Adventures - Streamlit Web Interface
AI-Powered Adaptive Learning System
"""

import streamlit as st
import time
from src.puzzle_generator import PuzzleGenerator, Difficulty
from src.tracker import PerformanceTracker
from src.adaptive_engine import AdaptiveEngine

# Page configuration
st.set_page_config(
    page_title="Math Adventures",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #4CAF50;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .puzzle-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 0.5rem 0;
    }
    .difficulty-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.5rem;
    }
    .easy { background: #4CAF50; color: white; }
    .medium { background: #FF9800; color: white; }
    .hard { background: #f44336; color: white; }
    .expert { background: #9C27B0; color: white; }
    .correct { color: #4CAF50; font-size: 1.5rem; }
    .incorrect { color: #f44336; font-size: 1.5rem; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        padding: 0.75rem;
        border: none;
        border-radius: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
        st.session_state.user_name = ""
        st.session_state.puzzle_gen = PuzzleGenerator()
        st.session_state.tracker = None
        st.session_state.adaptive_engine = None
        st.session_state.current_puzzle = None
        st.session_state.puzzle_count = 0
        st.session_state.total_puzzles = 10
        st.session_state.session_active = False
        st.session_state.show_feedback = False
        st.session_state.feedback_message = ""
        st.session_state.start_time = None
        st.session_state.session_complete = False

init_session_state()

def start_session(name, difficulty, num_puzzles):
    """Initialize a new learning session"""
    st.session_state.user_name = name
    st.session_state.tracker = PerformanceTracker(name)
    
    difficulty_map = {
        'Easy': Difficulty.EASY,
        'Medium': Difficulty.MEDIUM,
        'Hard': Difficulty.HARD,
        'Expert': Difficulty.EXPERT
    }
    st.session_state.adaptive_engine = AdaptiveEngine(difficulty_map[difficulty])
    st.session_state.total_puzzles = num_puzzles
    st.session_state.puzzle_count = 0
    st.session_state.session_active = True
    st.session_state.session_complete = False
    st.session_state.initialized = True
    
    generate_new_puzzle()

def generate_new_puzzle():
    """Generate a new puzzle at current difficulty"""
    st.session_state.current_puzzle = st.session_state.puzzle_gen.generate_puzzle(
        st.session_state.adaptive_engine.current_difficulty
    )
    st.session_state.show_feedback = False
    st.session_state.start_time = time.time()

def submit_answer(user_answer):
    """Process user's answer and update system"""
    if st.session_state.current_puzzle is None:
        return
    
    time_taken = time.time() - st.session_state.start_time
    correct = user_answer == st.session_state.current_puzzle['answer']
    
    # Record attempt
    st.session_state.tracker.record_attempt(
        puzzle=st.session_state.current_puzzle,
        user_answer=user_answer,
        correct=correct,
        time_taken=time_taken,
        difficulty_level=st.session_state.adaptive_engine.difficulty_level
    )
    
    # Show feedback
    if correct:
        st.session_state.feedback_message = f"✅ Correct! The answer is {st.session_state.current_puzzle['answer']}"
    else:
        st.session_state.feedback_message = f"❌ Not quite. The correct answer is {st.session_state.current_puzzle['answer']}"
    
    st.session_state.show_feedback = True
    st.session_state.puzzle_count += 1
    
    # Adjust difficulty every 3 puzzles
    if st.session_state.puzzle_count % 3 == 0 and st.session_state.puzzle_count < st.session_state.total_puzzles:
        transition = st.session_state.adaptive_engine.adjust_difficulty(st.session_state.tracker)
        if transition['decision'] != 'MAINTAIN':
            st.session_state.feedback_message += f"\n\n🎚️ **Difficulty {transition['decision']}!** Now at {st.session_state.adaptive_engine.get_difficulty_name()} level."
    
    # Check if session complete
    if st.session_state.puzzle_count >= st.session_state.total_puzzles:
        st.session_state.session_complete = True
        st.session_state.session_active = False

def reset_session():
    """Reset all session state"""
    st.session_state.initialized = False
    st.session_state.session_active = False
    st.session_state.session_complete = False
    st.session_state.puzzle_count = 0
    st.session_state.current_puzzle = None

# Main UI
st.markdown('<div class="main-header">🎮 Math Adventures</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Adaptive Learning System</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Dashboard")
    
    if not st.session_state.initialized:
        st.info("👋 Welcome! Start a new session to begin learning.")
    
    if st.session_state.session_active:
        st.success(f"👤 **{st.session_state.user_name}**")
        st.metric("Puzzle", f"{st.session_state.puzzle_count}/{st.session_state.total_puzzles}")
        st.metric("Difficulty", st.session_state.adaptive_engine.get_difficulty_name())
        st.metric("Current Streak", f"{st.session_state.tracker.current_streak} 🔥")
        
        # Real-time stats
        if st.session_state.tracker.attempts:
            recent = st.session_state.tracker.get_recent_performance(5)
            st.metric("Recent Accuracy", f"{recent['accuracy']*100:.1f}%")
            st.metric("Avg Time", f"{recent['avg_time']:.1f}s")
        
        st.divider()
        if st.button("🏁 End Session", use_container_width=True):
            st.session_state.session_complete = True
            st.session_state.session_active = False
            st.rerun()
    
    st.divider()
    st.caption("Math Adventures v1.0")
    st.caption("Adaptive Learning System")

# Main content area
if not st.session_state.initialized:
    # Welcome screen
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🚀 Start Your Math Adventure!")
        
        with st.form("start_form"):
            name = st.text_input("👤 Your Name", placeholder="Enter your name")
            
            difficulty = st.selectbox(
                "🎯 Starting Difficulty",
                ["Easy", "Medium", "Hard", "Expert"],
                index=1,
                help="Easy: Ages 5-6 | Medium: Ages 7-8 | Hard: Ages 9-10 | Expert: Advanced"
            )
            
            num_puzzles = st.slider("📝 Number of Puzzles", 5, 30, 10)
            
            submitted = st.form_submit_button("Start Learning! 🚀", use_container_width=True)
            
            if submitted:
                if name.strip():
                    start_session(name.strip(), difficulty, num_puzzles)
                    st.rerun()
                else:
                    st.error("Please enter your name!")

elif st.session_state.session_active and not st.session_state.session_complete:
    # Active learning session
    
    # Progress bar
    progress = st.session_state.puzzle_count / st.session_state.total_puzzles
    st.progress(progress)
    
    if st.session_state.show_feedback:
        # Show feedback and next button
        st.markdown(f'<div class="puzzle-box">✨ {st.session_state.feedback_message}</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Next Puzzle ➡️", use_container_width=True, type="primary"):
                generate_new_puzzle()
                st.rerun()
    
    else:
        # Show current puzzle
        puzzle = st.session_state.current_puzzle
        
        st.markdown(f"""
        <div class="puzzle-box">
            {puzzle['question']} = ?
        </div>
        """, unsafe_allow_html=True)
        
        # Answer input
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("answer_form", clear_on_submit=True):
                user_answer = st.number_input(
                    "Your Answer",
                    value=None,
                    step=1,
                    placeholder="Type your answer...",
                    label_visibility="collapsed"
                )
                
                submitted = st.form_submit_button("Submit Answer ✓", use_container_width=True, type="primary")
                
                if submitted and user_answer is not None:
                    submit_answer(int(user_answer))
                    st.rerun()

elif st.session_state.session_complete:
    # Session summary
    st.balloons()
    
    st.markdown("### 🎉 Session Complete!")
    
    summary = st.session_state.tracker.get_session_summary()
    
    # Overall metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Puzzles", summary['total_puzzles'])
    
    with col2:
        st.metric("Accuracy", f"{summary['accuracy']*100:.1f}%")
    
    with col3:
        st.metric("Avg Time", f"{summary['avg_time']:.2f}s")
    
    with col4:
        st.metric("Best Streak", f"{summary['best_streak']} 🔥")
    
    st.divider()
    
    # Detailed breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Performance Breakdown")
        
        st.metric("Correct Answers", f"{summary['correct']} ✅")
        st.metric("Incorrect Answers", f"{summary['incorrect']} ❌")
        st.metric("Current Streak", summary['current_streak'])
        st.metric("Session Duration", f"{summary['session_duration']:.0f}s")
    
    with col2:
        st.markdown("### 🎯 Performance by Difficulty")
        
        diff_names = {1: 'Easy', 2: 'Medium', 3: 'Hard', 4: 'Expert'}
        
        for diff, stats in sorted(summary['difficulty_breakdown'].items()):
            with st.expander(f"{diff_names.get(diff, f'Level {diff}')} Level"):
                st.write(f"**Accuracy:** {stats['accuracy']*100:.1f}%")
                st.write(f"**Puzzles:** {stats['correct']}/{stats['total']}")
                st.write(f"**Avg Time:** {stats['avg_time']:.2f}s")
    
    st.divider()
    
    # Recommendation
    recommendation = st.session_state.adaptive_engine.get_recommendation(st.session_state.tracker)
    st.info(f"💡 **Recommendation:** {recommendation}")
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Start New Session", use_container_width=True, type="primary"):
            reset_session()
            st.rerun()
    
    with col2:
        if st.button("📥 Download Results", use_container_width=True):
            st.success("Feature coming soon!")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Built with ❤️ for better learning experiences | Math Adventures v1.0</p>
    <p><small>Adaptive Learning System • Rule-Based Engine • Zero Dependencies</small></p>
</div>
""", unsafe_allow_html=True)
