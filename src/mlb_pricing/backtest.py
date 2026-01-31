import pandas as pd
import numpy as np

def kelly_fraction(p: float, odds: float, max_fraction: float = 0.5) -> float:
    """
    Compute Kelly fraction for American odds and win prob p.
    Caps at max_fraction and returns 0 if odds are invalid.
    """
    if pd.isna(odds) or odds == 0:
        return 0.0
    if odds > 0:
        b = odds / 100.0
    else:
        b = 100.0 / -odds
    if b == 0:
        return 0.0

    q = 1 - p
    f = (b * p - q) / b
    return float(np.clip(f, 0.0, max_fraction))

def run_backtest(
    market_compare: pd.DataFrame,
    bankroll0: float = 10_000,
    fraction: float = 0.25,
    kelly_cap: float = 0.5,
) -> dict:
    """
    Dynamic-bankroll backtest on a market_compare-like frame with:
    - p_home_win, p_away_win
    - home_moneyline, away_moneyline
    - home_win_actual, away_win_actual
    - home_bet_flag, away_bet_flag
    Returns updated DataFrame, equity curve, and ROI stats.
    """
    df = market_compare.copy()

    df["kelly_home_capped"] = df.apply(
        lambda r: kelly_fraction(r["p_home_win"], r["home_moneyline"], kelly_cap),
        axis=1,
    )
    df["kelly_away_capped"] = df.apply(
        lambda r: kelly_fraction(r["p_away_win"], r["away_moneyline"], kelly_cap),
        axis=1,
    )

    bankroll = bankroll0
    equity = []
    stake_home_records = []
    stake_away_records = []
    pnl_home_records = []
    pnl_away_records = []
    pnl_total_records = []

    def bet_pnl_safe(stake, odds, win):
        if pd.isna(odds) or odds == 0:
            return 0.0
        if win == 1:
            if odds > 0:
                return stake * (odds / 100.0)
            else:
                return stake * (100.0 / -odds)
        else:
            return -stake

    for _, row in df.iterrows():
        stake_home = fraction * row["kelly_home_capped"] * bankroll if row["home_bet_flag"] else 0.0
        stake_away = fraction * row["kelly_away_capped"] * bankroll if row["away_bet_flag"] else 0.0

        pnl_home = bet_pnl_safe(stake_home, row["home_moneyline"], row["home_win_actual"])
        pnl_away = bet_pnl_safe(stake_away, row["away_moneyline"], row["away_win_actual"])
        pnl_total = pnl_home + pnl_away
        bankroll += pnl_total

        stake_home_records.append(stake_home)
        stake_away_records.append(stake_away)
        pnl_home_records.append(pnl_home)
        pnl_away_records.append(pnl_away)
        pnl_total_records.append(pnl_total)
        equity.append(bankroll)

    df["stake_home"] = stake_home_records
    df["stake_away"] = stake_away_records
    df["pnl_home"] = pnl_home_records
    df["pnl_away"] = pnl_away_records
    df["pnl_total"] = pnl_total_records

    equity_curve = pd.Series(equity, index=df.index)
    roi_by_season = df.groupby("season")["pnl_total"].sum() / bankroll0
    overall_roi = (bankroll - bankroll0) / bankroll0

    return {
        "df": df,
        "equity_curve": equity_curve,
        "roi_by_season": roi_by_season,
        "overall_roi": overall_roi,
    }
