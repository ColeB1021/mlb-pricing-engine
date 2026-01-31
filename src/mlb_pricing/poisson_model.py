import pandas as pd
import numpy as np

def compute_win_probabilities(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given a per-game feature DataFrame, compute:
    - lambda_home, lambda_away (expected runs)
    - p_home_win, p_away_win, p_tie (if used)
    Returns a copy of df with these columns appended.
    """
    out = df.copy()
    # TODO: paste your lambda_home / lambda_away / Poisson win-prob logic here.

    # Clamp probabilities away from 0 and 1 for stability
    eps = 1e-4
    out["p_home_win"] = out["p_home_win"].clip(eps, 1 - eps)
    out["p_away_win"] = 1.0 - out["p_home_win"]
    return out
