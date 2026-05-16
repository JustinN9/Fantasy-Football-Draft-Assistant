SCORING_WEIGHTS = {
    # baseline player quality (VERY important anchor)
    "vbd_weight": 0.65,

    # upside matters more in fantasy than raw projection
    "upside_weight": 6.0,

    # risk should matter, but not dominate
    "risk_weight": 2.5,

    # positional scarcity pressure
    "scarcity_weight": 1.5,

    # ADP influence (keeps draft realistic, not optimal-only)
    "adp_weight": 0.4,

    # replacement-level value (VERY important for tier breaks)
    "opportunity_weight": 0.7
}