from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")

def load_odds() -> pd.DataFrame:
    """
    Load and combine Kaggle (2012–2021) and SBR (2021–2025) odds
    into a single 'odds' DataFrame with the unified schema.
    """
    # TODO: paste your existing odds_kaggle / odds_sbr logic here.
    raise NotImplementedError

def load_games() -> pd.DataFrame:
    """
    Load game results with game_id, teams, runs, odds, and season.
    """
    # TODO: use your existing 'games' builder.
    raise NotImplementedError

def load_fangraphs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load Fangraphs team batting, pitching, and fielding datasets.
    """
    batting = pd.read_csv(DATA_DIR / "raw" / "fangraphs_team_batting_2012_2025.csv")
    pitching = pd.read_csv(DATA_DIR / "raw" / "fangraphs_team_pitching_2012_2025.csv")
    fielding = pd.read_csv(DATA_DIR / "raw" / "fangraphs_team_fielding_2012_2025.csv")
    return batting, pitching, fielding
