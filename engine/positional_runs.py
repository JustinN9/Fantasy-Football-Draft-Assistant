def detect_positional_runs(draft_state):

    history = draft_state.pick_history
    total_picks = len(history)

    if total_picks < 8:
        return {}

    # Dynamic window sizing for stability
    if total_picks < 30:
        window = 6
    elif total_picks < 80:
        window = 10
    else:
        window = 14

    recent = history[-window:]

    # Count positions safely
    counts = {}

    for item in recent:
        pos = item.position if hasattr(item, "position") else item
        counts[pos] = counts.get(pos, 0) + 1

    total = len(recent)

    run_signals = {}

    for pos, count in counts.items():
        share = count / total

        # Smoothed thresholds
        if share >= 0.45:
            run_signals[pos] = "HOT_RUN"
        elif share >= 0.30:
            run_signals[pos] = "MODERATE_RUN"
        elif share >= 0.18:
            run_signals[pos] = "ACTIVE"

    return run_signals