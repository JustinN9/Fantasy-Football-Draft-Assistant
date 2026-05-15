from collections import deque

def detect_positional_runs(draft_state, window=10):
    """
    Looks at last N picks and detects if a position is being over-drafted.
    """

    if len(draft_state.pick_history) < window:
        return {}

    recent = draft_state.pick_history[-window:]

    counts = {}
    for pos in recent:
        counts[pos] = counts.get(pos, 0) + 1

    total = len(recent)

    run_signals = {}

    for pos, count in counts.items():
        share = count / total

        # thresholds tuned for fantasy drafts
        if share >= 0.40:
            run_signals[pos] = "HOT_RUN"
        elif share >= 0.25:
            run_signals[pos] = "MODERATE_RUN"

    return run_signals