from app_state_utils import handle_difficulty_change, initialize_state, reset_game_state
from logic_utils import check_guess, parse_guess, update_score


def apply_submit(state, raw_guess, low, high, attempt_limit):
    """Minimal submit-flow simulation matching app.py behavior."""
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        state["history"].append(raw_guess)
        return {"ok": False, "error": err, "outcome": None}

    state["attempts"] += 1
    state["history"].append(guess_int)

    outcome, message = check_guess(guess_int, state["secret"])
    state["score"] = update_score(state["score"], outcome, state["attempts"])

    if outcome == "Win":
        state["status"] = "won"
    elif state["attempts"] >= attempt_limit:
        state["status"] = "lost"

    return {"ok": True, "error": None, "outcome": outcome, "message": message}


def test_secret_stays_stable_across_multiple_submits():
    state = {}
    initialize_state(state, 1, 100, "Normal", lambda low, high: 50)

    before = state["secret"]
    first = apply_submit(state, "40", 1, 100, 8)
    second = apply_submit(state, "60", 1, 100, 8)

    assert before == 50
    assert state["secret"] == 50
    assert first["outcome"] == "Too Low"
    assert second["outcome"] == "Too High"


def test_invalid_guess_does_not_consume_attempt():
    state = {}
    initialize_state(state, 1, 100, "Normal", lambda low, high: 25)

    attempts_before = state["attempts"]
    result = apply_submit(state, "500", 1, 100, 8)

    assert result["ok"] is False
    assert state["attempts"] == attempts_before
    assert state["history"][-1] == "500"


def test_winning_guess_sets_status_won():
    state = {}
    initialize_state(state, 1, 100, "Normal", lambda low, high: 33)

    result = apply_submit(state, "33", 1, 100, 8)

    assert result["ok"] is True
    assert result["outcome"] == "Win"
    assert state["status"] == "won"


def test_attempt_limit_sets_lost_status_after_nonwinning_guesses():
    state = {}
    initialize_state(state, 1, 20, "Easy", lambda low, high: 20)

    for _ in range(5):
        result = apply_submit(state, "1", 1, 20, 6)

    assert result["outcome"] == "Too Low"
    assert state["status"] == "lost"
    assert state["attempts"] == 6


def test_difficulty_change_resets_state_and_secret_range():
    state = {}
    initialize_state(state, 1, 100, "Normal", lambda low, high: 44)

    apply_submit(state, "50", 1, 100, 8)
    assert state["attempts"] == 2
    assert state["history"] == [50]

    changed = handle_difficulty_change(
        state,
        difficulty="Hard",
        low=1,
        high=200,
        randint_fn=lambda low, high: 150,
    )

    assert changed is True
    assert state["secret"] == 150
    assert state["attempts"] == 1
    assert state["history"] == []
    assert state["status"] == "playing"


def test_new_game_reset_clears_progress_but_keeps_selected_difficulty():
    state = {}
    initialize_state(state, 1, 200, "Hard", lambda low, high: 180)
    apply_submit(state, "100", 1, 200, 5)

    reset_game_state(state, 1, 200, "Hard", lambda low, high: 175)

    assert state["secret"] == 175
    assert state["attempts"] == 1
    assert state["score"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []
    assert state["last_difficulty"] == "Hard"
