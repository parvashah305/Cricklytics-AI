def compute_pressure_index(
    required_run_rate: float, current_run_rate: float, dot_ball_percentage: float, wickets_fallen: int
) -> float:
    """
    Compute pressure index using weighted factors from project spec.
    pressure = ((rrr/crr)*0.4 + (dot_pct/100)*0.3 + (wickets/10)*0.3) * 100
    """
    safe_crr = current_run_rate if current_run_rate > 0 else 0.1
    pressure = (
        (required_run_rate / safe_crr) * 0.4
        + (dot_ball_percentage / 100.0) * 0.3
        + (wickets_fallen / 10.0) * 0.3
    ) * 100.0
    return round(max(0.0, min(100.0, pressure)), 2)
