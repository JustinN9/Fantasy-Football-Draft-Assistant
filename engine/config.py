SCORING_PROFILES = {
    "default": {
        # Baseline player quality
        "vbd_weight": 0.65,

        # Upside matters more in fantasy than raw projection
        "upside_weight": 6.0,

        # Risk should matter, but not dominate
        "risk_weight": 2.5,

        # Positional scarcity pressure
        "scarcity_weight": 1.5,

        # ADP influence (keeps draft realistic, not only optimal)
        "adp_weight": 0.4,

        # Replacement-level value (important for tier breaks)
        "opportunity_weight": 0.7
    }
}