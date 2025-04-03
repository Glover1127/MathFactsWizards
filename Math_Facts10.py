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
    Resets the current level state (score and problem deck) without changing the level.
    """
    st.session_state.score = 0
    st.session_state.problems = generate_problems(st.session_state.current_level)
    st.session_state.feedback = ""

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
        # No need for experimental rerun; session state changes trigger a rerun automatically.

# ------------------------------
# Session state initialization
# ------------------------------
if "current_level" not in st.session_state:
    st.session_state.current_level = None  # Level not yet chosen
    st.session_state.score = 0
    st.session_state.problems = []
    st.session_state.feedback = ""

# ------------------------------
# Level selection screen
# ------------------------------
if st.session_state.current_level is None:
    st.title("Math Facts Game for Second Graders")
    st.write("Practice your addition skills with fun math facts!")
    level_choice = st.selectbox("Select your starting level (1 to 14):", list(range(1, 15)))
    if st.button("Start Game"):
        st.session_state.current_level = level_choice
        st.session_state.score = 0
        st.session_state.problems = generate_problems(level_choice)
    st.stop()  # Stop further execution until a level is selected

# ------------------------------
# Main Game Screen
# ------------------------------
st.header(f"Level {st.session_state.current_level}")
st.write("Answer the math fact below. Earn 1 point for a correct answer and lose 1 point for a wrong answer.")
st.write("Reach 15 points to advance to the next level. But if your score goes to –1, you'll have to restart the level!")
st.write(f"**Score:** {st.session_state.score}")
progress_value = int((st.session_state.score / 15) * 100)
st.progress(progress_value)

# If there are no more problems left, regenerate the deck.
if not st.session_state.problems:
    st.session_state.problems = generate_problems(st.session_state.current_level)

# Get the current problem from the deck
current_problem = st.session_state.problems[0]
a, b = current_problem
st.write(f"**What is {a} + {b}?**")

# ------------------------------
# Answer submission form (Enter key submits and clears the input)
# ------------------------------
with st.form("answer_form", clear_on_submit=True):
    answer = st.text_input("Enter your answer:", key="answer_input")
    submitted = st.form_submit_button("Submit")

if submitted:
    try:
        if int(answer) == a + b:
            st.session_state.score += 1
            st.session_state.feedback = "✅ Correct! Great job!"
        else:
            st.session_state.score -= 1
            st.session_state.feedback = "❌ Not quite. Remember, addition is combining two numbers. Keep trying!"
    except ValueError:
        st.session_state.feedback = "Please enter a valid number."

    # Remove the current problem to avoid repeating it in this level.
    st.session_state.problems.pop(0)

    # Check if the player’s score went below 0
    if st.session_state.score < 0:
        st.error("Oh no! Your score went below 0. Restarting the level. Try again!")
        reset_level()

    # Check if the player reached 15 points to advance to the next level
    if st.session_state.score >= 15:
        advance_level()

# Display feedback after the submission
st.write(st.session_state.feedback)


