from typing import Callable, MutableMapping


def initialize_state(
    state: MutableMapping,
    low: int,
    high: int,
    difficulty: str,
    randint_fn: Callable[[int, int], int],
) -> None:
    """Initialize session-like state keys only when missing."""
    if "secret" not in state:
        state["secret"] = randint_fn(low, high)

    if "attempts" not in state:
        state["attempts"] = 1

    if "score" not in state:
        state["score"] = 0

    if "status" not in state:
        state["status"] = "playing"

    if "history" not in state:
        state["history"] = []

    if "last_difficulty" not in state:
        state["last_difficulty"] = difficulty


def reset_game_state(
    state: MutableMapping,
    low: int,
    high: int,
    difficulty: str,
    randint_fn: Callable[[int, int], int],
) -> None:
    """Reset state for a fresh game using the current difficulty range."""
    state["attempts"] = 1
    state["secret"] = randint_fn(low, high)
    state["score"] = 0
    state["status"] = "playing"
    state["history"] = []
    state["last_difficulty"] = difficulty


def handle_difficulty_change(
    state: MutableMapping,
    difficulty: str,
    low: int,
    high: int,
    randint_fn: Callable[[int, int], int],
) -> bool:
    """Reset and return True when difficulty changed, otherwise False."""
    if state.get("last_difficulty") == difficulty:
        return False

    reset_game_state(state, low, high, difficulty, randint_fn)
    return True


def attempts_left(attempt_limit: int, attempts: int) -> int:
    """Compute remaining attempts shown in UI."""
    return max(0, attempt_limit - attempts + 1)
