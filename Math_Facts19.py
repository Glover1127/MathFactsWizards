import streamlit as st
import random

# Title and introduction
st.title('✨ Math Facts Game 🎈')
st.write("Welcome to the Math Facts Game! Test your addition skills and advance through all 14 levels to win!")

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = None

# Select level before starting
def reset_level(level):
    st.session_state.score = 0
    st.session_state.level = level
    st.session_state.questions = []
    st.session_state.current_question = None

level_selected = st.selectbox("Select the level you want to start with:", list(range(1, 15)), index=st.session_state.level-1)
if st.button('Start Selected Level'):
    reset_level(level_selected)

# Generate questions based on level
def generate_questions(level):
    questions = []
    if level < 14:
        for x in range(13):
            questions.append((level - 1, x))
    else:
        for a in range(13):
            for b in range(13):
                questions.append((a, b))
    random.shuffle(questions)
    return questions

# Display new question if needed
if st.session_state.current_question is None:
    if not st.session_state.questions:
        st.session_state.questions = generate_questions(st.session_state.level)
    st.session_state.current_question = st.session_state.questions.pop()

question = st.session_state.current_question
st.write(f"## What is {question[0]} + {question[1]}?")

# Answer input
answer = st.text_input("Enter your answer:", key=f"answer_{st.session_state.level}_{st.session_state.score}")
submit = st.button("Submit Answer")

# Progress bar
progress = st.progress(st.session_state.score / 15)
st.write(f"Current score: {st.session_state.score}")

# Check the answer
def check_answer(answer, question):
    correct = question[0] + question[1]
    if int(answer) == correct:
        st.session_state.score += 1
        st.success('Correct! 🎉')
        if st.session_state.score >= 15:
            st.balloons()
            st.success(f"You've advanced to the next level!")
            reset_level(min(st.session_state.level + 1, 14))
    else:
        st.session_state.score -= 1
        hints = [
            "Keep trying, you'll get the next one!",
            "Almost there, think carefully!",
            "Oops, try counting on your fingers!",
            "Stay positive, you can do it!",
            "Nice effort, give it another shot!"
        ]
        st.warning(random.choice(hints))
        if st.session_state.score < 0:
            st.error('Score reached -1. Restarting this level.')
            reset_level(st.session_state.level)

    st.session_state.current_question = None

if submit and answer.strip().isdigit():
    check_answer(answer, question)
    st.rerun()
elif submit:
    st.error("Please enter a valid number.")

# Congratulatory message on final completion
if st.session_state.level == 14 and st.session_state.score >= 15:
    st.success("Congratulations! You've completed all levels! 🎆🎈✨")
    st.balloons()
    st.write("Thank you for playing the Math Facts Game!")
