import random


def apply_noise(score, strength=0.04):
    """
    Adds controlled randomness to scoring.

    strength:
        0.02 = very stable
        0.04 = realistic draft variance
        0.08 = chaotic drafts
    """

    noise = random.uniform(-strength, strength)
    return score * (1 + noise)