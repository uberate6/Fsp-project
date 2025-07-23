import streamlit as st
import random

# Load words
with open("words.txt") as f:
    WORDS = [word.strip().upper() for word in f if len(word.strip()) == 5]

# Choose a random word if not already chosen
if "target_word" not in st.session_state:
    st.session_state.target_word = random.choice(WORDS)
    st.session_state.attempts = []
    st.session_state.game_over = False

st.title("🟩 Wordle with Emojis")
st.caption("Guess the 5-letter word!")

def check_guess(guess, target):
    feedback = []
    target_list = list(target)
    guess_list = list(guess)

    # First pass: correct position
    for i in range(5):
        if guess[i] == target[i]:
            feedback.append("🟩")
            target_list[i] = None
        else:
            feedback.append(None)

    # Second pass: correct letter wrong position
    for i in range(5):
        if feedback[i] is None:
            if guess[i] in target_list:
                feedback[i] = "🟨"
                target_list[target_list.index(guess[i])] = None
            else:
                feedback[i] = "⬜"

    return "".join(feedback)

# Input
if not st.session_state.game_over:
    guess = st.text_input("Enter your guess:", max_chars=5).upper()
    if st.button("Submit Guess"):
        if len(guess) != 5 or guess not in WORDS:
            st.warning("Invalid 5-letter word.")
        else:
            feedback = check_guess(guess, st.session_state.target_word)
            st.session_state.attempts.append((guess, feedback))
            if guess == st.session_state.target_word:
                st.session_state.game_over = True
                st.success("🎉 Correct! You guessed the word!")
            elif len(st.session_state.attempts) >= 6:
                st.session_state.game_over = True
                st.error(f"❌ Out of tries! The word was: {st.session_state.target_word}")

# Display guesses
for guess, feedback in st.session_state.attempts:
    st.write(f"{guess} → {feedback}")

if st.session_state.game_over:
    if st.button("Play Again"):
        st.session_state.clear()