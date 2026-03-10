def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty.

    The values are hardcoded to match the original behaviour in app.py.  If
    an unknown difficulty string is provided the "Normal" range is returned
    as a sensible default.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    # fallback
    return 1, 100


def parse_guess(raw: str):
    """
    Parse the raw string provided by the user and convert it to an integer.

    Parameters
    ----------
    raw : str
        The string as entered in the text input widget.

    Returns
    -------
    tuple[bool, int | None, str | None]
        A triple where the first element indicates success, the second is the
        integer value (or ``None`` if parsing failed), and the third element is
        an error message to show the user (``None`` on success).
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        # allow floats like "42.0" but cast to int to simplify comparisons
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare a player guess against the secret value.

    Parameters
    ----------
    guess : int | str
        The value supplied by the player (after parsing).  The function is
        intentionally liberal with the type since the original app converts
        the secret to a string on alternating turns as part of the "glitch"
        behaviour.
    secret : int | str
        The secret number (stored in session state).  It may already be a
        string depending on the attempt count.

    Returns
    -------
    tuple[str, str]
        The outcome ("Win", "Too High", or "Too Low") together with the
        human-readable hint message (which must now agree with the outcome).
    """

    # direct equality check handles the common case and also avoids type
    # comparison issues when both are strings.
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # numeric comparison; will raise TypeError if one operand is a string
        # FIX: Corrected hint directions in check_guess; original had swapped
        # "Higher" and "Lower" messages. Collaborated with Copilot to refactor
        # logic into this module and verify correctness with pytest.
        if guess > secret:
            # guess is larger than secret
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        # fall back to string comparison; this replicates the original
        # glitchy behaviour, but the messages still need to match the outcome
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update the player's score based on the result of a guess.

    The scoring rules are translated directly from the original application.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
