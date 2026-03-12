from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def test_check_guess_win_tuple_shape():
    # Regression: old tests assumed check_guess returned only a string.
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_check_guess_too_high_message_direction():
    # Regression: old app had reversed hint text for high/low.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_check_guess_too_low_message_direction():
    # Regression: old app had reversed hint text for high/low.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_parse_guess_rejects_out_of_range_low():
    # Regression: old parser accepted out-of-range values.
    ok, guess, err = parse_guess("0", 1, 100)
    assert ok is False
    assert guess is None
    assert "between 1 and 100" in err


def test_parse_guess_rejects_out_of_range_high():
    ok, guess, err = parse_guess("101", 1, 100)
    assert ok is False
    assert guess is None
    assert "between 1 and 100" in err


def test_parse_guess_accepts_valid_integer():
    ok, guess, err = parse_guess("42", 1, 100)
    assert ok is True
    assert guess == 42
    assert err is None


def test_get_range_for_difficulty_hard_is_larger_than_normal():
    # Regression: old hard range was 1-50, effectively easier than normal.
    easy_low, easy_high = get_range_for_difficulty("Easy")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")

    assert (easy_low, easy_high) == (1, 20)
    assert (normal_low, normal_high) == (1, 100)
    assert (hard_low, hard_high) == (1, 200)
    assert hard_high > normal_high


def test_update_score_too_high_never_rewards_player():
    # Regression: old logic added +5 on even attempts for "Too High".
    assert update_score(0, "Too High", 1) == -5
    assert update_score(0, "Too High", 2) == -5


def test_update_score_too_low_penalty():
    assert update_score(0, "Too Low", 3) == -5


def test_update_score_win_floor_and_formula():
    # Formula uses 100 - 10 * (attempt_number + 1) with floor at 10.
    assert update_score(0, "Win", 1) == 80
    assert update_score(0, "Win", 20) == 10
