from app_state_utils import (
    attempts_left,
    handle_difficulty_change,
    initialize_state,
    reset_game_state,
)


def test_initialize_state_sets_missing_keys_once():
    state = {}

    initialize_state(state, 1, 100, "Normal", lambda low, high: 77)

    assert state["secret"] == 77
    assert state["attempts"] == 1
    assert state["score"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []
    assert state["last_difficulty"] == "Normal"


def test_initialize_state_does_not_overwrite_existing_values():
    state = {
        "secret": 42,
        "attempts": 3,
        "score": 15,
        "status": "playing",
        "history": [10, 20],
        "last_difficulty": "Easy",
    }

    initialize_state(state, 1, 100, "Normal", lambda low, high: 99)

    assert state["secret"] == 42
    assert state["attempts"] == 3
    assert state["score"] == 15
    assert state["history"] == [10, 20]
    assert state["last_difficulty"] == "Easy"


def test_handle_difficulty_change_resets_state_and_secret():
    state = {
        "secret": 42,
        "attempts": 4,
        "score": 25,
        "status": "lost",
        "history": [60, 70],
        "last_difficulty": "Normal",
    }

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
    assert state["score"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []
    assert state["last_difficulty"] == "Hard"


def test_handle_difficulty_change_noop_when_unchanged():
    state = {
        "secret": 42,
        "attempts": 2,
        "score": 10,
        "status": "playing",
        "history": [21],
        "last_difficulty": "Normal",
    }

    changed = handle_difficulty_change(
        state,
        difficulty="Normal",
        low=1,
        high=100,
        randint_fn=lambda low, high: 99,
    )

    assert changed is False
    assert state["secret"] == 42
    assert state["attempts"] == 2
    assert state["score"] == 10
    assert state["history"] == [21]


def test_reset_game_state_resets_for_current_difficulty():
    state = {
        "secret": 99,
        "attempts": 5,
        "score": 40,
        "status": "won",
        "history": [10, 20, 30],
        "last_difficulty": "Easy",
    }

    reset_game_state(state, 1, 200, "Hard", lambda low, high: 123)

    assert state["secret"] == 123
    assert state["attempts"] == 1
    assert state["score"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []
    assert state["last_difficulty"] == "Hard"


def test_attempts_left_matches_ui_math_and_clamps_to_zero():
    assert attempts_left(8, 1) == 8
    assert attempts_left(8, 8) == 1
    assert attempts_left(8, 9) == 0
