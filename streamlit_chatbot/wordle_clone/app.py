import streamlit as st
import random

# Load word list
with open("words.txt", "r") as f:
    WORD_LIST = [word.strip().lower() for word in f if len(word.strip()) == 5]

TARGET_WORD = st.session_state.get("target_word", random.choice(WORD_LIST))
if "target_word" not in st.session_state:
    st.session_state.target_word = TARGET_WORD
if "guesses" not in st.session_state:
    st.session_state.guesses = []

MAX_ATTEMPTS = 6

def check_guess(guess, target):
    result = []
    for i in range(5):
        if guess[i] == target[i]:
            result.append("green")
        elif guess[i] in target:
            result.append("yellow")
        else:
            result.append("gray")
    return result

st.title("🟩 Wordle Clone (Streamlit Edition)")

with st.form("wordle_form"):
    guess = st.text_input("Enter your 5-letter guess:").lower()
    submitted = st.form_submit_button("Submit")

    if submitted:
        if len(guess) != 5 or guess not in WORD_LIST:
            st.warning("Invalid guess. Make sure it's a valid 5-letter word.")
        elif len(st.session_state.guesses) >= MAX_ATTEMPTS:
            st.warning("No more attempts left.")
        else:
            st.session_state.guesses.append((guess, check_guess(guess, TARGET_WORD)))

# Display guesses
def check_guess(guess, target):
    result = []
    for i in range(5):
        if guess[i] == target[i]:
            result.append("🟩")
        elif guess[i] in target:
            result.append("🟨")
        else:
            result.append("⬜")
    return result

# Display guesses using emoji squares
for guess, colors in st.session_state.guesses:
    row = ""
    for i in range(5):
        row += f"{colors[i]} **{guess[i].upper()}** "
    st.markdown(row)


# End game conditions
if any(guess == TARGET_WORD for guess, _ in st.session_state.guesses):
    st.success(f"🎉 You guessed it! The word was **{TARGET_WORD.upper()}**.")
    if st.button("Play Again"):
        st.session_state.clear()
elif len(st.session_state.guesses) >= MAX_ATTEMPTS:
    st.error(f"☠️ Game Over. The word was **{TARGET_WORD.upper()}**.")
    if st.button("Try Again"):
        st.session_state.clear()
