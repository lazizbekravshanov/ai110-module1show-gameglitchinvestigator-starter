from logic_utils import check_guess, parse_guess, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win and appropriate
    # celebratory message should be returned.
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high():
    # Guessing above the secret should give the right outcome and a "lower"
    # hint (the original version had the directions reversed).
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_parse_guess():
    ok, val, err = parse_guess("42")
    assert ok and val == 42 and err is None
    ok, val, err = parse_guess("")
    assert not ok and err == "Enter a guess."
    ok, val, err = parse_guess("not a number")
    assert not ok and err == "That is not a number."


def test_update_score():
    # winning on first attempt yields close to 100 points
    assert update_score(0, "Win", 1) >= 80
    # too high on even attempt gives +5
    assert update_score(10, "Too High", 2) == 15
    # too high on odd attempt subtracts
    assert update_score(10, "Too High", 3) == 5
    # too low always subtracts 5
    assert update_score(10, "Too Low", 1) == 5


def test_check_guess_string_secret():
    # Test the fallback string comparison (simulates the original glitchy
    # behavior where secret was converted to string on alternating attempts).
    # Even with string secret, hints should still be correct.
    outcome, message = check_guess(60, "50")
    assert outcome == "Too High"
    assert "LOWER" in message
    outcome, message = check_guess(40, "50")
    assert outcome == "Too Low"
    assert "HIGHER" in message
