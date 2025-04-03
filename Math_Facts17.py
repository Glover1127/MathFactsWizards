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
        st.experimental_rerun()

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
# Level selection vs. Main Game UI
# ------------------------------
if st.session_state.current_level is None:
    # Level Selection Screen
    st.title("Math Facts Game for Second Graders")
    st.write("Practice your addition skills with fun math facts!")
    level_choice = st.selectbox("Select your starting level (1 to 14):", list(range(1, 15)))
    if st.button("Start Game"):
        st.session_state.current_level = level_choice
        st.session_state.problems = generate_problems(level_choice)
        st.session_state.score = 0
        st.session_state.current_problem = st.session_state.problems[0] if st.session_state.problems else None
        st.experimental_rerun()  # Immediately update the UI after starting the game.
else:
    # Main Game Screen
    st.header(f"Level {st.session_state.current_level}")
    st.write("Answer the math fact below. Earn 1 point for a correct answer and lose 1 point for a wrong answer.")
    st.write("Reach 15 points to advance to the next level. But if your score goes to –1, you'll have to restart the level!")
    st.write(f"**Score:** {st.session_state.score}")
    
    progress_value = int((st.session_state.score / 15) * 100)
    st.progress(progress_value)
    
    # Ensure we have a current problem.
    if not st.session_state.problems:
        st.session_state.problems = generate_problems(st.session_state.current_level)
    if st.session_state.current_problem is None and st.session_state.problems:
        st.session_state.current_problem = st.session_state.problems[0]
    
    # Display the current problem.
    if st.session_state.current_problem:
        a, b = st.session_state.current_problem
        st.write(f"**What is {a} + {b}?**")
    else:
        st.write("No problems available. Please restart the level.")
    
    # Answer submission form.
    with st.form("answer_form", clear_on_submit=True):
        answer = st.text_input("Enter your answer:")
        submitted = st.form_submit_button("Submit")
    
    if submitted and st.session_state.current_problem:
        current_a, current_b = st.session_state.current_problem
        try:
            if int(answer) == current_a + current_b:
                st.session_state.score += 1
                st.session_state.feedback = "✅ Correct! Great job!"
            else:
                st.session_state.score -= 1
                st.session_state.feedback = "❌ Not quite. Remember, addition is combining two numbers. Keep trying!"
        except ValueError:
            st.session_state.feedback = "Please enter a valid number."
        
        # Remove the answered problem from the deck.
        if st.session_state.problems:
            st.session_state.problems.pop(0)
        if st.session_state.problems:
            st.session_state.current_problem = st.session_state.problems[0]
        else:
            st.session_state.current_problem = None
        
        # Check for level restart or advancement.
        if st.session_state.score < 0:
            st.error("Oh no! Your score went below 0. Restarting the level. Try again!")
            reset_level()
        elif st.session_state.score >= 15:
            advance_level()
        
        st.experimental_rerun()  # Force update the UI after processing the answer.
    
    st.write(st.session_state.feedback)
