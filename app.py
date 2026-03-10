import random
import streamlit as st

# all game logic has been refactored into helpers so the streamlit file is
# concerned only with UI and state management.  tests exercise the helpers
# directly.
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# initialise the game state once per session (or when the difficulty
# changes).  earlier versions relied on a simple membership check which
# turned out not to be robust when widgets were recreated; dynamic keys were
# also triggering a full state reset.  storing a sentinel prevents the
# secret from being re-randomised on every button click.
# FIX: Prevented secret from resetting on every submit by adding a sentinel
# check for game initialization. Collaborated with Copilot to identify the
# Streamlit rerun issue and implement the guard.
if (
    "game_initialized" not in st.session_state
    or st.session_state.get("difficulty") != difficulty
):
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 1
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.difficulty = difficulty
    st.session_state.game_initialized = True

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# Enhanced UI: Display game history as a table
if st.session_state.history:
    st.subheader("📊 Guess History")
    history_data = []
    for i, guess in enumerate(st.session_state.history, 1):
        closeness = "🔥 Hot" if abs(guess - st.session_state.secret) <= 10 else "❄️ Cold"
        history_data.append({"Attempt": i, "Guess": guess, "Closeness": closeness})
    st.table(history_data)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# a fixed key is sufficient here.  keeping the guess widget's key
# constant avoids odd interactions with streamlit's state machinery.
raw_guess = st.text_input("Enter your guess:", key="guess_input")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # reset everything exactly like the initialisation block above;
    # use the current difficulty range so the secret stays in bounds.
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 1
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.game_initialized = True
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # the original code intentionally flipped the type of the secret on
        # alternating attempts to create a "glitchy" comparison.  the helper
        # function still handles that, so we just pass through whatever is in
        # state.
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            if outcome == "Win":
                st.success(f"🎉 {message}")
            else:
                closeness_emoji = "🔥" if abs(guess_int - st.session_state.secret) <= 10 else "❄️"
                st.info(f"{closeness_emoji} {message}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
