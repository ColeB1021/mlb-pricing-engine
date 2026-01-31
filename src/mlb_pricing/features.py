import pandas as pd

def build_team_features(
    games: pd.DataFrame,
    batting: pd.DataFrame,
    pitching: pd.DataFrame,
    fielding: pd.DataFrame,
) -> pd.DataFrame:
    """
    Join game-level data with Fangraphs stats and any rolling / park features.
    Returns a per-game frame suitable as input to the Poisson model.
    """
    # TODO: paste your current feature-join logic here.
    raise NotImplementedError
