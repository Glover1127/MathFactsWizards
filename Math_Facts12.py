import streamlit as st
import random

# ------------------------------
# Helper functions
# ------------------------------

def generate_problems(level):
    """
    Generate a list of unique math problems based on the level.
    For levels 1-13, the first addend is fixed to level-1 and the second addend runs from 0 to 12.
    For level 14, generate all combinations (0 through 12 for both addends).
    The list is then randomized.
    """
    if level == 14:
        problems = [(a, b) for a in range(13) for b in range(13)]
    else:
        base = level - 1
        problems = [(base, b) for b in range(13)]
    random.shuffle(problems)
    return problems

def reset_level():
    """
    Resets the current level state (score, problems deck, and current problem) without changing the level.
    """
    st.session_state.score = 0
    st.session_state.problems = generate_problems(st.session_state.current_level)
    st.session_state.feedback = ""
    st.session_state.current_problem = st.session_state.problems[0] if st.session_state.problems else None

def advance_level():
    """
    Advances to the next level. If already at level 14, the game is won.
    """
    if st.session_state.current_level == 14:
        st.balloons()
        st.success("🎉 Congratulations! You have completed all levels and won the game! 🎉")
        st.stop()
    else:
        st.success(
            f"Great work! You've completed Level {st.session_state.current_level}. "
            f"Moving on to Level {st.session_state.current_level + 1}."
        )
        st.session_state.current_level += 1
        reset_level()

# ------------------------------
# Session state initialization
# ------------------------------
if "current_level" not in st.session_state:
    st.session_state.current_level = None  # Level not yet chosen
    st.session_state.score = 0
    st.session_state.problems = []
    st.session_state.feedback = ""
    st.session_state.current_problem = None

# ------------------------------
# Level selection screen
# ------------------------------
if

